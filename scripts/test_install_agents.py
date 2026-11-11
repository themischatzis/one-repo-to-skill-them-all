"""Run with: python3 scripts/test_install_agents.py"""
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "checkout"
        self.home = Path(self.tmp.name) / "home" / ".copilot"
        self.root.mkdir()
        self.home.mkdir(parents=True)
        for directory in ("agents", "roles", "guard"):
            shutil.copytree(REPO / directory, self.root / directory)
        shutil.copyfile(REPO / "copilot-instructions.md", self.root / "copilot-instructions.md")
        self.install = runpy.run_path(str(REPO / "scripts/install-agents.py"))["install"]

    def test_checkout_changes_do_not_change_installed_agents_or_guard(self):
        (self.home / "agents").mkdir()
        source = self.root / "agents/gandalf/gandalf.agent.md"
        agent = self.home / "agents/gandalf.agent.md"
        agent.symlink_to(source)
        (self.home / "guard").symlink_to(self.root / "guard", target_is_directory=True)
        routing = self.home / "copilot-instructions.md"
        routing.symlink_to(self.root / "copilot-instructions.md")
        self.install(self.root, self.home)
        before = [p.read_bytes() for p in (agent, self.home / "guard/guard.py", routing)]
        source.write_text(source.read_text().replace("description:", 'tools: ["read"]\ndescription:', 1))
        (self.root / "guard/guard.py").write_text("raise RuntimeError('old checkout')")
        (self.root / "copilot-instructions.md").write_text("old routing")
        self.assertEqual(before, [p.read_bytes() for p in (agent, self.home / "guard/guard.py", routing)])
        self.assertFalse(any(p.is_symlink() for p in (agent, self.home / "guard", routing)))
        hook = next(line.strip().removeprefix("command: ") for line in agent.read_text().splitlines()
                    if line.strip().startswith("command: "))
        env = {**os.environ, "HOME": str(self.home.parent), "TMPDIR": self.tmp.name}
        for role, tool, args, expected in (
            ("gandalf", "atlassian-getJiraIssue", {"issueIdOrKey": "TEST-1"}, None),
            ("backend", "bash", {"command": "gh pr merge 1"}, "deny"),
            ("gandalf", "bash", {"command": "gh pr merge 1"}, "ask"),
            ("gandalf", "task", {"agent_type": "backend"}, None),
            ("gandalf", "task", {"agent_type": "explore", "name": "backend"}, None),
            ("backend", "write_agent", {"agent_id": "peer", "message": "API result"}, None),
            ("sam", "apply_patch", "*** Begin Patch\n*** Update File: tests/a.py\n@@\n-a\n+b\n*** End Patch\n", None),
            ("sam", "Edit", "*** Begin Patch\n*** Update File: tests/a.py\n@@\n-a\n+b\n*** End Patch\n", None),
        ):
            with self.subTest(role=role, tool=tool):
                event = {"tool_name": tool, "tool_input": args, "session_id": "install-test", "cwd": str(self.root)}
                result = subprocess.run(["bash", "-c", hook.removesuffix("gandalf") + role],
                                        input=json.dumps(event), capture_output=True, text=True, env=env, check=True)
                self.assertEqual(json.loads(result.stdout)["permissionDecision"] if result.stdout else None, expected)

    def test_reinstall_publishes_intentional_updates_and_preserves_other_files(self):
        self.install(self.root, self.home)
        unrelated = self.home / "agents/other.agent.md"
        unrelated.write_text("keep me")
        source = self.root / "agents/gandalf/gandalf.agent.md"
        source.write_text(source.read_text() + "\nUpdated brief.\n")
        self.install(self.root, self.home)
        self.assertEqual(source.read_bytes(), (self.home / "agents/gandalf.agent.md").read_bytes())
        self.assertEqual(unrelated.read_text(), "keep me")

    def test_invalid_candidate_does_not_replace_installed_version(self):
        self.install(self.root, self.home)
        installed = self.home / "agents/gandalf.agent.md"
        before = installed.read_bytes()
        source = self.root / "roles/backend/backend.agent.md"
        valid = source.read_text()
        for invalid in (valid.replace("description:", 'tools: ["read"]\ndescription:', 1),
                        valid.replace('guard.py" backend', 'guard.py" backned'),
                        valid.replace('guard.py" backend', 'guard.py" backend-extra'),
                        valid.replace("PreToolUse:", "PostToolUse:")):
            with self.subTest(candidate=invalid):
                source.write_text(invalid)
                with self.assertRaises(ValueError):
                    self.install(self.root, self.home)
                self.assertEqual(installed.read_bytes(), before)

    def test_foreign_symlinks_are_refused_before_installing(self):
        foreign = Path(self.tmp.name) / "foreign"
        foreign.mkdir()
        for target in (self.home / "agents", self.home / "guard", self.home / "copilot-instructions.md"):
            with self.subTest(target=target):
                target.symlink_to(foreign, target_is_directory=True)
                with self.assertRaises(ValueError):
                    self.install(self.root, self.home)
                self.assertTrue(target.is_symlink())
                self.assertEqual(list(foreign.iterdir()), [])
                target.unlink()
        (self.home / "agents").mkdir()
        agent = self.home / "agents/gandalf.agent.md"
        agent.symlink_to(foreign / "gandalf.agent.md")
        with self.assertRaises(ValueError):
            self.install(self.root, self.home)
        self.assertTrue(agent.is_symlink())


if __name__ == "__main__":
    unittest.main()
