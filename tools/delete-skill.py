#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class OlafPaths:
    repo_root: Path

    @property
    def local_olaf_dir(self) -> Path:
        return self.repo_root / ".olaf"

    @property
    def local_core_dir(self) -> Path:
        return self.repo_root

    @property
    def local_skills_dir(self) -> Path:
        return self.local_core_dir / "skills"

    @property
    def local_competencies_dir(self) -> Path:
        return self.local_core_dir / "competencies"

    @property
    def local_reference_dir(self) -> Path:
        return self.local_core_dir / "reference"

    @property
    def local_collections_file(self) -> Path:
        return self.local_reference_dir / "competency-collections.json"

    @property
    def global_olaf_dir(self) -> Path:
        return Path.home() / ".olaf"

    @property
    def global_core_dir(self) -> Path:
        return self.global_olaf_dir

    @property
    def global_skills_dir(self) -> Path:
        return self.global_core_dir / "skills"

    @property
    def global_competencies_dir(self) -> Path:
        return self.global_core_dir / "competencies"


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def _read_text_sanitized(path: Path) -> str:
    data = path.read_bytes()
    # Some files in this repo appear to contain null bytes.
    # This keeps JSON parsing tolerant while still preserving the content structure.
    data = data.replace(b"\x00", b"")
    return data.decode("utf-8", errors="replace")


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(_read_text_sanitized(path))
    except FileNotFoundError as ex:
        raise RuntimeError(f"Missing JSON file: {path}") from ex
    except json.JSONDecodeError as ex:
        raise RuntimeError(f"Invalid JSON in file: {path} ({ex})") from ex


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def confirm_or_exit(prompt: str, *, assume_yes: bool) -> None:
    if assume_yes:
        return
    ans = input(f"{prompt} [y/N]: ").strip().lower()
    if ans not in {"y", "yes"}:
        raise RuntimeError("Aborted by user")


def remove_from_competency_manifest(manifest_path: Path, skill_id: str) -> bool:
    if not manifest_path.exists():
        return False

    manifest = read_json(manifest_path)
    changed = False

    bom = manifest.get("bom")
    if isinstance(bom, dict):
        skills = bom.get("skills")
        if isinstance(skills, list) and skill_id in skills:
            bom["skills"] = [s for s in skills if s != skill_id]
            changed = True

        entry_points = bom.get("entry_points")
        if isinstance(entry_points, list):
            new_eps = []
            for ep in entry_points:
                if isinstance(ep, dict) and ep.get("id") == skill_id:
                    changed = True
                    continue
                new_eps.append(ep)
            bom["entry_points"] = new_eps

    if changed:
        write_json(manifest_path, manifest)

    return changed


def run_select_collection(*, paths: OlafPaths, reinit: bool) -> None:
    if not paths.local_collections_file.exists():
        raise RuntimeError(f"Missing local collections file: {paths.local_collections_file}")

    collections = read_json(paths.local_collections_file)
    active = collections.get("metadata", {}).get("active_collection")
    if not isinstance(active, str) or not active:
        raise RuntimeError(f"Missing metadata.active_collection in {paths.local_collections_file}")

    script = paths.repo_root / "tools" / "select-collection.py"
    if not script.exists():
        raise RuntimeError(f"Missing select-collection tool: {script}")

    cmd = [sys.executable, str(script), "--collection", active, "--local-root", str(paths.repo_root)]
    if reinit:
        cmd.append("--reinit")

    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Delete an OLAF skill (local repo or global user install) and remove references from the owning competency manifest."
    )
    parser.add_argument("--repo-root", required=True, help="Path to the git repo root containing the local .olaf folder")
    parser.add_argument("--skill-id", required=True, help="Skill folder name under skills/ (kebab-case)")

    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--local", action="store_true", help="Delete from repo-local .olaf and update team-competencies manifest")
    scope.add_argument("--global", action="store_true", help="Delete from user ~/.olaf and update my-competencies manifest")

    parser.add_argument("--reindex", action="store_true", help="Regenerate query-competency-index.md after changes")
    parser.add_argument("--reinit", action="store_true", help="With --reindex: also regenerate /olaf-* commands")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")

    args = parser.parse_args()

    paths = OlafPaths(repo_root=Path(args.repo_root).resolve())
    skill_id = args.skill_id.strip()

    if args.local:
        skill_dir = paths.local_skills_dir / skill_id
        manifest_path = paths.local_competencies_dir / "team-competencies" / "competency-manifest.json"
        where = "LOCAL"
    else:
        skill_dir = paths.global_skills_dir / skill_id
        manifest_path = paths.global_competencies_dir / "my-competencies" / "competency-manifest.json"
        where = "GLOBAL"

    confirm_or_exit(
        f"Delete {where} skill '{skill_id}'\n  Skill dir: {skill_dir}\n  Update manifest: {manifest_path}\nProceed?",
        assume_yes=args.yes,
    )

    if skill_dir.exists():
        shutil.rmtree(skill_dir)
        print(f"✓ Deleted skill directory: {skill_dir}")
    else:
        print(f"ℹ️  Skill directory not found (already deleted?): {skill_dir}")

    changed = remove_from_competency_manifest(manifest_path, skill_id)
    if changed:
        print(f"✓ Removed '{skill_id}' from manifest: {manifest_path}")
    else:
        print(f"ℹ️  No manifest update needed: {manifest_path}")

    if args.reindex:
        run_select_collection(paths=paths, reinit=args.reinit)
        print("✓ Reindex complete")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as ex:
        eprint(f"❌ {ex}")
        raise SystemExit(1)
