#!/usr/bin/env python3
"""Publish agents, their guard and routing as copies, independent of git checkouts."""
import os
from pathlib import Path
import re
import runpy
import sys
import tempfile


def install(repo, home):
    repo, home = Path(repo).resolve(), Path(home).absolute()
    if home.is_symlink() or home.resolve().is_relative_to(repo):
        raise ValueError("installation must be outside the checkout, in a real directory")
    agents = sorted([*repo.glob("agents/*/*.agent.md"), *repo.glob("roles/*/*.agent.md")])
    roles = runpy.run_path(str(repo / "guard/guard.py"))["ROLES"]
    names = [p.name.removesuffix(".agent.md") for p in agents]
    if len(names) != len(set(names)) or set(names) != set(roles):
        raise ValueError("agent files must match the guard's ROLES")
    files = []
    for source, role in zip(agents, names):
        text = source.read_text()
        header = text.split("---", 2)[1] if text.startswith("---\n") else ""
        hook = f'command: python3 "$HOME/.copilot/guard/guard.py" {role}'
        hook_block = "hooks:\n  PreToolUse:\n    - type: command\n      " + hook + "\n      timeoutSec: 10"
        if (re.search(r"(?m)^tools\s*:", header)
                or not re.search(rf"(?m)^name: {re.escape(role)}$", header)
                or not re.search(rf"(?m)^{re.escape(hook_block)}$", header)):
            raise ValueError(f"{source}: omit tools and keep the matching name and guard hook")
        files.append((source, home / "agents" / source.name, text.encode()))
    for relative in ("guard/guard.py", "copilot-instructions.md"):
        source = repo / relative
        files.append((source, home / relative, source.read_bytes()))
    for directory in (home / "agents", home / "guard"):
        if directory.is_symlink():
            if directory != home / "guard" or directory.resolve() != repo / "guard":
                raise ValueError(f"refusing foreign directory symlink: {directory}")
        elif directory.exists() and not directory.is_dir():
            raise ValueError(f"not a directory: {directory}")
    for source, target, _ in files:
        if target.is_symlink() and target.resolve() != source:
            raise ValueError(f"refusing foreign file symlink: {target}")
        if target.exists() and not target.is_file():
            raise ValueError(f"not a file: {target}")
    if (home / "guard").is_symlink():
        (home / "guard").unlink()
    for _, target, data in files:
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(dir=target.parent, prefix=".install-")
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return len(agents)


if __name__ == "__main__":
    try:
        count = install(Path(__file__).resolve().parents[1], Path.home() / ".copilot")
    except (OSError, ValueError) as error:
        sys.exit(f"Installation refused: {error}")
    print(f"Installed {count} custom agents, guard and routing as stable copies. Restart Copilot CLI.")
