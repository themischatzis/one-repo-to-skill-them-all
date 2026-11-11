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
OPENAI_KEY = "s" + "k-" + "A" * 24


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def write(path, text="x", tool="Write"):
    return {"tool_name": tool, "tool_input": {"path": path, "file_text": text}}


def read(path):
    return {"tool_name": "Read", "tool_input": {"path": path}}


def web(url):
    return {"tool_name": "WebFetch", "tool_input": {"url": url}}


def agent(agent_type=None):
    return {"tool_name": "Agent", "tool_input": {"prompt": "x", **({"agent_type": agent_type} if agent_type else {})}}


# (role, event, expected) where expected is None (allowed), "deny" or "ask"
CASES = [
    # merge: denied for roles, asks Themis for Gandalf
    ("backend", bash("git merge other"), "deny"),
    ("backend", bash("git status; git merge other"), "deny"),
    ("backend", bash("git -C . merge other"), "deny"),
    ("backend", bash("gh pr merge 12"), "deny"),
    ("backend", bash("gh -R o/r pr merge 12 --squash"), "deny"),
    ("backend", bash("env FOO=1 gh pr merge 12"), "deny"),
    ("backend", bash("gh api -X PUT repos/o/r/pulls/12/merge"), "deny"),
    ("backend", bash("gh api graphql -f query='mutation { mergePullRequest(input: {}) { clientMutationId } }'"), "deny"),
    ("reviewer", bash("gh pr merge 12"), "deny"),
    ("gandalf", bash("git merge main"), "ask"),
    ("gandalf", bash("gh pr merge 1"), "ask"),
    ("gandalf", bash("gh api -X PUT repos/o/r/pulls/12/merge"), "ask"),
    # everything else in git and GitHub is open
    ("backend", bash("git commit -m x"), None),
    ("backend", bash("git push origin main"), None),
    ("backend", bash("git rebase main"), None),
    ("backend", bash("git merge-base main HEAD"), None),
    ("backend", bash("gh pr create --title x"), None),
    ("backend", bash("gh pr view 12"), None),
    ("reviewer", bash("gh api -X POST repos/o/r/issues"), None),
    # sudo is denied, other sensitive commands ask
    ("backend", bash("sudo ls"), "deny"),
    ("gandalf", bash("sudo ls"), "deny"),
    ("backend", bash("ls && sudo rm x"), "deny"),
    ("backend", bash("timeout 5 sudo ls"), "deny"),
    ("backend", bash("curl https://example.com"), "ask"),
    ("backend", bash("wget https://example.com"), "ask"),
    ("backend", bash("ssh host"), "ask"),
    ("backend", bash("aws s3 ls"), "ask"),
    ("backend", bash("wp plugin list"), "ask"),
    ("backend", bash("ls | xargs rm"), "ask"),
    ("backend", bash("npm publish"), "ask"),
    ("devops", bash("terraform apply -auto-approve"), "ask"),
    ("devops", bash("kubectl delete pod x"), "ask"),
    ("devops", bash("docker push img"), "ask"),
    ("gandalf", bash("curl https://x.y"), "ask"),
    ("backend", bash("npm test && npm run build"), None),
    ("devops", bash("terraform plan"), None),
    ("backend", bash("python3 -c 'print(1)'"), None),
    ("backend", bash("rm -rf build"), None),
    ("architect", bash("ls"), None),
    ("reviewer", write("/tmp/a.md"), None),
    ("qa", write("src/app.ts"), None),
    # secrets: paths, commands, env, token-shaped content
    ("backend", read(".env"), "deny"),
    ("backend", read(".env.local"), "deny"),
    ("backend", read(".env.example"), None),
    ("backend", read("~/.ssh/id_rsa"), "deny"),
    ("backend", read("~/.aws/credentials"), "deny"),
    ("backend", read("certs/server.pem"), "deny"),
    ("backend", read("~/.copilot/config.json"), "deny"),
    ("backend", read("~/.copilot/skills/ground-rules/SKILL.md"), None),
    ("backend", write("~/.copilot/agents/backend.agent.md"), "deny"),
    ("backend", write(".env"), "deny"),
    ("backend", bash("cat .env"), "deny"),
    ("backend", bash("cat < .env"), "deny"),
    ("backend", bash("cp .env /tmp/x"), "deny"),
    ("backend", bash("echo hi > .env"), "deny"),
    ("backend", bash("echo hi > out.txt"), None),
    ("backend", bash("echo hi > /dev/null"), None),
    ("backend", bash("cat .e''nv"), "deny"),
    ("backend", bash("printenv"), "deny"),
    ("backend", bash("env"), "deny"),
    ("backend", bash("echo $GITHUB_TOKEN"), "deny"),
    ("backend", bash("cat ~/.copilot/settings.json"), "deny"),
    ("backend", write("notes.md", "key " + GH_TOKEN), "deny"),
    ("backend", write("notes.md", AWS_KEY), "deny"),
    ("backend", write("notes.md", PEM), "deny"),
    ("backend", bash("echo " + GH_TOKEN), "deny"),
    ("backend", bash("echo " + OPENAI_KEY), "deny"),
    # shell shapes the parser cannot check
    ("backend", bash("ls `whoami`"), "deny"),
    ("backend", bash("git status\ngit merge x"), "deny"),
    ("backend", bash("cat <<EOF\nhi\nEOF"), "deny"),
    ("backend", bash("ls <(git merge x)"), "deny"),
    # web and subagents
    ("analyst", web("https://example.com/a"), None),
    ("analyst", web("http://example.com"), "deny"),
    ("analyst", web("https://127.0.0.1/x"), "deny"),
    ("analyst", web("https://u:p@example.com"), "deny"),
    ("analyst", web("https://2130706433/"), "deny"),
    ("analyst", web("https://[::ffff:127.0.0.1]/"), "deny"),
    ("backend", web("https://example.com"), "deny"),
    ("backend", agent(), "deny"),
    ("backend", agent("sam"), "deny"),
    ("gandalf", agent("backend"), None),
    ("gandalf", agent("sam"), None),
    ("gandalf", agent("gollum"), None),
    ("gandalf", agent("general-purpose"), None),
    ("gandalf", agent("explore"), None),
    ("gandalf", agent(), None),
    # tool-name spelling and malformed payloads
    ("backend", {"tool_name": "bash", "tool_input": {"command": "git merge x"}}, "deny"),
    ("backend", {"tool_name": "bash", "tool_input": {"command": 5}}, "deny"),
    ("backend", {"tool_name": "Read", "tool_input": {"path": 5}}, "deny"),
    ("backend", {"tool_name": "Read", "tool_input": "x"}, "deny"),
    ("nobody", bash("ls"), "deny"),
]


def kind(reason):
    return None if reason is None else "ask" if reason.startswith(guard.ASK) else "deny"


class GuardTest(unittest.TestCase):
    def test_cases(self):
        for role, event, expected in CASES:
            event = {**event, "cwd": CWD}
            with self.subTest(role=role, event=event):
                reason = guard.check(role, event)
                self.assertEqual(kind(reason), expected, reason)

    def test_ask_reaches_copilot_as_a_prompt(self):
        out = subprocess.run([sys.executable, GUARD, "gandalf"], capture_output=True, text=True,
                             input=json.dumps({**bash("git merge main"), "cwd": CWD, "session_id": "ask-test"})).stdout
        self.assertEqual(json.loads(out)["permissionDecision"], "ask")

    def test_every_role_is_known(self):
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
        d, event = tempfile.mkdtemp(), {**bash("sudo ls"), "cwd": CWD, "session_id": "s"}
        for _ in range(guard.MAX_DENIALS):
            self.assertIn("sudo", guard.decide("backend", event, d))
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
