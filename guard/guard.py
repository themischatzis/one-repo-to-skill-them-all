#!/usr/bin/env python3
"""preToolUse guard for Gandalf and his role agents.

Usage: guard.py <role>, with the PreToolUse payload (snake_case) on stdin.

Prints a deny decision, or nothing. Nothing leaves Copilot's normal permission
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

TESTS = ("**/test/**", "**/tests/**", "**/__tests__/**", "**/*.test.*", "**/*.spec.*", "**/*Test.*", "**/*_test.*")
DOCS = ("**/*.md", "**/docs/**")

# role: (class, write scope). Scope None means anywhere inside the working directory.
ROLES = {
    "adversary": ("read", None), "architect": ("read", None), "manager": ("read", None),
    "retrieval": ("read", None), "vp": ("read", None),
    "analyst": ("research", None), "visionary": ("research", None),
    "reviewer": ("inspect", None), "security": ("inspect", None),
    "backend": ("build", None), "frontend": ("build", None), "devops": ("build", None),
    "ml-engineer": ("build", None), "prompt-engineer": ("build", None),
    "ci-fixer": ("build", None), "resolver": ("build", None),
    "qa": ("build", TESTS), "docs": ("build", DOCS),
    "sam": ("build", None), "gollum": ("inspect", None),
    "gandalf": ("orchestrate", None),
}
STARTABLE = set(ROLES) - {"gandalf"}

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
    r"|sk-[A-Za-z0-9_-]{20,}|AIza[\w-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}")
COPILOT_HOME = re.compile(r"\.copilot(?:/|\b)")

ALWAYS_DENY = {
    "sudo", "su", "doas", "curl", "wget", "nc", "ncat", "netcat", "ssh", "scp", "sftp", "rsync",
    "telnet", "ftp", "eval", "xargs", "chmod", "chown", "chgrp", "dd", "mkfs", "mount", "osascript",
    "launchctl", "crontab", "defaults", "printenv", "declare", "typeset", "aws", "gcloud", "az",
    "twine", "wp",
}
# Commands whose listed subcommands deploy, publish, log in or run arbitrary code.
DENY_SUB = {
    "npm": {"publish", "login", "adduser", "logout", "token", "owner", "access", "deprecate", "unpublish", "dist-tag", "team", "org", "profile"},
    "yarn": {"publish", "login", "npm"}, "pnpm": {"publish", "login"},
    "cargo": {"publish", "login"}, "gem": {"push"}, "mvn": {"deploy"}, "gradle": {"publish"},
    "docker": {"login", "push", "run", "exec", "compose", "system", "rm", "rmi"},
    "terraform": {"apply", "destroy", "import", "taint"},
    "kubectl": {"apply", "delete", "exec", "patch", "create", "replace", "scale", "rollout", "cp", "edit", "drain", "cordon"},
    "helm": {"install", "upgrade", "uninstall", "rollback"},
}
GIT_ALLOW = {
    "status", "diff", "log", "show", "blame", "ls-files", "ls-tree", "rev-parse", "rev-list", "describe",
    "grep", "shortlog", "cat-file", "show-ref", "merge-base", "name-rev", "diff-tree", "check-ignore", "branch",
}
GIT_BAD_FLAG = re.compile(r"--(?:ext-diff|no-index|open-files-in-pager|textconv)|-O")
GIT_BRANCH_LIST = {"--show-current", "-a", "--all", "-r", "--remotes", "-v", "-vv", "--verbose", "-l", "--list"}
GIT_BRANCH_VALUE = {"--contains", "--no-contains", "--merged", "--no-merged", "--points-at", "--sort", "--format"}
# Read-only GitHub access. Anything that changes or deletes remote state is absent on purpose.
GH_ALLOW = {
    "pr": {"view", "list", "diff", "checks", "status"}, "issue": {"view", "list", "status"},
    "run": {"view", "list"}, "repo": {"view"}, "release": {"view", "list"}, "workflow": {"view", "list"},
    "label": {"list"}, "search": {"code", "commits", "issues", "prs", "repos"},
}
INTERPRETERS = re.compile(r"(?:python[\d.]*|node|deno|bun|php|ruby|perl|bash|sh|zsh|dash|fish)$")
INLINE_FLAGS = {"--eval", "--print"}
INLINE_CLUSTER = re.compile(r"-[A-Za-z]*[ceEpr]")
WRAPPERS = {"env", "command", "builtin", "time", "nohup", "nice", "exec", "timeout", "setsid", "stdbuf", "watch"}
KEYWORDS = {"if", "then", "else", "elif", "fi", "do", "done", "while", "until", "for", "case", "esac", "!", "{", "}"}
WRITERS = {"tee", "mv", "cp", "touch", "mkdir", "rmdir", "rm", "ln", "install", "patch", "truncate", "shred"}
PRIVATE_HOST = re.compile(r"^(?:localhost|127\.|10\.|192\.168\.|169\.254\.|172\.(?:1[6-9]|2\d|3[01])\.|0\.0\.0\.0|\[?::1)")


def glob_re(glob):
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("/**", i):
            out, i = out + "(?:/.*)?", i + 3
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + r"\Z")


def resolve(path, cwd):
    return os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))


def inside(path, cwd):
    return path == cwd or path.startswith(cwd + os.sep)


def path_problem(path, cwd, write, scope=None):
    """Why a file path is off limits, or None."""
    real = resolve(path, cwd)
    if SECRET.search(real):
        return f"{path} looks like a secret file"
    if COPILOT_HOME.search(real) and (write or "/.copilot/skills/" not in real):
        return "Copilot's own config is off limits"
    if write:
        if not inside(real, cwd):
            return f"{path} is outside the working directory"
        if ".git" in os.path.relpath(real, cwd).split(os.sep):
            return "writing inside .git is not allowed"
        if scope and not any(glob_re(g).match(os.path.relpath(real, cwd)) for g in scope):
            return f"{path} is outside this role's write scope"
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


def first_sub(args):
    """First non-option word, skipping the values of -C and -c."""
    skip = False
    for a in args:
        if skip:
            skip = False
        elif a in ("-C", "-c"):
            skip = True
        elif not a.startswith("-"):
            return a
    return None


def branch_problem(args):
    """git branch may only list: known list flags, plus values for the filter flags."""
    skip, listing = False, any(a in ("-l", "--list") for a in args)
    for a in args:
        if skip:
            skip = False
        elif a in GIT_BRANCH_VALUE:
            skip = True
        elif a.split("=", 1)[0] in GIT_BRANCH_VALUE or a in GIT_BRANCH_LIST:
            continue
        elif not a.startswith("-") and listing:
            continue
        else:
            return "git branch may only list"
    return None


def api_problem(args):
    """gh api may only send GET requests with no body."""
    for i, a in enumerate(args):
        if a.startswith("--"):
            name, _, value = a.partition("=")
            if name in ("--field", "--raw-field", "--input"):
                return "gh api may only read"
            if name == "--method" and (value or (args[i + 1:i + 2] or [""])[0]).upper() != "GET":
                return "gh api may only read"
        elif a.startswith("-") and len(a) > 1:
            for j, c in enumerate(a[1:], 1):
                if c in "fF":
                    return "gh api may only read"
                if c == "X":
                    if (a[j + 1:] or (args[i + 1:i + 2] or [""])[0]).upper() != "GET":
                        return "gh api may only read"
                    break
                if c in "HqtpR":
                    break
    return None


def check_words(words, cwd, may_write):
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
    if cmd in ALWAYS_DENY:
        return f"{cmd} is not allowed"
    if cmd == "set" and not args or cmd == "export" and (not args or "-p" in args):
        return "dumping the environment is not allowed"
    if INTERPRETERS.match(cmd) and (not args or INLINE_FLAGS & set(args) or any(INLINE_CLUSTER.match(a) for a in args)):
        return f"{cmd} with inline code or stdin is not allowed, write a file and run it"
    if cmd == "find" and {"-delete", "-exec", "-execdir", "-ok", "-okdir"} & set(args):
        return "find with -delete or -exec is not allowed"
    if cmd == "git":
        if "-c" in args or any(a.startswith(("--config-env", "--output", "--exec-path")) or GIT_BAD_FLAG.match(a) for a in args):
            return "git config overrides, --output and external programs are not allowed"
        sub = first_sub(args)
        if sub not in GIT_ALLOW:
            return f"git {sub} is not allowed, the parent handles git"
        if sub == "branch" and (problem := branch_problem(args[args.index("branch") + 1:])):
            return problem
    elif cmd == "gh":
        sub, rest = args[:1], args[1:2]
        if sub == ["api"]:
            if problem := api_problem(args[1:]):
                return problem
        elif not (sub and rest and rest[0] in GH_ALLOW.get(sub[0], ())):
            return f"gh {' '.join(args[:2])} is not allowed"
    elif cmd in DENY_SUB and first_sub(args) in DENY_SUB[cmd]:
        return f"{cmd} {first_sub(args)} is not allowed"
    if cmd in WRITERS or cmd in ("sed", "perl") and any(a.startswith("-i") for a in args):
        if not may_write:
            return f"{cmd} writes files, which this role may not do from the shell"
        if cmd == "rm" and any(a.startswith("-") and set(a[1:]) & set("rRf-") for a in args):
            return "rm with -r or -f is not allowed"
        for a in args:
            if not a.startswith("-") and (problem := path_problem(a, cwd, True)):
                return problem
    return None


def check_shell(command, cwd, may_write):
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
    try:
        segments, targets = parse(command)
    except ValueError as e:
        return str(e)
    for target in targets:
        if not may_write:
            return "this role may not write files from the shell"
        if problem := path_problem(target, cwd, True):
            return problem
    for words in segments:
        if problem := check_words(words, cwd, may_write):
            return problem
    return None


TOOL_ALIASES = {
    "bash": "Bash", "shell": "Bash", "powershell": "Bash",
    "write": "Write", "edit": "Write", "multiedit": "Write", "notebookedit": "Write", "create": "Write",
    "str_replace": "Write", "str_replace_editor": "Write", "apply_patch": "Write",
    "read": "Read", "view": "Read", "grep": "Read", "glob": "Read",
    "webfetch": "WebFetch", "web_fetch": "WebFetch", "websearch": "WebSearch", "web_search": "WebSearch",
    "agent": "Agent", "task": "Agent",
}


def check(role, event):
    cls, scope = ROLES[role]
    args = event.get("tool_input") or {}
    if not isinstance(args, dict):
        return "the tool input is not an object"
    tool = TOOL_ALIASES.get(str(event.get("tool_name", "")).lower(), "")
    cwd = os.path.realpath(event.get("cwd") or ".")
    if TOKENS.search(json.dumps(args)):
        return "the tool input contains a secret-looking value"
    path = args.get("path") or args.get("file_path")
    if path is not None and not isinstance(path, str):
        return "the path is not a string"
    if tool == "Bash":
        if cls not in ("inspect", "build"):
            return "this role has no shell"
        command = args.get("command", "")
        if not isinstance(command, str):
            return "the command is not a string"
        return check_shell(command, cwd, cls == "build" and scope is None)
    if tool == "Write":
        if cls != "build":
            return "this role is read-only"
        return path_problem(path, cwd, True, scope) if path else "an edit without a path cannot be checked"
    if tool == "Read" and path:
        return path_problem(path, cwd, False)
    if tool in ("WebFetch", "WebSearch"):
        if cls != "research":
            return "this role has no web access"
        url = urlparse(str(args.get("url", "")))
        host = url.hostname or ""
        if tool == "WebFetch" and (url.scheme != "https" or "@" in url.netloc or PRIVATE_HOST.match(host)
                                   or host.isdigit() or host.lower().startswith("0x") or ":" in host):
            return "only public https URLs without credentials are allowed"
    if tool == "Agent":
        if cls != "orchestrate":
            return "only Gandalf may start other agents"
        if args.get("agent_type") not in STARTABLE:
            return "Gandalf may only start the role agents, sam or gollum"
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
    if reason and not reason.startswith(("a STOP", f"{MAX_DENIALS} blocked")):
        bump("strikes", role, session_id, directory)
    return reason


def main():
    role = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        reason = decide(role, json.load(sys.stdin))
    except Exception as e:
        reason = f"the guard failed ({type(e).__name__}), failing closed"
    if reason:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": f"Blocked by guard ({role}): {reason}. Report BLOCKED to the parent with this reason; do not look for another route.",
        }))


if __name__ == "__main__":
    main()
