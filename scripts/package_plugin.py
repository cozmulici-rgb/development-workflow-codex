#!/usr/bin/env python3
"""Build a distributable archive for the local Codex plugin repo."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
PLUGIN_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
INCLUDE_PATHS = (
    Path(".codex-plugin"),
    Path(".agents"),
    Path("docs"),
    Path("skills"),
    Path("LICENSE"),
    Path("README.md"),
    Path("AGENTS.md"),
)


def main() -> int:
    validate_cmd = [sys.executable, str(ROOT / "scripts" / "validate_repo.py")]
    result = subprocess.run(validate_cmd, cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    manifest = json.loads(PLUGIN_MANIFEST.read_text(encoding="utf-8"))
    archive_stem = f"{manifest['name']}-{manifest['version']}"
    staging_dir = DIST_DIR / archive_stem
    archive_path = DIST_DIR / f"{archive_stem}.zip"

    if staging_dir.exists():
        shutil.rmtree(staging_dir)

    DIST_DIR.mkdir(exist_ok=True)
    staging_dir.mkdir()

    for relative_path in INCLUDE_PATHS:
        source = ROOT / relative_path
        destination = staging_dir / relative_path
        if source.is_dir():
            shutil.copytree(
                source,
                destination,
                ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"),
            )
        elif source.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)

    if archive_path.exists():
        archive_path.unlink()

    built_archive = shutil.make_archive(
        str(DIST_DIR / archive_stem),
        "zip",
        root_dir=DIST_DIR,
        base_dir=archive_stem,
    )
    shutil.rmtree(staging_dir)

    print(f"Created {Path(built_archive).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
