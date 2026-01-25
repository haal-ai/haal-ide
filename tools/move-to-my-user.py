#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
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
        return self.repo_root / "skills"

    @property
    def local_reference_dir(self) -> Path:
        return self.repo_root / "reference"

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


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
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


def copy_or_move_dir(src: Path, dst: Path, *, move: bool, overwrite: bool) -> None:
    if not src.exists() or not src.is_dir():
        raise RuntimeError(f"Local skill directory not found: {src}")

    if dst.exists():
        if not overwrite:
            raise RuntimeError(f"Global destination already exists: {dst} (use --overwrite)")
        shutil.rmtree(dst)

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)

    if move:
        shutil.rmtree(src)


def ensure_my_competencies_manifest(*, paths: OlafPaths, skill_id: str) -> Path:
    competency_id = "my-competencies"
    comp_dir = paths.global_competencies_dir / competency_id
    manifest_path = comp_dir / "competency-manifest.json"

    if manifest_path.exists():
        manifest = read_json(manifest_path)
    else:
        today = date.today().isoformat()
        manifest = {
            "metadata": {
                "id": competency_id,
                "name": "My Competencies",
                "shortDescription": "User-maintained competency that aggregates personal skills.",
                "description": "Personal competency package intended to hold user-created skills.",
                "version": "1.0.0",
                "objectives": ["Group personal skills", "Expose personal skills via the OLAF competency index"],
                "tags": ["user", "personal"],
                "author": "User",
                "status": "experimental",
                "exposure": "internal",
                "created": today,
                "updated": today,
            },
            "bom": {
                "skills": [],
                "entry_points": [],
            },
        }

    bom = manifest.setdefault("bom", {})
    skills = bom.setdefault("skills", [])
    if skill_id not in skills:
        skills.append(skill_id)

    entry_points = bom.setdefault("entry_points", [])
    if not any(isinstance(ep, dict) and ep.get("id") == skill_id for ep in entry_points):
        entry_points.append({"id": skill_id, "manifest": f"skills/{skill_id}/skill-manifest.json", "location": "global"})

    metadata = manifest.setdefault("metadata", {})
    metadata["updated"] = date.today().isoformat()

    write_json(manifest_path, manifest)
    return manifest_path


def add_competency_to_active_collection(*, collections_file: Path) -> str:
    competency_id = "my-competencies"
    collections = read_json(collections_file)

    active = collections.get("metadata", {}).get("active_collection")
    if not isinstance(active, str) or not active:
        raise RuntimeError(f"Missing metadata.active_collection in {collections_file}")

    target = None
    for c in collections.get("collections", []):
        if isinstance(c, dict) and c.get("id") == active:
            target = c
            break

    if target is None:
        raise RuntimeError(f"Active collection '{active}' not found in {collections_file}")

    comps = target.setdefault("competencies", [])
    if not isinstance(comps, list):
        raise RuntimeError(f"Invalid competencies list for collection '{active}'")

    if competency_id not in comps:
        comps.append(competency_id)

    write_json(collections_file, collections)
    return active


def run_select_collection(*, paths: OlafPaths, collection_id: str, reinit: bool) -> None:
    script = paths.repo_root / "tools" / "select-collection.py"
    if not script.exists():
        raise RuntimeError(f"Missing select-collection tool: {script}")

    cmd = [sys.executable, str(script), "--collection", collection_id, "--local-root", str(paths.repo_root)]
    if reinit:
        cmd.append("--reinit")

    subprocess.run(cmd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Move/copy a repo-local OLAF skill to the global ~/.olaf install and register it under my-competencies."
    )
    parser.add_argument("--repo-root", required=True, help="Path to the git repo root containing the local .olaf folder")
    parser.add_argument("--skill-id", required=True, help="Skill folder name under skills/ (kebab-case)")
    parser.add_argument("--move", action="store_true", help="Move (delete local) after copying. Default is copy only.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing global skill folder if present")
    parser.add_argument("--reinit", action="store_true", help="Also regenerate /olaf-* commands after reindex")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")

    args = parser.parse_args()

    paths = OlafPaths(repo_root=Path(args.repo_root).resolve())
    skill_id = args.skill_id.strip()

    local_skill_dir = paths.local_skills_dir / skill_id
    global_skill_dir = paths.global_skills_dir / skill_id

    if not paths.local_collections_file.exists():
        raise RuntimeError(f"Missing local collections file: {paths.local_collections_file}")

    action = "MOVE" if args.move else "COPY"
    confirm_or_exit(
        f"{action} skill '{skill_id}'\n  From: {local_skill_dir}\n  To:   {global_skill_dir}\nProceed?",
        assume_yes=args.yes,
    )

    copy_or_move_dir(local_skill_dir, global_skill_dir, move=args.move, overwrite=args.overwrite)
    print(f"✓ Skill {action.lower()} complete")

    manifest_path = ensure_my_competencies_manifest(paths=paths, skill_id=skill_id)
    print(f"✓ Updated global competency manifest: {manifest_path}")

    active_collection = add_competency_to_active_collection(collections_file=paths.local_collections_file)
    print(f"✓ Ensured my-competencies in active collection '{active_collection}'")

    confirm_or_exit(f"Regenerate competency index for collection '{active_collection}' now?", assume_yes=args.yes)

    run_select_collection(paths=paths, collection_id=active_collection, reinit=args.reinit)
    print("✓ Reindex complete")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as ex:
        eprint(f"❌ {ex}")
        raise SystemExit(1)
