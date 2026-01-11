#!/usr/bin/env python3

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GlobalOlaf:
    @property
    def root(self) -> Path:
        return Path.home() / ".olaf"

    @property
    def core(self) -> Path:
        return self.root / "core"

    @property
    def competencies(self) -> Path:
        return self.core / "competencies"

    @property
    def skills(self) -> Path:
        return self.core / "skills"


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _read_text_sanitized(path: Path) -> str:
    raw = path.read_bytes().replace(b"\x00", b"")
    return raw.decode("utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(_read_text_sanitized(path))
    except FileNotFoundError as ex:
        raise RuntimeError(f"Missing JSON file: {path}") from ex
    except json.JSONDecodeError as ex:
        raise RuntimeError(f"Invalid JSON in file: {path} ({ex})") from ex


def copytree_overwrite(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Backup global ~/.olaf my-competencies and its skills into ~/.olaf-backup"
    )
    parser.add_argument(
        "--backup-root",
        default=str(Path.home() / ".olaf-backup"),
        help="Backup root directory (default: ~/.olaf-backup)",
    )
    parser.add_argument(
        "--label",
        default=None,
        help="Optional backup label (default: timestamp)",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )

    args = parser.parse_args()

    olaf = GlobalOlaf()
    comp_dir = olaf.competencies / "my-competencies"
    manifest_path = comp_dir / "competency-manifest.json"

    if not manifest_path.exists():
        raise RuntimeError(f"my-competencies manifest not found: {manifest_path}")

    manifest = read_json(manifest_path)

    skill_ids: set[str] = set()
    bom = manifest.get("bom")
    if isinstance(bom, dict):
        skills = bom.get("skills")
        if isinstance(skills, list):
            for s in skills:
                if isinstance(s, str) and s:
                    skill_ids.add(s)

    label = args.label or datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = Path(args.backup_root).expanduser().resolve()
    backup_dir = backup_root / label

    if backup_dir.exists() and not args.yes:
        ans = input(f"Backup path exists: {backup_dir}. Overwrite? [y/N]: ").strip().lower()
        if ans not in {"y", "yes"}:
            raise RuntimeError("Aborted by user")

    # Backup competency
    copytree_overwrite(comp_dir, backup_dir / "core" / "competencies" / "my-competencies")

    # Backup skills referenced by competency
    for sid in sorted(skill_ids):
        src_skill = olaf.skills / sid
        if not src_skill.exists() or not src_skill.is_dir():
            print(f"⚠️  Skill directory missing, skipping: {src_skill}")
            continue
        copytree_overwrite(src_skill, backup_dir / "core" / "skills" / sid)

    # Write a small metadata file for humans/tools
    meta = {
        "created": datetime.now().isoformat(),
        "source": str(olaf.root),
        "competency": "my-competencies",
        "skills": sorted(skill_ids),
    }
    (backup_dir).mkdir(parents=True, exist_ok=True)
    (backup_dir / "backup-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(f"✓ Backup created: {backup_dir}")
    print(f"  Competency: my-competencies")
    print(f"  Skills backed up: {len(skill_ids)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as ex:
        eprint(f"❌ {ex}")
        raise SystemExit(1)
