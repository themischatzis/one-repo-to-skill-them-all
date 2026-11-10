"""Run with: python3 guard/test_guard.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

import guard

GUARD = os.path.join(os.path.dirname(os.path.abspath(guard.__file__)), "guard.py")
CWD = os.path.realpath(tempfile.mkdtemp())
GH_TOKEN = "gh" + "p_" + "A" * 36
AWS_KEY = "AK" + "IA" + "A" * 16
PEM = "-----BEGIN " + "RSA PRIVATE KEY-----"


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def write(path, text="x", tool="Write"):
    return {"tool_name": tool, "tool_input": {"path": path, "file_text": text}}


def read(path):
    return {"tool_name": "Read", "tool_input": {"path": path}}


# (role, event, denied)
CASES = [
    # git and GitHub: read allowed, everything that changes state denied
    ("backend", bash("git status && git diff --stat"), False),
    ("backend", bash("git log --oneline -5"), False),
    ("backend", bash("git branch --show-current"), False),
    ("backend", bash("git commit -m x"), True),
    ("backend", bash("git push origin main"), True),
    ("backend", bash("git -C . push"), True),
    ("backend", bash("git -c core.pager=sh log"), True),
    ("backend", bash("git branch -D old"), True),
    ("backend", bash("git status; git merge other"), True),
    ("backend", bash("echo a | git reset --hard"), True),
    ("reviewer", bash("gh pr view 12"), False),
    ("reviewer", bash("gh api repos/o/r/pulls/1"), False),
    ("reviewer", bash("gh pr merge 12"), True),
    ("reviewer", bash("gh pr create --title x"), True),
    ("reviewer", bash("gh api -X POST repos/o/r/issues"), True),
    ("reviewer", bash("gh api repos/o/r/issues -f title=x"), True),
    # secrets: paths, commands, env, token-shaped content
    ("backend", read(".env"), True),
    ("backend", read(".env.local"), True),
    ("backend", read(".env.example"), False),
    ("backend", read("~/.ssh/id_rsa"), True),
    ("backend", read("~/.aws/credentials"), True),
    ("backend", read("certs/server.pem"), True),
    ("backend", read("~/.copilot/config.json"), True),
    ("backend", read("~/.copilot/skills/ground-rules/SKILL.md"), False),
    ("backend", bash("cat .env"), True),
    ("backend", bash("cat < .env"), True),
    ("backend", bash("cp .env /tmp/x"), True),
    ("backend", bash("printenv"), True),
    ("backend", bash("env"), True),
    ("backend", bash("echo $GITHUB_TOKEN"), True),
    ("backend", bash("cat ~/.copilot/settings.json"), True),
    ("backend", write("notes.md", "key " + GH_TOKEN), True),
    ("backend", write("notes.md", AWS_KEY), True),
    ("backend", write("notes.md", PEM), True),
    ("backend", bash("echo " + GH_TOKEN), True),
    # writes: inside the working directory only, never to config
    ("backend", write(os.path.join(CWD, "src/a.php")), False),
    ("backend", write("src/a.php", tool="Edit"), False),
    ("backend", write("/etc/hosts"), True),
    ("backend", write("../outside.txt"), True),
    ("backend", write("~/.copilot/agents/backend.agent.md"), True),
    ("backend", write(".env"), True),
    ("backend", bash("echo hi > /tmp/x"), True),
    ("backend", bash("echo hi > out.txt"), False),
    ("backend", bash("echo hi > /dev/null"), False),
    ("backend", bash("tee ../x < a"), True),
    ("backend", bash("rm -rf build"), True),
    ("backend", bash("rm old.txt"), False),
    ("backend", bash("mv a.txt /tmp/a.txt"), True),
    ("backend", {"tool_name": "Edit", "tool_input": {"old_str": "a", "new_str": "b"}}, True),
    # shell escape hatches
    ("backend", bash("curl https://example.com"), True),
    ("backend", bash("sudo ls"), True),
    ("backend", bash("python3 -c 'print(1)'"), True),
    ("backend", bash("node -e 'x'"), True),
    ("backend", bash("bash -c 'ls'"), True),
    ("backend", bash("ls | sh"), True),
    ("backend", bash("eval ls"), True),
    ("backend", bash("ls `whoami`"), True),
    ("backend", bash("cat <<EOF\nhi\nEOF"), True),
    ("backend", bash("find . -name x -delete"), True),
    ("backend", bash("ls | xargs rm"), True),
    ("backend", bash("npm publish"), True),
    ("backend", bash("npm test && npm run build"), False),
    ("backend", bash("python3 -m pytest tests/ -q"), False),
    ("backend", bash("php -l src/a.php"), False),
    ("backend", bash("wp plugin list"), True),
    ("devops", bash("terraform plan"), False),
    ("devops", bash("terraform apply -auto-approve"), True),
    ("devops", bash("kubectl delete pod x"), True),
    ("devops", bash("aws s3 ls"), True),
    ("devops", bash("docker push img"), True),
    ("backend", bash('git log --format="%h (%s)"'), False),
    # roles: read-only, inspect, scoped
    ("architect", bash("ls"), True),
    ("architect", write("a.md"), True),
    ("architect", read("src/a.php"), False),
    ("reviewer", write("a.md"), True),
    ("reviewer", bash("npm test"), False),
    ("reviewer", bash("sed -i s/a/b/ f"), True),
    ("reviewer", bash("echo x > f"), True),
    ("reviewer", bash("touch f"), True),
    ("security", bash("git diff"), False),
    ("qa", write("tests/a_test.py"), False),
    ("qa", write("src/__tests__/a.test.ts"), False),
    ("qa", write("src/app.ts"), True),
    ("qa", bash("echo x > src/app.ts"), True),
    ("qa", bash("npm test"), False),
    ("docs", write("README.md"), False),
    ("docs", write("docs/guide/a.txt"), False),
    ("docs", write("src/app.ts"), True),
    # web and subagents
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "https://example.com/a"}}, False),
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "http://example.com"}}, True),
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "https://127.0.0.1/x"}}, True),
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "https://u:p@example.com"}}, True),
    ("backend", {"tool_name": "WebFetch", "tool_input": {"url": "https://example.com"}}, True),
    ("backend", {"tool_name": "Task", "tool_input": {"prompt": "x"}}, True),
    ("backend", {"tool_name": "Agent", "tool_input": {"prompt": "x"}}, True),
    ("gandalf", {"tool_name": "Task", "tool_input": {"prompt": "x", "agent_type": "backend"}}, False),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "sam"}}, False),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "gollum"}}, False),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "general-purpose"}}, True),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "task"}}, True),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x"}}, True),
    ("gandalf", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "gandalf"}}, True),
    ("backend", {"tool_name": "Agent", "tool_input": {"prompt": "x", "agent_type": "sam"}}, True),
    ("gandalf", bash("ls"), True),
    ("gandalf", write("a.md"), True),
    # sam and gollum are guarded like any role
    ("sam", bash("git push"), True),
    ("sam", write("src/a.php"), False),
    ("sam", write("../x"), True),
    ("gollum", write("a.md"), True),
    ("gollum", bash("git diff"), False),
    ("gollum", {"tool_name": "Agent", "tool_input": {"agent_type": "sam"}}, True),
    # line breaks, braces and process substitution
    ("backend", bash("git status\ngit push"), True),
    ("backend", bash("ls\r\ncurl x"), True),
    ("backend", bash("ls \\\n && git push"), True),
    ("backend", bash("{ git push; }"), True),
    ("backend", bash("ls <(git push)"), True),
    # flag forms
    ("backend", bash("git branch newbranch"), True),
    ("backend", bash("git branch -df old"), True),
    ("backend", bash("git branch --set-upstream-to=o/x"), True),
    ("backend", bash("git branch --list 'feat/*'"), False),
    ("backend", bash("git branch -a --contains abc123"), False),
    ("backend", bash("git grep -O sh x"), True),
    ("backend", bash("git diff --ext-diff"), True),
    ("backend", bash("git diff --no-index a b"), True),
    ("reviewer", bash("gh api -XPOST repos/o/r/issues"), True),
    ("reviewer", bash("gh api -XPATCH repos/o/r -fvisibility=public"), True),
    ("reviewer", bash("gh api --method DELETE repos/o/r"), True),
    ("reviewer", bash("gh api -X GET repos/o/r"), False),
    ("reviewer", bash("gh api repos/o/r/pulls -H 'Accept: application/json' -q .[0].title"), False),
    ("backend", bash("bash -lc 'curl x'"), True),
    ("backend", bash("python3 -Sc 'print(1)'"), True),
    ("backend", bash("command -p curl x"), True),
    ("backend", bash("timeout 5 curl x"), True),
    ("backend", bash("nice -n 10 curl x"), True),
    ("backend", bash("cat .e''nv"), True),
    ("backend", bash('cat .en"v"'), True),
    # GitHub: reads open, anything that merges, deletes or writes remotely closed
    ("backend", bash("gh pr view 1 --json state"), False),
    ("backend", bash("gh search issues foo"), False),
    ("backend", bash("gh release view v1"), False),
    ("backend", bash("gh pr merge 1"), True),
    ("backend", bash("gh repo delete o/r --yes"), True),
    ("backend", bash("gh release delete v1"), True),
    ("backend", bash("gh issue comment 1 -b x"), True),
    ("backend", bash("git push origin --delete old"), True),
    # .git and tool-name spelling
    ("backend", write(".git/config"), True),
    ("backend", write(".git/hooks/pre-commit"), True),
    ("backend", {"tool_name": "bash", "tool_input": {"command": "git push"}}, True),
    ("backend", {"tool_name": "create", "tool_input": {"path": "../x", "file_text": "x"}}, True),
    ("architect", {"tool_name": "edit", "tool_input": {"path": "a", "old_str": "a", "new_str": "b"}}, True),
    ("backend", {"tool_name": "bash", "tool_input": {"command": 5}}, True),
    ("backend", {"tool_name": "Read", "tool_input": {"path": 5}}, True),
    ("backend", {"tool_name": "Read", "tool_input": "x"}, True),
    ("gandalf", {"tool_name": "task", "tool_input": {"agent_type": "general-purpose"}}, True),
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "https://2130706433/"}}, True),
    ("analyst", {"tool_name": "WebFetch", "tool_input": {"url": "https://[::ffff:127.0.0.1]/"}}, True),
]


class GuardTest(unittest.TestCase):
    def test_cases(self):
        for role, event, denied in CASES:
            event = {**event, "cwd": CWD}
            with self.subTest(role=role, event=event):
                reason = guard.check(role, event)
                self.assertEqual(reason is not None, denied, reason)

    def test_every_role_has_a_class(self):
        self.assertEqual(len(guard.ROLES), 21)

    def test_call_budget(self):
        d = tempfile.mkdtemp()
        results = [guard.over_budget("backend", "s1", d) for _ in range(guard.MAX_CALLS + 1)]
        self.assertFalse(any(results[:-1]))
        self.assertTrue(results[-1])
        self.assertFalse(guard.over_budget("backend", "s2", d))
        self.assertFalse(guard.over_budget("backend", "a/b", d) or guard.over_budget("backend", "a_b", d))

    def test_missing_session_id_is_denied(self):
        event = {**bash("ls"), "cwd": CWD}
        self.assertIn("session_id", guard.decide("backend", event, tempfile.mkdtemp()))
        self.assertIsNone(guard.decide("backend", {**event, "session_id": "s"}, tempfile.mkdtemp()))

    def test_repeated_denials_halt_the_role(self):
        d, event = tempfile.mkdtemp(), {**bash("git push"), "cwd": CWD, "session_id": "s"}
        for _ in range(guard.MAX_DENIALS):
            self.assertIn("git", guard.decide("backend", event, d))
        self.assertIn("halted", guard.decide("backend", {**bash("ls"), "cwd": CWD, "session_id": "s"}, d))
        self.assertIsNone(guard.decide("backend", {**bash("ls"), "cwd": CWD, "session_id": "other"}, d))
        self.assertIsNone(guard.decide("qa", {**bash("ls"), "cwd": CWD, "session_id": "s"}, d))

    def test_stop_file_halts_everyone(self):
        d = tempfile.mkdtemp()
        open(os.path.join(d, "STOP"), "w").close()
        self.assertIn("STOP", guard.decide("qa", {**bash("ls"), "cwd": CWD, "session_id": "s"}, d))

    def test_bad_payload_is_denied_not_crashed(self):
        for stdin in ("", "null", "[]", "{not json"):
            r = subprocess.run([sys.executable, GUARD, "backend"], input=stdin, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertIn('"deny"', r.stdout)

    def test_unknown_role_is_denied(self):
        r = subprocess.run([sys.executable, GUARD, "nobody"],
                           input=json.dumps({**bash("ls"), "session_id": "s"}), capture_output=True, text=True)
        self.assertIn('"deny"', r.stdout)


if __name__ == "__main__":
    os.chdir(CWD)
    unittest.main()
