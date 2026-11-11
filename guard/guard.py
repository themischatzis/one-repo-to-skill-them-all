#!/usr/bin/env python3
"""preToolUse guard for Gandalf and his role agents.

Usage: guard.py <role>, with the PreToolUse payload (snake_case) on stdin.

Prints a deny or ask decision, or nothing. Nothing leaves Copilot's normal permission
flow, prompts included: the guard never approves a call. Any error, a bad
payload or an unknown role is printed as a deny.
"""
import hashlib
import json
import os
import re
import shlex
import sys
import tempfile
import time
from urllib.parse import urlparse

ROLES = {
    "adversary", "architect", "manager", "retrieval", "vp", "analyst", "visionary",
    "reviewer", "security", "backend", "frontend", "devops", "ml-engineer", "prompt-engineer",
    "ci-fixer", "resolver", "qa", "docs", "sam", "gollum", "gandalf",
}
ORCH = "gandalf"

SECRET = re.compile(r"""(?:^|[/\s='"])(?:
    \.env(?:\.(?!(?:example|sample|template)\b)[\w.-]+)?(?![\w.-])
  | [\w.-]+\.(?:pem|key|p12|pfx|jks|keystore)\b
  | id_(?:rsa|dsa|ecdsa|ed25519)\b(?!\.pub)
  | \.(?:ssh|aws|gnupg|kube|docker)(?:/|\b)
  | \.(?:npmrc|netrc|pypirc|git-credentials)\b
  | credentials\.json\b
)""", re.X)
SECRET_ENV_VAR = re.compile(r"\$\{?\w*(?:TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|PRIVATE_KEY|CREDENTIAL)", re.I)
TOKENS = re.compile(
    r"gh[pousr]_[A-Za-z0-9]{36,}|github_pat_\w{40,}|AKIA[0-9A-Z]{16}|xox[abprs]-[\w-]{10,}"
    r"|(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}|AIza[\w-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}")
COPILOT_HOME = re.compile(r"\.copilot(?:/|\b)")
MERGE_API = re.compile(r"mergePullRequest|enablePullRequestAutoMerge|/pulls/[^\s/]+/merge\b")

ASK = "ask: "
# sudo is the only command denied outright. These ask Themis first.
SHADY = {
    "su", "doas", "curl", "wget", "nc", "ncat", "netcat", "ssh", "scp", "sftp", "rsync", "telnet", "ftp",
    "eval", "xargs", "chmod", "chown", "chgrp", "dd", "mkfs", "mount", "osascript", "launchctl", "crontab",
    "defaults", "aws", "gcloud", "az", "twine", "wp",
}
# Commands whose listed subcommands deploy, publish or log in. They ask Themis first.
SHADY_SUB = {
    "npm": {"publish", "login", "adduser", "logout", "token", "owner", "access", "deprecate", "unpublish", "dist-tag", "team", "org", "profile"},
    "yarn": {"publish", "login", "npm"}, "pnpm": {"publish", "login"},
    "cargo": {"publish", "login"}, "gem": {"push"}, "mvn": {"deploy"}, "gradle": {"publish"},
    "docker": {"login", "push", "run", "exec", "compose", "system", "rm", "rmi"},
    "terraform": {"apply", "destroy", "import", "taint"},
    "kubectl": {"apply", "delete", "exec", "patch", "create", "replace", "scale", "rollout", "cp", "edit", "drain", "cordon"},
    "helm": {"install", "upgrade", "uninstall", "rollback"},
}
ENV_DUMP = {"printenv", "declare", "typeset"}
WRAPPERS = {"env", "command", "builtin", "time", "nohup", "nice", "exec", "timeout", "setsid", "stdbuf", "watch"}
KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "while", "until", "for", "case", "esac", "!", "{", "}"}
PRIVATE_HOST = re.compile(r"^(?:localhost|127\.|10\.|192\.168\.|169\.254\.|172\.(?:1[6-9]|2\d|3[01])\.|0\.0\.0\.0|\[?::1)")


def resolve(path, cwd):
    return os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))


def path_problem(path, cwd, write):
    """Why a file path is off limits, or None."""
    real = resolve(path, cwd)
    lexical = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
    if SECRET.search(real) or SECRET.search(lexical):
        return f"{path} looks like a secret file"
    for p in (real, lexical):
        if COPILOT_HOME.search(p) and (write or "/.copilot/skills/" not in p):
            return "Copilot's own config is off limits"
    return None


def parse(command):
    """Split a command into (segments of words, redirect targets). Raises ValueError if unparseable."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    segments, words, targets, redirect = [], [], [], False
    for tok in lex:
        if redirect:
            targets.append(tok)
            redirect = False
        elif set(tok) <= set("();&|"):
            segments.append(words)
            words = []
        elif "<<" in tok:
            raise ValueError("heredocs are not supported, use the edit tool")
        elif "<" in tok or ">" in tok:
            redirect = ">" in tok
        else:
            words.append(tok)
    return segments + [words], [t for t in targets if t != "/dev/null" and not re.match(r"&?\d*-?$", t)]


def sub_index(args):
    """Index of the first non-option word, skipping the values of -C and -c; len(args) if none."""
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
        elif a in ("-C", "-c"):
            skip = True
        elif not a.startswith("-"):
            return i
    return len(args)


def first_sub(args):
    i = sub_index(args)
    return args[i] if i < len(args) else None


def merges(cmd, args):
    if cmd == "git":
        return first_sub(args) == "merge"
    if cmd == "gh":
        words = [a for a in args if not a.startswith("-")]
        return any(words[i:i + 2] == ["pr", "merge"] for i in range(len(words)))
    return False


def check_words(words, orch):
    while words and (words[0] in KEYWORDS or "=" in words[0].split("/")[0] or words[0] in WRAPPERS):
        wrapper = words[0]
        words = words[1:]
        while wrapper == "env" and words and (words[0].startswith("-") or "=" in words[0]):
            words = words[1:]
        if wrapper in WRAPPERS and wrapper != "env":
            while words and words[0].startswith("-"):
                words = words[1:]
            if wrapper in ("timeout", "nice", "watch") and words and re.match(r"\d+[smhd]?$", words[0]):
                words = words[1:]
        if wrapper == "env" and not words:
            return "dumping the environment is not allowed"
    if not words:
        return None
    cmd, args = os.path.basename(words[0]), words[1:]
    if cmd == "sudo":
        return "sudo is not allowed"
    if cmd in ENV_DUMP or cmd == "set" and not args or cmd == "export" and (not args or "-p" in args):
        return "dumping the environment is not allowed"
    if merges(cmd, args):
        return f"{ASK if orch else ''}{cmd} merge is only for Themis to approve"
    if cmd in SHADY or first_sub(args) in SHADY_SUB.get(cmd, ()):
        return f"{ASK}{cmd} {first_sub(args) or ''}".rstrip() + " is sensitive"
    return None


def check_shell(command, cwd, orch):
    if "`" in command:
        return "backticks are not supported, use $() or separate commands"
    if "\n" in command or "\r" in command:
        return "one command per call, no line breaks"
    if "<(" in command or ">(" in command:
        return "process substitution is not supported"
    bare = command.replace("'", "").replace('"', "").replace("\\", "")
    if SECRET.search(command) or SECRET.search(bare) or COPILOT_HOME.search(bare) or "/proc/" in command and "environ" in command:
        return "the command touches a secret file or Copilot's config"
    if SECRET_ENV_VAR.search(command):
        return "the command reads a secret-looking environment variable"
    if MERGE_API.search(command):
        return f"{ASK if orch else ''}merging through the API is only for Themis to approve"
    try:
        segments, targets = parse(command)
    except ValueError as e:
        return str(e)
    for target in targets:
        if problem := path_problem(target, cwd, True):
            return problem
    problems = [p for words in segments if (p := check_words(words, orch))]
    return next((p for p in problems if not p.startswith(ASK)), problems[0] if problems else None)


TOOL_ALIASES = {
    "bash": "Bash", "shell": "Bash", "powershell": "Bash",
    "write": "Write", "edit": "Write", "multiedit": "Write", "notebookedit": "Write", "create": "Write",
    "str_replace": "Write", "str_replace_editor": "Write", "apply_patch": "Write",
    "read": "Read", "view": "Read", "grep": "Read", "glob": "Read",
    "webfetch": "WebFetch", "web_fetch": "WebFetch", "websearch": "WebSearch", "web_search": "WebSearch",
    "agent": "Agent", "task": "Agent",
}


def check(role, event):
    if role not in ROLES:
        return "unknown role"
    orch = role == ORCH
    name = str(event.get("tool_name", "")).lower()
    tool = TOOL_ALIASES.get(name, "")
    cwd = os.path.realpath(event.get("cwd") or ".")
    args = event.get("tool_input")
    if TOKENS.search(json.dumps(args)):
        return "the tool input contains a secret-looking value"
    if tool == "Write" and isinstance(args, str):
        paths = re.findall(r"(?m)^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+)$", args)
        if not paths or not args.startswith("*** Begin Patch\n") or not args.rstrip().endswith("*** End Patch"):
            return "the patch has no checkable file operations"
        return next((p for path in paths if (p := path_problem(path, cwd, True))), None)
    args = args or {}
    if not isinstance(args, dict):
        return f"the {name} tool input is not an object ({type(args).__name__})"
    path = args.get("path") or args.get("file_path")
    if path is not None and not isinstance(path, str):
        return "the path is not a string"
    if tool == "Bash":
        command = args.get("command", "")
        if not isinstance(command, str):
            return "the command is not a string"
        return check_shell(command, cwd, orch)
    if tool in ("Write", "Read") and path:
        return path_problem(path, cwd, tool == "Write")
    if tool in ("WebFetch", "WebSearch"):
        url = urlparse(str(args.get("url", "")))
        host = url.hostname or ""
        if tool == "WebFetch" and (url.scheme != "https" or "@" in url.netloc or PRIVATE_HOST.match(host)
                                   or host.isdigit() or host.lower().startswith("0x") or ":" in host):
            return "only public https URLs without credentials are allowed"
    if tool == "Agent":
        if not orch:
            return "only Gandalf may start other agents"
        agent_type = args.get("agent_type")
        if not isinstance(agent_type, str) or not agent_type.strip() or agent_type.strip().lower() == ORCH:
            return "choose an explicit agent_type; recursive Gandalf runs are not allowed"
    return None


MAX_CALLS = 200
MAX_DENIALS = 10
STATE_DIR = os.path.join(tempfile.gettempdir(), "gandalf-guard")


def bump(kind, role, session_id, directory=None):
    """Count one event and return the new total. Old counter files are pruned."""
    directory = directory or STATE_DIR
    os.makedirs(directory, mode=0o700, exist_ok=True)
    now = time.time()
    for name in os.listdir(directory):
        p = os.path.join(directory, name)
        if name != "STOP" and now - os.path.getmtime(p) > 86400:
            os.remove(p)
    path = os.path.join(directory, hashlib.sha256(f"{kind}\0{session_id}\0{role}".encode()).hexdigest()[:32])
    with open(path, "ab") as f:
        f.write(b".")
    return os.path.getsize(path)


def over_budget(role, session_id, directory=None):
    """Count this call; True once a role passes MAX_CALLS in one session."""
    return bump("calls", role, session_id, directory) > MAX_CALLS


def halted(role, session_id, directory=None):
    """The kill switch: a STOP file, or too many blocked attempts, halts a role in a session."""
    directory = directory or STATE_DIR
    if os.path.exists(os.path.join(directory, "STOP")):
        return "a STOP file exists, Themis halted all agents"
    path = os.path.join(directory, hashlib.sha256(f"strikes\0{session_id}\0{role}".encode()).hexdigest()[:32])
    if os.path.exists(path) and os.path.getsize(path) >= MAX_DENIALS:
        return f"{MAX_DENIALS} blocked attempts, this role is halted"
    return None


def decide(role, event, directory=None):
    """The deny reason for one call, or None."""
    session_id = event.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        return "the payload has no session_id, so calls cannot be counted"
    reason = halted(role, session_id, directory) or check(role, event)
    if not reason and over_budget(role, session_id, directory):
        reason = f"more than {MAX_CALLS} tool calls in this session, which looks like a runaway loop"
    if reason and not reason.startswith(("a STOP", f"{MAX_DENIALS} blocked", ASK)):
        bump("strikes", role, session_id, directory)
    return reason


def main():
    role = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        reason = decide(role, json.load(sys.stdin))
    except Exception as e:
        reason = f"the guard failed ({type(e).__name__}), failing closed"
    if reason and reason.startswith(ASK):
        print(json.dumps({
            "permissionDecision": "ask",
            "permissionDecisionReason": f"{role} needs Themis's approval: {reason[len(ASK):]}.",
        }))
    elif reason:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Blocked by guard ({role}): {reason}. Report BLOCKED to the parent with this reason; do not look for another route.",
        }))


if __name__ == "__main__":
    main()
