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
import subprocess
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
  | [\w.-]+\.(?:pem|key|p12|pfx|jks|keystore)(?![\w.-])
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
# Copilot writes require Gandalf and approval; credentials and settings stay protected.
SENSITIVE_COPILOT = re.compile(r"(?i)\b(?:config|mcp-config|settings)\.json\b|[\w.-]*(?:oauth|token|credential|secret)[\w.-]*")
READ_CMDS = {"ls", "cat", "head", "tail", "wc", "grep", "rg", "find", "stat", "file", "diff", "jq", "du", "cd", "pwd", "echo", "cut"}
FIND_WRITES = {"-delete", "-exec", "-execdir", "-ok", "-okdir", "-fprint", "-fls", "-fprintf", "--pre", "--pre-glob"}
HIDDEN_GLOB = re.compile(r"(?:~|\$\{?HOME\}?|(?<![\w.])/[^\s]*?)/\.[^\s/]*[*?\[{]")
DYNAMIC_SUB = re.compile(r"\b(?:git|gh)\s+(?:\$\(|`)")
SHELLS = {"bash", "sh", "zsh", "dash"}
MERGE_API = re.compile(r"mergePullRequest|enablePullRequestAutoMerge|/pulls/[^\s/]+/merge\b")
SECRET_CMD = re.compile(r"\bgh\s+auth\s+(?:token|status\s+(?:-t|--show-token))\b|\bsecurity\s+find-(?:generic|internet)-password\b|\.config/gh/hosts\.yml")
FORCE_PUSH = re.compile(r"^(?:--force|--prune|--delete|--mirror|-[a-zA-Z]*[fd][a-zA-Z]*|[+:].+)$")
LEASE_PUSH = re.compile(r"^--force-with-lease(?:=.*)?$")
SET_LIMIT = re.compile(r"^\s*python3?\s+(?:~|\$HOME|/\S+?)/\.copilot/guard/guard\.py\s+--set-limit\s+\d{3,6}\s*$")
STATE_TAMPER = re.compile(r"gandal\S*-g\S*|guard\.py\s+--set-limit|/(?:STOP|LIMIT)\b")


def after_rebase(cwd):
    """True when the last thing that moved HEAD in this repo was a finished rebase."""
    try:
        out = subprocess.run(["git", "reflog", "-1", "--format=%gs"], cwd=cwd, capture_output=True, text=True, timeout=3).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return "rebase" in out and "(finish)" in out
DELETE_API = re.compile(r"\bgh\s+api\b.*(?:-X|--method)\s*=?\s*DELETE\b|\bgh\s+repo\s+delete\b", re.I)
ASK_RAW = re.compile(
    r"\b(?:curl|wget)\b[^|;&]*\|\s*(?:sudo\s+)?(?:ba|z|da)?sh\b"
    r"|\bcurl\b[^|;&]*\s(?:-d|-F|-T|--data\S*|--form\S*|--upload-file)\b")

ASK = "ask: "
# sudo, force-push and remote deletes are denied outright. These ask Themis first.
SHADY = {
    "su", "doas", "nc", "ncat", "netcat", "ssh", "scp", "sftp", "rsync", "telnet", "ftp",
    "dd", "mkfs", "osascript", "launchctl", "crontab", "aws", "gcloud", "az", "twine",
}
# Commands whose listed subcommands deploy, publish or log in. They ask Themis first.
SHADY_SUB = {
    "npm": {"publish", "login", "adduser", "token", "owner", "access", "deprecate", "unpublish", "dist-tag"},
    "yarn": {"publish", "login"}, "pnpm": {"publish", "login"},
    "cargo": {"publish", "login"}, "gem": {"push"}, "mvn": {"deploy"}, "gradle": {"publish"},
    "docker": {"login", "push"},
    "terraform": {"apply", "destroy"},
    "kubectl": {"apply", "delete", "patch", "replace", "scale", "drain"},
    "helm": {"install", "upgrade", "uninstall", "rollback"},
}
ENV_DUMP = {"printenv", "declare", "typeset"}
WRAPPERS = {"env", "command", "builtin", "time", "nohup", "nice", "exec", "timeout", "setsid", "stdbuf", "watch"}
KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "while", "until", "for", "case", "esac", "!", "{", "}"}
PRIVATE_HOST = re.compile(r"^(?:localhost|127\.|10\.|192\.168\.|169\.254\.|172\.(?:1[6-9]|2\d|3[01])\.|0\.0\.0\.0|\[?::1)")


def resolve(path, cwd):
    return os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))


def path_problem(path, cwd, write, orch=False):
    """Why a file path is off limits, or None."""
    real = resolve(path, cwd)
    lexical = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
    if write and ("gandalf-guard" in real or "gandalf-guard" in lexical):
        return f"guard state is protected: {path}"
    if SECRET.search(real) or SECRET.search(lexical):
        return f"{path} looks like a secret file"
    for p in (real, lexical):
        if COPILOT_HOME.search(p) and (write or SENSITIVE_COPILOT.search(p)):
            if write and orch and not SENSITIVE_COPILOT.search(p):
                return f"{ASK}writing under Copilot's home is only for Themis to approve"
            return "Copilot's own config is off limits"
    return None


def parse(command):
    """Return word segments, redirect targets and pipeline group IDs."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    segments, words, targets, redirect = [], [], [], False
    groups, group = [], 0
    for tok in lex:
        if redirect:
            targets.append(tok)
            redirect = False
        elif set(tok) <= set("();&|"):
            segments.append(words)
            groups.append(group)
            if tok.strip(";") not in ("|", "|&"):
                group += 1
            words = []
        elif "<<" in tok:
            raise ValueError("heredocs are not supported, use the edit tool")
        elif "<" in tok or ">" in tok:
            redirect = ">" in tok
        else:
            words.append(tok)
    return (segments + [words],
            [t for t in targets if t != "/dev/null" and not re.match(r"&?\d*-?$", t)],
            groups + [group])


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
        return first_sub(args) == "merge" and "--abort" not in args
    if cmd == "gh":
        words = [a for a in args if not a.startswith("-")]
        return any(words[i:i + 2] == ["pr", "merge"] for i in range(len(words)))
    return False


def check_words(words, orch, cwd="."):
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
    # Wrappers that run another command are checked as that command.
    if cmd == "eval":
        return check_shell(" ".join(args), cwd, orch)
    if cmd == "xargs":
        return check_words([a for a in args if not a.startswith("-")], orch, cwd)
    if cmd in SHELLS and "-c" in args[:-1]:
        return check_shell(args[args.index("-c") + 1], cwd, orch)
    if cmd in ("git", "gh") and ((first_sub(args) or "").startswith(("$", "`")) or any(a.startswith("alias.") for a in args)):
        return f"a dynamic or aliased {cmd} subcommand is not allowed"
    if merges(cmd, args):
        return f"{ASK if orch else ''}{cmd} merge is only for Themis to approve"
    if cmd == "git" and first_sub(args) == "push":
        push_args = args[sub_index(args) + 1:]
        if any(FORCE_PUSH.match(a) for a in push_args):
            return "force-push and remote deletes are not allowed"
        if any(LEASE_PUSH.match(a) for a in push_args) and not after_rebase(cwd):
            return "force-push is only allowed with --force-with-lease right after a rebase"
    if cmd in SHADY or first_sub(args) in SHADY_SUB.get(cmd, ()):
        return f"{ASK}{cmd} {first_sub(args) or ''}".rstrip() + " is sensitive"
    return None


def copilot_read_problem(segments, groups, orch):
    """Check Copilot-touching pipelines without restricting unrelated commands."""
    relevant = {group for words, group in zip(segments, groups) if COPILOT_HOME.search(" ".join(words))}
    problems, inside = [], False
    for words, group in zip(segments, groups):
        if not inside and group not in relevant:
            continue
        for path in words:
            if not inside and not COPILOT_HOME.search(path):
                continue
            if SENSITIVE_COPILOT.search(path):
                return "Copilot credentials and settings are protected"
            if re.search(r"(?:^|[/\s])\.\.(?:/|\s|$)", path):
                problems.append(f"{ASK if orch else ''}Copilot home: parent-directory traversal in {path!r}")
        if any("=" in w.split("/")[0] and COPILOT_HOME.search(w) for w in words):
            inside = True
        words = [w for w in words if "=" not in w.split("/")[0]]
        if words and (os.path.basename(words[0]) not in READ_CMDS or FIND_WRITES & set(words[1:])):
            problems.append(f"{ASK if orch else ''}Copilot home: {os.path.basename(words[0])} may write or execute code")
        if words and os.path.basename(words[0]) == "cd":
            inside = True
    return next((p for p in problems if not p.startswith(ASK)), problems[0] if problems else None)


def check_shell(command, cwd, orch):
    command = re.sub(r"\\\r?\n", "", command)
    bare = command.replace("'", "").replace('"', "").replace("\\", "")
    if SECRET.search(command) or SECRET.search(bare) or SECRET_CMD.search(command) or "/proc/" in command and "environ" in command:
        return "the command touches a secret file"
    if SECRET_ENV_VAR.search(command):
        return "the command reads a secret-looking environment variable"
    # The one way to raise the call limit: Gandalf runs it and Themis approves the prompt.
    if SET_LIMIT.match(command):
        return f"{ASK if orch else ''}raising the call limit is only for Themis to approve"
    if m := STATE_TAMPER.search(command):
        return f"{ASK if orch else ''}guard state is protected (matched {m.group(0)!r})"
    if HIDDEN_GLOB.search(bare) or DYNAMIC_SUB.search(command):
        return "globs on hidden names and dynamic git or gh subcommands are not allowed"
    if MERGE_API.search(command) or DELETE_API.search(command):
        return f"{ASK if orch else ''}merging or deleting through the API is only for Themis to approve"
    if ASK_RAW.search(command):
        return f"{ASK}curl upload or pipe to shell is sensitive"
    # Line breaks and substitutions split into segments, so each part is still checked.
    try:
        segments, targets, groups = parse(re.sub(r"[\r\n`]|\$\(|[<>]\(", ";", command))
    except ValueError:
        segments, targets = [w.split() for w in re.split(r"[;&|()\r\n`]+", command)], []
        groups = [0] * len(segments)
    if re.search(r"`|\$\(|[<>]\(", command):
        groups = [0] * len(segments)
    problems = []
    if COPILOT_HOME.search(bare) and (problem := copilot_read_problem(segments, groups, orch)):
        problems.append(problem)
    for target in targets:
        if problem := path_problem(target, cwd, True, orch):
            problems.append(problem)
    problems.extend(p for words in segments if (p := check_words(words, orch, cwd)))
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
        problems = [p for path in paths if (p := path_problem(path, cwd, True, orch))]
        return next((p for p in problems if not p.startswith(ASK)), problems[0] if problems else None)
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
        return path_problem(path, cwd, tool == "Write", orch)
    if tool in ("WebFetch", "WebSearch"):
        try:
            url = urlparse(str(args.get("url", "")))
            host = url.hostname or ""
        except ValueError:
            return "the URL is not valid"
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


MAX_CALLS = 500
MAX_DENIALS = 10
STATE_DIR = os.path.join(tempfile.gettempdir(), "gandalf-guard")


def bump(kind, role, session_id, directory=None):
    """Count one event and return the new total. Old counter files are pruned."""
    directory = directory or STATE_DIR
    os.makedirs(directory, mode=0o700, exist_ok=True)
    now = time.time()
    for name in os.listdir(directory):
        p = os.path.join(directory, name)
        try:
            if name != "STOP" and now - os.path.getmtime(p) > 86400:
                os.remove(p)
        except FileNotFoundError:
            continue
    path = os.path.join(directory, hashlib.sha256(f"{kind}\0{session_id}\0{role}".encode()).hexdigest()[:32])
    with open(path, "ab") as f:
        f.write(b".")
    return os.path.getsize(path)


def call_limit(directory=None):
    """MAX_CALLS, or the higher limit Themis approved with --set-limit (it expires with the day-old prune)."""
    try:
        with open(os.path.join(directory or STATE_DIR, "LIMIT")) as f:
            return max(MAX_CALLS, min(int(f.read().strip()), 100000))
    except (OSError, ValueError):
        return MAX_CALLS


def set_limit(n, directory=None):
    directory = directory or STATE_DIR
    os.makedirs(directory, mode=0o700, exist_ok=True)
    fd = os.open(os.path.join(directory, "LIMIT"), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(str(n))


def over_budget(role, session_id, directory=None):
    """Count this call; True once a role passes the call limit in one session."""
    return bump("calls", role, session_id, directory) > call_limit(directory)


def halted(role, session_id, directory=None):
    """The kill switch: a STOP file, or too many blocked attempts, halts a role in a session."""
    directory = directory or STATE_DIR
    if os.path.exists(os.path.join(directory, "STOP")):
        return "a STOP file exists, Themis halted all agents"
    path = os.path.join(directory, hashlib.sha256(f"strikes\0{session_id}\0{role}".encode()).hexdigest()[:32])
    if os.path.exists(path) and os.path.getsize(path) >= MAX_DENIALS:
        return f"{MAX_DENIALS} blocked attempts, this role is halted"
    return None


def state(fn, default, *args):
    """Run a counter or kill-switch step; a state-dir error must not block the agent."""
    try:
        return fn(*args)
    except OSError:
        return default


def decide(role, event, directory=None):
    """The deny reason for one call, or None."""
    session_id = event.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        return "the payload has no session_id, so calls cannot be counted"
    reason = state(halted, None, role, session_id, directory) or check(role, event)
    if not reason and state(over_budget, False, role, session_id, directory):
        reason = f"more than {call_limit(directory)} tool calls in this session, which looks like a runaway loop; ask Themis to raise the limit"
    if reason and not reason.startswith(("a STOP", f"{MAX_DENIALS} blocked", ASK)):
        state(bump, 0, "strikes", role, session_id, directory)
    return reason


def crash_reason(role, raw, error):
    """After a guard bug: reads that cannot touch secrets go through, everything else is denied."""
    try:
        tool = TOOL_ALIASES.get(str(json.loads(raw).get("tool_name", "")).lower(), "")
    except Exception:
        tool = ""
    unsafe = SECRET.search(raw) or TOKENS.search(raw) or (COPILOT_HOME.search(raw) and SENSITIVE_COPILOT.search(raw))
    if tool == "Read" and role in ROLES and not unsafe:
        return None
    return f"the guard failed ({type(error).__name__}), failing closed"


RULE_CODES = (
    ("guard failed", "crash"), ("guard state", "state"), ("STOP", "stop"),
    ("blocked attempts", "halt"), ("tool calls", "budget"),
    ("sudo", "sudo"), ("force-push", "force-push"), ("merg", "merge"), ("secret", "secret"),
    ("Copilot", "config"), ("environment", "env"), ("sensitive", "ask-cmd"), ("agent", "spawn"),
    ("https", "web"), ("patch", "patch"),
)
LOG_LIMIT = 1_000_000


def rule_code(reason):
    return next((code for text, code in RULE_CODES if text in reason), "other")


def log_decision(role, raw, reason, crashed):
    """Append one redacted line (no command, path or token) per deny, ask or crash. Never raises."""
    try:
        path = os.environ.get("GUARD_LOG") or os.path.expanduser("~/.copilot/guard-logs/denials.log")
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        if os.path.exists(path) and os.path.getsize(path) > LOG_LIMIT:
            os.replace(path, path + ".1")
        try:
            event = json.loads(raw)
            tool, session = str(event.get("tool_name", "")), str(event.get("session_id", ""))[:8]
        except Exception:
            tool, session = "", ""
        code = "crash-allowed" if crashed and not reason else rule_code(reason or "")
        kind = "ask" if reason and reason.startswith(ASK) else "deny" if reason else "allow"
        line = json.dumps({"ts": int(time.time()), "role": role, "tool": tool, "kind": kind, "code": code, "session": session})
        fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
        with os.fdopen(fd, "a") as f:
            f.write(line + "\n")
    except Exception:
        pass


def main():
    role = sys.argv[1] if len(sys.argv) > 1 else ""
    if role == "--set-limit" and len(sys.argv) == 3 and sys.argv[2].isdigit():
        set_limit(sys.argv[2])
        print(f"call limit is now {call_limit()} until the state files are a day old")
        return
    raw, crashed = sys.stdin.read(), False
    try:
        reason = decide(role, json.loads(raw))
    except Exception as e:
        reason, crashed = crash_reason(role, raw, e), True
    if reason or crashed:
        log_decision(role, raw, reason, crashed)
    if reason and reason.startswith(ASK):
        print(json.dumps({
            "permissionDecision": "ask",
            "permissionDecisionReason": f"{role} needs Themis's approval: {reason[len(ASK):]}.",
        }))
    elif reason:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": f"BLOCKED [{rule_code(reason)}] {role}: {reason}.",
        }))


if __name__ == "__main__":
    main()
