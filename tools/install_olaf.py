#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
import time
import json
import tempfile
from datetime import datetime
from pathlib import Path


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def run(cmd: list[str], *, cwd: Path | None = None, quiet: bool = False) -> None:
    try:
        subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            check=True,
            stdout=subprocess.DEVNULL if quiet else None,
            stderr=subprocess.DEVNULL if quiet else None,
        )
    except FileNotFoundError:
        raise
    except subprocess.CalledProcessError as ex:
        raise RuntimeError(f"Command failed ({ex.returncode}): {' '.join(cmd)}") from ex


def _pick_collection_id_from_file(collections_file: Path) -> str | None:
    if not collections_file.exists():
        return None

    try:
        collections = json.loads(collections_file.read_text(encoding="utf-8"))
    except Exception:
        return None

    available_ids: set[str] = set()
    for c in collections.get("collections", []):
        cid = c.get("id")
        if isinstance(cid, str) and cid:
            available_ids.add(cid)

    candidate = collections.get("metadata", {}).get("active_collection")
    if isinstance(candidate, str) and candidate in available_ids:
        return candidate
    if "core" in available_ids:
        return "core"
    if available_ids:
        return sorted(available_ids)[0]
    return None


def install_minimal_tools(target_dir: Path, clone_dir: Path) -> None:
    tools_dir = target_dir / "tools"
    tools_dir.mkdir(parents=True, exist_ok=True)

    # Install the installer itself
    shutil.copy2(Path(__file__), tools_dir / "install_olaf.py")

    # Install select-collection in a stable location
    local_select = Path(__file__).with_name("select-collection.py")
    if local_select.exists() and local_select.is_file():
        shutil.copy2(local_select, tools_dir / "select-collection.py")
    else:
        src_select = clone_dir / "skills" / "create-skill" / "scripts" / "select_collection.py"
        if src_select.exists() and src_select.is_file():
            shutil.copy2(src_select, tools_dir / "select-collection.py")


def ensure_global_my_competencies(target_dir: Path) -> Path:
    comp_dir = target_dir / "competencies" / "my-competencies"
    manifest_path = comp_dir / "competency-manifest.json"
    if manifest_path.exists():
        return manifest_path

    comp_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().date().isoformat()
    manifest = {
        "metadata": {
            "id": "my-competencies",
            "name": "My Competencies",
            "shortDescription": "User-maintained competency that aggregates personal skills.",
            "description": "Personal competency package intended to hold user-created skills.",
            "version": "1.0.0",
            "objectives": [
                "Group personal skills",
                "Expose personal skills via the OLAF competency index",
            ],
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
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest_path


def generate_query_competency_index(
    target_dir: Path,
    *,
    collection_id: str | None = None,
    local_root: Path | None = None,
) -> Path:
    # Ensure kernel/global user competency exists before index generation so it isn't pruned.
    ensure_global_my_competencies(target_dir)

    preferred = target_dir / "tools" / "select-collection.py"
    fallback = target_dir / "skills" / "create-skill" / "scripts" / "select_collection.py"
    script = preferred if preferred.exists() else fallback
    if not script.exists():
        raise RuntimeError(
            f"Missing select-collection tool in installed target. Expected one of: "
            f"{preferred} or {fallback}"
        )

    if not collection_id:
        collection_id = "core"

    if local_root is not None:
        output_path = local_root / "reference" / "query-competency-index.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = target_dir / "reference" / "query-competency-index.md"
    cmd = [sys.executable, str(script), "--collection", collection_id, "--output", str(output_path)]
    if local_root is not None:
        cmd.extend(["--local-root", str(local_root)])
    try:
        run(cmd, quiet=True)
    except RuntimeError:
        # Rerun with output visible to surface the underlying cause.
        # If the rerun succeeds and produces the expected file, do not treat as fatal.
        run(cmd, quiet=False)
    if not output_path.exists():
        raise RuntimeError(f"Competency index generation did not produce expected file: {output_path}")
    return output_path


def ensure_local_competency_collections(local_root: Path, target_dir: Path) -> Path:
    local_ref = local_root / "reference"
    local_ref.mkdir(parents=True, exist_ok=True)
    local_file = local_ref / "competency-collections.json"
    if local_file.exists():
        return local_file

    src = target_dir / "reference" / "competency-collections.json"
    if src.exists() and src.is_file():
        shutil.copy2(src, local_file)
    return local_file


def sync_global_active_collection_from_seed(*, clone_dir: Path, target_dir: Path) -> None:
    """Ensure global competency-collections active_collection follows the seed clone (seed wins)."""

    seed_file = clone_dir / "reference" / "competency-collections.json"
    target_file = target_dir / "reference" / "competency-collections.json"

    if not seed_file.exists() or not seed_file.is_file():
        return
    if not target_file.exists() or not target_file.is_file():
        return

    try:
        seed_data = json.load(open(seed_file, "r", encoding="utf-8"))
        target_data = json.load(open(target_file, "r", encoding="utf-8"))
    except Exception:
        return

    if not isinstance(seed_data, dict) or not isinstance(target_data, dict):
        return

    seed_meta = seed_data.get("metadata")
    if not isinstance(seed_meta, dict):
        return

    seed_active = seed_meta.get("active_collection")
    if not isinstance(seed_active, str) or not seed_active.strip():
        return
    seed_active = seed_active.strip()

    # Only apply if the seed's active collection exists in the target's collection list.
    target_collections = target_data.get("collections")
    if not isinstance(target_collections, list):
        return
    target_ids: set[str] = set()
    for c in target_collections:
        if isinstance(c, dict):
            cid = c.get("id")
            if isinstance(cid, str) and cid:
                target_ids.add(cid)
    if seed_active not in target_ids:
        return

    target_meta = target_data.get("metadata")
    if not isinstance(target_meta, dict):
        target_meta = {}
        target_data["metadata"] = target_meta

    if target_meta.get("active_collection") == seed_active:
        return

    target_meta["active_collection"] = seed_active
    target_meta["lastUpdated"] = datetime.now().isoformat()

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(target_data, f, indent=2)


def _load_competency_locations(collections_file: Path) -> dict[str, str]:
    try:
        data = json.load(open(collections_file, "r", encoding="utf-8"))
    except Exception:
        return {}

    locations = data.get("competency_locations")
    if not isinstance(locations, dict):
        return {}

    out: dict[str, str] = {}
    for k, v in locations.items():
        if isinstance(k, str) and isinstance(v, str):
            out[k] = v
    return out


def _registry_path_in_clone(clone_dir: Path) -> Path:
    # Prefer commit-friendly name (doesn't match olaf-* ignore patterns)
    preferred = clone_dir / "_olaf-registry.json"
    if preferred.exists() and preferred.is_file():
        return preferred
    # Backward compatibility
    return clone_dir / "olaf-registry.json"


def _load_prune_list_from_file(path: Path) -> tuple[set[str], set[str]]:
    """Load prune list from a JSON file.

    Expected format:
      {
        "skills": ["skill-id-1", "skill-id-2"],
        "competencies": ["comp-id-1", "comp-id-2"]
      }

    Returns (skills_to_prune, competencies_to_prune). Never raises.
    """

    if not path.exists() or not path.is_file():
        return set(), set()
    try:
        data = json.load(open(path, "r", encoding="utf-8"))
    except Exception:
        return set(), set()

    skills: set[str] = set()
    comps: set[str] = set()

    raw_skills = data.get("skills") if isinstance(data, dict) else None
    if isinstance(raw_skills, list):
        for s in raw_skills:
            if isinstance(s, str) and s.strip():
                skills.add(s.strip())

    raw_comps = data.get("competencies") if isinstance(data, dict) else None
    if isinstance(raw_comps, list):
        for c in raw_comps:
            if isinstance(c, str) and c.strip():
                comps.add(c.strip())

    return skills, comps


def _find_prune_list_file(*, clone_dir: Path, local_root: Path, explicit: str | None = None) -> Path | None:
    """Find the prune list file.

    Search order:
    1) Explicit CLI path (relative to local_root if not absolute)
    2) Seed clone: reference/olaf-prune-list.json
    3) Seed clone: reference/prune-list.json
    4) Local repo: reference/olaf-prune-list.json
    5) Local repo: reference/prune-list.json
    """

    candidates: list[Path] = []

    if isinstance(explicit, str) and explicit.strip():
        p = Path(explicit.strip())
        if not p.is_absolute():
            p = local_root / p
        candidates.append(p)

    candidates.extend(
        [
            clone_dir / "reference" / "olaf-prune-list.json",
            clone_dir / "reference" / "prune-list.json",
            local_root / "reference" / "olaf-prune-list.json",
            local_root / "reference" / "prune-list.json",
        ]
    )

    for c in candidates:
        if c.exists() and c.is_file():
            return c
    return None


def _find_prune_list_files_in_clone(clone_dir: Path) -> list[Path]:
    candidates = [
        clone_dir / "reference" / "olaf-prune-list.json",
        clone_dir / "reference" / "prune-list.json",
    ]
    return [p for p in candidates if p.exists() and p.is_file()]


def _collect_prune_lists(
    *,
    clone_dir: Path,
    secondary_clone_dirs: list[Path],
    local_root: Path,
    prune_file: str | None,
) -> tuple[set[str], set[str], list[Path]]:
    """Collect and merge prune lists from seed + secondaries (+ optional explicit/local).

    Merge strategy: union across all discovered prune list files.
    """

    sources: list[Path] = []

    # 1) Explicit
    if isinstance(prune_file, str) and prune_file.strip():
        p = Path(prune_file.strip())
        if not p.is_absolute():
            p = local_root / p
        if p.exists() and p.is_file():
            sources.append(p)

    # 2) Seed clone
    sources.extend(_find_prune_list_files_in_clone(clone_dir))

    # 3) Secondary clones
    for sec in secondary_clone_dirs:
        sources.extend(_find_prune_list_files_in_clone(sec))

    # 4) Local repo
    local_candidates = [
        local_root / "reference" / "olaf-prune-list.json",
        local_root / "reference" / "prune-list.json",
    ]
    sources.extend([p for p in local_candidates if p.exists() and p.is_file()])

    # Unique but preserve order
    unique_sources: list[Path] = []
    seen: set[str] = set()
    for s in sources:
        key = str(s).lower()
        if key in seen:
            continue
        seen.add(key)
        unique_sources.append(s)

    skills: set[str] = set()
    comps: set[str] = set()
    for src in unique_sources:
        s, c = _load_prune_list_from_file(src)
        skills |= s
        comps |= c

    return skills, comps, unique_sources


def apply_prune_list(
    *,
    target_dir: Path,
    clone_dir: Path,
    secondary_clone_dirs: list[Path],
    local_root: Path,
    enabled: bool,
    prune_file: str | None = None,
) -> None:
    """Delete explicitly listed skills/competencies from the installed global target.

    This is intentionally explicit (opt-in) and never deletes anything outside:
      - <target_dir>/skills/<id>
      - <target_dir>/competencies/<id>
    """

    if not enabled:
        print("Prune: disabled (--no-prune); skipping")
        return

    skills, comps, sources = _collect_prune_lists(
        clone_dir=clone_dir,
        secondary_clone_dirs=secondary_clone_dirs,
        local_root=local_root,
        prune_file=prune_file,
    )

    if not sources:
        print("Prune: enabled but no prune list files found (seed/secondaries/local); skipping")
        return

    print("Prune: sources:")
    for p in sources:
        print(f"- {p}")

    if not skills and not comps:
        print("Prune: merged list is empty; nothing to do")
        return

    if skills:
        print("Prune: skills to remove:")
        for s in sorted(skills):
            print(f"- {s}")
    if comps:
        print("Prune: competencies to remove:")
        for c in sorted(comps):
            print(f"- {c}")

    skills_dir = target_dir / "skills"
    comps_dir = target_dir / "competencies"

    for sid in sorted(skills):
        victim = skills_dir / sid
        if victim.exists() and victim.is_dir():
            print(f"Prune: removing skill {sid}")
            rmtree_if_exists(victim)
        else:
            print(f"Prune: skill not found (skip) {sid}")

    for cid in sorted(comps):
        victim = comps_dir / cid
        if victim.exists() and victim.is_dir():
            print(f"Prune: removing competency {cid}")
            rmtree_if_exists(victim)
        else:
            print(f"Prune: competency not found (skip) {cid}")


def load_registry_with_diagnostics(clone_dir: Path) -> tuple[list[tuple[str, str]], str]:
    """Load registry from seed clone only.

    Returns (entries, status_message).
    This function must never raise: a malformed registry should not fail install.
    """

    registry_path = _registry_path_in_clone(clone_dir)
    if not registry_path.exists() or not registry_path.is_file():
        return [], f"no registry file in seed clone ({registry_path})"

    try:
        data = json.load(open(registry_path, "r", encoding="utf-8"))
    except Exception:
        return [], f"registry file present but not valid JSON ({registry_path})"

    items = data.get("secondary-repos")
    if not isinstance(items, list):
        return [], f"registry file present but missing 'secondary-repos' list ({registry_path})"

    out: list[tuple[str, str]] = []
    for it in items:
        if not isinstance(it, str):
            continue
        try:
            out.append(parse_repo_branch(it))
        except ValueError:
            continue

    if not out:
        return [], f"registry file present but contains 0 valid secondary entries ({registry_path})"

    return out, f"seed registry ({registry_path})"


def copy_local_competencies_from_clone(clone_root: Path, local_root: Path, local_competency_ids: set[str]) -> None:
    if not local_competency_ids:
        return

    src_competencies = clone_root / "competencies"
    if not src_competencies.exists():
        raise RuntimeError(f"Missing expected competencies folder in clone: {src_competencies}")

    _ = ensure_local_olaf_skeleton(local_root)
    dest_competencies = local_root / "competencies"
    dest_competencies.mkdir(parents=True, exist_ok=True)

    for comp_id in sorted(local_competency_ids):
        src_dir = src_competencies / comp_id
        if not src_dir.exists() or not src_dir.is_dir():
            print(f"⚠️  Local competency not found in clone: {comp_id}")
            continue
        dst_dir = dest_competencies / comp_id
        rmtree_if_exists(dst_dir)
        dst_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_dir, dst_dir)


def sanitize_global_competency_collections(target_dir: Path) -> None:
    collections_file = target_dir / "reference" / "competency-collections.json"
    if not collections_file.exists():
        return

    try:
        data = json.load(open(collections_file, "r", encoding="utf-8"))
    except Exception:
        return

    collections = data.get("collections")
    if not isinstance(collections, list):
        return

    global_competencies_dir = target_dir / "competencies"

    def exists_globally(comp_id: str) -> bool:
        manifest = global_competencies_dir / comp_id / "competency-manifest.json"
        if manifest.exists():
            return True
        return (global_competencies_dir / comp_id).exists()

    # Normalize legacy IDs to current IDs.
    # Note: keep this conservative; anything not present globally will be removed afterwards.
    replacements: dict[str, str] = {
        "my-prompts": "team-competencies",
        "olaf-olaf-admin": "haal-admin",
        "olaf-admin": "haal-admin",
    }

    changed = False
    new_collections: list[dict] = []

    for coll in collections:
        if not isinstance(coll, dict):
            continue

        comps = coll.get("competencies")
        if not isinstance(comps, list):
            new_collections.append(coll)
            continue

        normalized: list[str] = []
        for c in comps:
            if not isinstance(c, str):
                continue
            normalized.append(replacements.get(c, c))

        filtered = [c for c in normalized if exists_globally(c)]
        if filtered != comps:
            changed = True
            coll["competencies"] = filtered

        # Drop empty collections (no competencies after filtering)
        if filtered:
            new_collections.append(coll)
        else:
            changed = True

    if not changed:
        return

    data["collections"] = new_collections
    meta = data.get("metadata")
    if not isinstance(meta, dict):
        meta = {}
        data["metadata"] = meta
    meta["lastUpdated"] = datetime.now().isoformat()

    with open(collections_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _read_json_sanitized(path: Path) -> dict:
    raw = path.read_bytes().replace(b"\x00", b"")
    return json.loads(raw.decode("utf-8", errors="replace"))


def preserve_my_competencies(target_dir: Path) -> tuple[Path | None, set[str]]:
    """Backup ~/.olaf/competencies/my-competencies and its referenced skills.

    Returns (backup_root, referenced_skill_ids). If nothing to preserve, returns (None, set()).
    """

    comp_dir = target_dir / "competencies" / "my-competencies"
    manifest_path = comp_dir / "competency-manifest.json"
    if not manifest_path.exists():
        return None, set()

    try:
        manifest = _read_json_sanitized(manifest_path)
    except Exception:
        manifest = {}

    skill_ids: set[str] = set()
    bom = manifest.get("bom")
    if isinstance(bom, dict):
        skills = bom.get("skills")
        if isinstance(skills, list):
            for s in skills:
                if isinstance(s, str) and s:
                    skill_ids.add(s)

    backup_root = Path(tempfile.mkdtemp(prefix="olaf_preserve_"))
    preserved_comp = backup_root / "competencies" / "my-competencies"
    preserved_comp.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(comp_dir, preserved_comp)

    preserved_skills_dir = backup_root / "skills"
    preserved_skills_dir.mkdir(parents=True, exist_ok=True)
    for sid in sorted(skill_ids):
        src = target_dir / "skills" / sid
        if not src.exists() or not src.is_dir():
            continue
        shutil.copytree(src, preserved_skills_dir / sid)

    return backup_root, skill_ids


def restore_my_competencies(target_dir: Path, backup_root: Path | None) -> None:
    if backup_root is None:
        return

    preserved_comp = backup_root / "competencies" / "my-competencies"
    if preserved_comp.exists():
        dst_comp = target_dir / "competencies" / "my-competencies"
        rmtree_if_exists(dst_comp)
        dst_comp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(preserved_comp, dst_comp)

    preserved_skills_dir = backup_root / "skills"
    if preserved_skills_dir.exists():
        for src in preserved_skills_dir.iterdir():
            if not src.is_dir():
                continue
            dst = target_dir / "skills" / src.name
            rmtree_if_exists(dst)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(src, dst)


def _normalize_registry_repo(value: str) -> str:
    v = value.strip()
    if not v:
        return v
    # Accept full GitHub URLs like https://github.com/org/repo
    if v.startswith("http://") or v.startswith("https://"):
        if "github.com/" in v:
            v = v.split("github.com/", 1)[1]
        v = v.removesuffix(".git")
    # Strip any leading slashes
    v = v.lstrip("/")
    return v


def load_install_seed_from_local_config(local_root: Path) -> tuple[str | None, str | None]:
    """Load install seed from local repo _olaf-config.json (preferred) or olaf-config.json.

    Expected format:
      {
        "registry-repo": "https://github.com/haal-ai/haal-ide",
        "branch": "main"
      }
    """

    config_path = local_root / "_olaf-config.json"
    if not config_path.exists() or not config_path.is_file():
        config_path = local_root / "olaf-config.json"
    if not config_path.exists() or not config_path.is_file():
        return None, None

    try:
        data = json.load(open(config_path, "r", encoding="utf-8"))
    except Exception:
        return None, None

    repo = data.get("registry-repo")
    branch = data.get("branch")

    repo_out = _normalize_registry_repo(repo) if isinstance(repo, str) else None
    branch_out = branch.strip() if isinstance(branch, str) and branch.strip() else None

    return repo_out, branch_out


def _seed_source_label(*, args_repo: str | None, args_branch: str | None, cfg_repo: str | None, cfg_branch: str | None) -> str:
    if isinstance(args_repo, str) and args_repo.strip():
        return "CLI (--repo/--branch)"
    if isinstance(args_branch, str) and args_branch.strip():
        return "CLI (--repo/--branch)"
    if (cfg_repo and cfg_repo.strip()) or (cfg_branch and cfg_branch.strip()):
        return "local config (_olaf-config.json/olaf-config.json)"
    return "built-in defaults"


def ensure_git_available() -> None:
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError as ex:
        raise RuntimeError("git is required but was not found on PATH. Please install Git and retry.") from ex
    except subprocess.CalledProcessError as ex:
        raise RuntimeError("git is required but could not be executed (git --version failed).") from ex


def ensure_git_repo(local_root: Path, *, init_if_missing: bool) -> None:
    if (local_root / ".git").exists():
        return
    if not init_if_missing:
        raise RuntimeError(
            f"Local path is not a git repository (missing .git): {local_root}\n"
            "Either run 'git init' (or clone a repo) first, or re-run with --init-git."
        )

    local_root.mkdir(parents=True, exist_ok=True)
    run(["git", "init"], cwd=local_root, quiet=True)


def _normalize_windows_drive_letter(path_str: str) -> str:
    # Some tooling treats workspace paths as case-sensitive on Windows.
    # Normalize drive letter to lowercase to avoid C: vs c: mismatches.
    if len(path_str) >= 2 and path_str[1] == ":" and path_str[0].isalpha():
        return path_str[0].lower() + path_str[1:]
    return path_str


def rmtree_if_exists(path: Path) -> None:
    if not path.exists():
        return

    def _on_rm_error(func, p, exc_info):
        try:
            os.chmod(p, 0o700)
            func(p)
        except Exception:
            raise

    try:
        shutil.rmtree(path, onerror=_on_rm_error)
        return
    except PermissionError:
        # Common on Windows when AV or a git process temporarily holds pack files.
        # Retry briefly, then fall back to renaming aside.
        for _ in range(5):
            time.sleep(0.25)
            try:
                shutil.rmtree(path, onerror=_on_rm_error)
                return
            except PermissionError:
                continue

        ts = int(time.time())
        backup = path.with_name(f"{path.name}_old_{ts}")
        try:
            if backup.exists():
                shutil.rmtree(backup, onerror=_on_rm_error)
            path.rename(backup)
        except Exception as ex:
            raise RuntimeError(
                f"Could not remove temp clone directory '{path}'. It may be locked by another process. "
                "Close programs using it and retry."
            ) from ex


def copy_dir(src: Path, dst: Path) -> None:
    if not src.exists() or not src.is_dir():
        raise RuntimeError(f"Expected directory does not exist: {src}")

    rmtree_if_exists(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)


def copy_dir_excluding_top_level(src: Path, dst: Path, *, exclude_names: set[str]) -> None:
    if not src.exists() or not src.is_dir():
        raise RuntimeError(f"Expected directory does not exist: {src}")

    def _ignore(directory: str, names: list[str]) -> set[str]:
        try:
            if Path(directory).resolve() == src.resolve():
                return {n for n in names if n in exclude_names}
        except Exception:
            return set()
        return set()

    rmtree_if_exists(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, ignore=_ignore)


def merge_dir_excluding_top_level(src: Path, dst: Path, *, exclude_names: set[str]) -> None:
    """Merge-copy src into dst, excluding some top-level names.

    Unlike copy_dir_excluding_top_level, this does NOT delete the destination.
    Later installs override earlier ones file-by-file.
    """

    if not src.exists() or not src.is_dir():
        raise RuntimeError(f"Expected directory does not exist: {src}")

    dst.mkdir(parents=True, exist_ok=True)

    for child in src.iterdir():
        if child.name in exclude_names:
            continue

        dest = dst / child.name
        if child.is_dir():
            # Merge directory tree, overwriting files.
            shutil.copytree(child, dest, dirs_exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(child, dest)


def parse_repo_branch(spec: str) -> tuple[str, str]:
    """Parse 'owner/repo@branch' (branch optional, defaults to main)."""
    s = spec.strip()
    if not s:
        raise ValueError("Empty repo spec")
    if "@" in s:
        repo, branch = s.split("@", 1)
        repo = repo.strip()
        branch = branch.strip() or "main"
        return repo, branch
    return s, "main"


def load_registry_from_clone(clone_dir: Path) -> list[tuple[str, str]]:
    """Load secondary repos from olaf-registry.json at repo root in clone."""

    registry_path = clone_dir / "olaf-registry.json"
    if not registry_path.exists() or not registry_path.is_file():
        return []

    try:
        data = json.load(open(registry_path, "r", encoding="utf-8"))
    except Exception:
        return []

    items = data.get("secondary-repos")
    if not isinstance(items, list):
        return []

    out: list[tuple[str, str]] = []
    for it in items:
        if not isinstance(it, str):
            continue
        try:
            out.append(parse_repo_branch(it))
        except ValueError:
            continue

    return out


def clone_repo_to(
    *,
    repo: str,
    branch: str,
    dst: Path,
) -> None:
    url = f"https://github.com/{repo}.git"
    rmtree_if_exists(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", "--branch", branch, url, str(dst)], quiet=True)


def merge_install_from_clone(
    *,
    clone_dir: Path,
    target_dir: Path,
) -> None:
    src_olaf = clone_dir / ".olaf"
    if not src_olaf.exists():
        raise RuntimeError(f"Clone does not contain .olaf folder: {src_olaf}")
    merge_dir_excluding_top_level(src_olaf, target_dir, exclude_names={"docs", "tools"})


def copy_olaf_prefixed_files(src_root: Path, dst_root: Path) -> int:
    copied = 0
    if not src_root.exists():
        return 0

    for path in src_root.rglob("*"):
        if not path.is_file():
            continue
        if not path.name.startswith("olaf-"):
            continue

        rel = path.relative_to(src_root)
        dest = dst_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, dest)
        copied += 1

    return copied


def sync_local_helper_files_from_clone(*, clone_root: Path, local_root: Path) -> None:
    # Copy olaf-* files into local project folders
    for tool_dir in [".github", ".kiro", ".windsurf"]:
        src_dir = clone_root / tool_dir
        dst_dir = local_root / tool_dir
        copied = copy_olaf_prefixed_files(src_dir, dst_dir)
        _ = copied

        # Rewrite any hardcoded references to ~/.olaf inside the synced olaf-* files
        _ = rewrite_olaf_paths(dst_dir, Path.home() / ".olaf", name_prefix="olaf-")


def _ensure_workspace_readonly_settings(settings: dict, target_dir: Path) -> None:
    target_pattern = f"{_normalize_windows_drive_letter(target_dir.as_posix())}/**"

    readonly = settings.get("files.readonlyInclude")
    if readonly is None:
        readonly = {}
        settings["files.readonlyInclude"] = readonly
    if isinstance(readonly, dict):
        readonly[target_pattern] = True

    files_exclude = settings.get("files.exclude")
    if files_exclude is None:
        files_exclude = {}
        settings["files.exclude"] = files_exclude
    if isinstance(files_exclude, dict):
        files_exclude[target_pattern] = True

    watcher_exclude = settings.get("files.watcherExclude")
    if watcher_exclude is None:
        watcher_exclude = {}
        settings["files.watcherExclude"] = watcher_exclude
    if isinstance(watcher_exclude, dict):
        watcher_exclude[target_pattern] = True


def write_code_workspace(repo_root: Path, target_dir: Path, *, window_title: str) -> Path:
    workspace_path = repo_root / "olaf.code-workspace"
    workspace = {
        "folders": [
            {"path": "."},
            {"path": _normalize_windows_drive_letter(str(target_dir))},
        ],
        "settings": {
            "window.title": window_title,
        },
    }
    _ensure_workspace_readonly_settings(workspace["settings"], target_dir)
    workspace_path.write_text(json.dumps(workspace, indent=2) + "\n", encoding="utf-8")
    return workspace_path


def find_existing_code_workspace(repo_root: Path) -> Path | None:
    candidates: list[Path] = []

    for p in repo_root.glob("*.code-workspace"):
        if p.is_file():
            candidates.append(p)

    for p in repo_root.rglob("*.code-workspace"):
        if not p.is_file():
            continue
        if p in candidates:
            continue
        candidates.append(p)

    if not candidates:
        return None

    # Prefer the closest match to repo root.
    candidates = sorted(candidates, key=lambda p: (len(p.parts), str(p).lower()))
    return candidates[0]


def ensure_workspace_has_target(workspace_path: Path, target_dir: Path, *, window_title: str) -> bool:
    try:
        raw = workspace_path.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as ex:
        raise RuntimeError(f"Existing workspace is not valid JSON: {workspace_path}") from ex

    if not isinstance(data, dict):
        raise RuntimeError(f"Existing workspace JSON must be an object: {workspace_path}")

    folders = data.get("folders")
    if folders is None:
        folders = []
        data["folders"] = folders
    if not isinstance(folders, list):
        raise RuntimeError(f"Workspace 'folders' must be a list: {workspace_path}")

    settings = data.get("settings")
    if settings is None:
        settings = {}
        data["settings"] = settings
    if not isinstance(settings, dict):
        raise RuntimeError(f"Workspace 'settings' must be an object: {workspace_path}")

    target_str = _normalize_windows_drive_letter(str(target_dir))
    already = False
    for f in folders:
        if isinstance(f, dict) and f.get("path") == target_str:
            already = True
            break

    settings["window.title"] = window_title
    _ensure_workspace_readonly_settings(settings, target_dir)

    if already:
        workspace_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        return False

    folders.append({"path": target_str})
    workspace_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return True


def _merge_dict_bool_settings(dst: dict, src: dict) -> dict:
    if not isinstance(dst, dict):
        return dst
    for k, v in src.items():
        if k not in dst:
            dst[k] = v
        else:
            if isinstance(v, bool) and isinstance(dst.get(k), bool):
                dst[k] = dst[k] or v
    return dst


def ensure_global_olaf_folder_protection(target_dir: Path) -> None:
    vscode_dir = target_dir / ".vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)
    settings_path = vscode_dir / "settings.json"

    existing: dict = {}
    if settings_path.exists():
        try:
            raw = settings_path.read_text(encoding="utf-8")
            existing = json.loads(raw) if raw.strip() else {}
        except Exception:
            existing = {}

    if not isinstance(existing, dict):
        existing = {}

    desired_readonly = {"**": True}
    desired_exclude = {"**": True}

    readonly = existing.get("files.readonlyInclude")
    if readonly is None:
        readonly = {}
        existing["files.readonlyInclude"] = readonly
    if isinstance(readonly, dict):
        _merge_dict_bool_settings(readonly, desired_readonly)

    files_exclude = existing.get("files.exclude")
    if files_exclude is None:
        files_exclude = {}
        existing["files.exclude"] = files_exclude
    if isinstance(files_exclude, dict):
        _merge_dict_bool_settings(files_exclude, desired_exclude)

    watcher_exclude = existing.get("files.watcherExclude")
    if watcher_exclude is None:
        watcher_exclude = {}
        existing["files.watcherExclude"] = watcher_exclude
    if isinstance(watcher_exclude, dict):
        _merge_dict_bool_settings(watcher_exclude, desired_exclude)

    settings_path.write_text(json.dumps(existing, indent=2) + "\n", encoding="utf-8")


def _is_text_file(path: Path) -> bool:
    # Conservative: only rewrite common text formats.
    return path.suffix.lower() in {
        ".md",
        ".txt",
        ".json",
        ".yaml",
        ".yml",
        ".py",
        ".ps1",
        ".sh",
        ".toml",
        ".ini",
    }


def rewrite_olaf_paths(root: Path, target_dir: Path, *, name_prefix: str | None = None) -> int:
    replaced = 0
    target_str = _normalize_windows_drive_letter(str(target_dir))
    replacements = {
        "~/.olaf": target_str,
        "~/.olaf/": target_str + os.sep,
        "`~/.olaf": f"`{target_str}",
        "`~/.olaf/": f"`{target_str}{os.sep}",
        "$HOME/.olaf": target_str,
        "$HOME/.olaf/": target_str + os.sep,
        "$env:USERPROFILE\\.olaf": target_str,
        "%USERPROFILE%\\.olaf": target_str,
    }

    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if name_prefix and not p.name.startswith(name_prefix):
            continue
        if not _is_text_file(p):
            continue

        try:
            before = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        after = before
        for src, dst in replacements.items():
            effective_dst = dst
            # If we are rewriting inside Python source, escape backslashes so we
            # don't create invalid string literals like "C:\Users\...".
            if p.suffix.lower() == ".py":
                effective_dst = effective_dst.replace("\\", "\\\\")
            after = after.replace(src, effective_dst)

        if after != before:
            p.write_text(after, encoding="utf-8")
            replaced += 1

    return replaced


def ensure_local_olaf_skeleton(repo_root: Path) -> Path:
    local_olaf = repo_root / ".olaf"

    # create minimal skeleton only if missing
    (repo_root / "competencies").mkdir(parents=True, exist_ok=True)
    (repo_root / "reference").mkdir(parents=True, exist_ok=True)
    (repo_root / "schemas").mkdir(parents=True, exist_ok=True)
    (repo_root / "scripts").mkdir(parents=True, exist_ok=True)
    (repo_root / "skills").mkdir(parents=True, exist_ok=True)
    (local_olaf / "data").mkdir(parents=True, exist_ok=True)
    (local_olaf / "work" / "staging").mkdir(parents=True, exist_ok=True)
    return repo_root


def ensure_local_team_competencies_manifest(repo_root: Path) -> Path:
    _ = ensure_local_olaf_skeleton(repo_root)
    comp_dir = repo_root / "competencies" / "team-competencies"
    manifest_path = comp_dir / "competency-manifest.json"

    # If the file exists but is empty/invalid, treat it as missing and regenerate.
    if manifest_path.exists():
        try:
            raw = manifest_path.read_text(encoding="utf-8", errors="ignore")
            if raw.strip():
                _ = json.loads(raw)
                return manifest_path
        except Exception:
            pass

    comp_dir.mkdir(parents=True, exist_ok=True)

    # Minimal manifest so team-competencies can be treated as a local kernel competency,
    # even before a team defines any skills.
    manifest = {
        "metadata": {
            "id": "team-competencies",
            "name": "Team Competencies",
            "shortDescription": "Team-maintained local competency",
            "description": "Local competency package for team/project skills.",
            "version": "1.0.0",
            "objectives": ["Provide a local place to register team skills"],
            "tags": ["team", "local"],
            "author": "OLAF",
            "status": "experimental",
            "exposure": "internal",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().strftime("%Y-%m-%d"),
        },
        "bom": {
            "skills": [],
            "entry_points": [],
        },
    }

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def copy_team_competencies_manifest(clone_root: Path, repo_root: Path) -> None:
    # Preserve an existing local team competency.
    # This competency represents the team's local state; only seed it if missing.
    local_existing = repo_root / "competencies" / "team-competencies"
    if local_existing.exists():
        return

    src_competencies = clone_root / "competencies"
    if not src_competencies.exists():
        raise RuntimeError(f"Missing expected competencies folder in clone: {src_competencies}")

    # find a likely manifest file (names vary across branches)
    manifest_candidates: list[Path] = []

    # 1) direct common names
    for name in [
        "team-competencies-manifest.json",
        "team-competencies-manifest-v1.json",
        "team-competencies-manifest-v2.json",
    ]:
        p = src_competencies / name
        if p.exists():
            manifest_candidates.append(p)

    # 2) any json under a team-competencies folder that looks like a manifest
    team_dir = src_competencies / "team-competencies"
    if team_dir.exists() and team_dir.is_dir():
        for p in team_dir.rglob("*.json"):
            lname = p.name.lower()
            if "manifest" in lname or lname in {"manifest.json", "team-competencies.json"}:
                manifest_candidates.append(p)

    # 3) fallback: any json file anywhere under competencies whose filename contains both tokens
    if not manifest_candidates:
        for p in src_competencies.rglob("*.json"):
            lname = p.name.lower()
            if "team" in lname and "competenc" in lname and "manifest" in lname:
                manifest_candidates.append(p)

    if not manifest_candidates:
        # diagnostics: show a few likely json files
        likely: list[Path] = []
        for p in src_competencies.rglob("*.json"):
            rel = p.relative_to(src_competencies)
            rel_s = str(rel).lower()
            if "team" in rel_s or "manifest" in rel_s:
                likely.append(p)
        likely = sorted(likely, key=lambda p: len(str(p)))[:20]

        msg = (
            "Could not find team competencies manifest in clone under competencies. "
            "Searched for common names and for manifest.json inside team-competencies/."
        )
        if likely:
            msg += "\nCandidates found (inspect/confirm which one to copy):\n" + "\n".join(
                f"  - {p.relative_to(clone_root)}" for p in likely
            )
        raise RuntimeError(msg)

    manifest = sorted(set(manifest_candidates), key=lambda p: len(str(p)))[0]

    _ = ensure_local_olaf_skeleton(repo_root)
    dest_competencies = repo_root / "competencies"

    # copy folder containing manifest if it is in a subfolder; otherwise copy just the file
    if manifest.parent != src_competencies:
        rel_dir = manifest.parent.relative_to(src_competencies)
        dest_dir = dest_competencies / rel_dir
        rmtree_if_exists(dest_dir)
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(manifest.parent, dest_dir)
    else:
        dest_competencies.mkdir(parents=True, exist_ok=True)
        shutil.copy2(manifest, dest_competencies / manifest.name)


def ensure_git_exclude(repo_root: Path) -> None:
    exclude_path = repo_root / ".git" / "info" / "exclude"
    exclude_path.parent.mkdir(parents=True, exist_ok=True)

    existing = ""
    if exclude_path.exists():
        existing = exclude_path.read_text(encoding="utf-8", errors="ignore")

    lines = [ln.strip() for ln in existing.splitlines()]
    if "olaf-*" not in lines:
        with exclude_path.open("a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write("olaf-*\n")

    existing = ""
    if exclude_path.exists():
        existing = exclude_path.read_text(encoding="utf-8", errors="ignore")
    lines = [ln.strip() for ln in existing.splitlines()]
    if ".olaf/work" not in lines and ".olaf/work/" not in lines:
        with exclude_path.open("a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write(".olaf/work/\n")

    existing = ""
    if exclude_path.exists():
        existing = exclude_path.read_text(encoding="utf-8", errors="ignore")
    lines = [ln.strip() for ln in existing.splitlines()]
    if "olaf.code-workspace" not in lines:
        with exclude_path.open("a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write("olaf.code-workspace\n")


def copy_data_from_target_no_overwrite(target_dir: Path, repo_root: Path) -> int:
    local_olaf = ensure_local_olaf_skeleton(repo_root)
    src_data = target_dir / "data"
    if not src_data.exists() or not src_data.is_dir():
        return 0

    dst_data = local_olaf / "data"
    copied = 0

    for p in src_data.rglob("*"):
        if p.is_dir():
            continue

        rel = p.relative_to(src_data)
        dest = dst_data / rel
        if dest.exists():
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest)
        copied += 1

    return copied


def main() -> int:
    parser = argparse.ArgumentParser(description="Clone OLAF repo and install .olaf plus olaf-* helper files")
    parser.add_argument("--repo", default=None, help="GitHub repo in owner/repo form (defaults from olaf-config.json if present)")
    parser.add_argument("--branch", default=None, help="Git branch name (defaults from olaf-config.json if present)")
    parser.add_argument(
        "--init-git",
        "--git-init",
        action="store_true",
        help="If --local is not a git repo, run 'git init' in that folder",
    )
    parser.add_argument(
        "--clean-global",
        action="store_true",
        help="Delete the global target folder (default: ~/.olaf) before reinstalling",
    )
    parser.add_argument(
        "--clean-local",
        action="store_true",
        help="Delete the local .olaf folder under --local before reinstalling",
    )
    parser.add_argument(
        "--no-preserve-my-competencies",
        action="store_true",
        help="When doing --clean-global, do not preserve ~/.olaf/competencies/my-competencies",
    )
    parser.add_argument(
        "--no-prune",
        action="store_true",
        help="Disable automatic pruning even if prune list files are present.",
    )
    parser.add_argument(
        "--prune-file",
        default=None,
        help="Path to prune list JSON file. If relative, treated as relative to --local repo root.",
    )
    parser.add_argument(
        "--target",
        default=str(Path.home() / ".olaf"),
        help="Target folder for installed .olaf (default: ~/.olaf)",
    )
    parser.add_argument(
        "--local",
        default=".",
        help="Folder where local .olaf will be created/updated (default: current directory)",
    )

    args = parser.parse_args()

    try:
        ensure_git_available()

        launch_root = Path.cwd()
        local_root = Path(os.path.expanduser(args.local)).resolve() if args.local else launch_root
        window_title = f"{local_root.name} (olaf)"

        ensure_git_repo(local_root, init_if_missing=bool(args.init_git))

        cfg_repo, cfg_branch = load_install_seed_from_local_config(local_root)
        repo = args.repo if isinstance(args.repo, str) and args.repo.strip() else cfg_repo
        branch = args.branch if isinstance(args.branch, str) and args.branch.strip() else cfg_branch
        if not repo:
            repo = "haal-ai/haal-ide"
        if not branch:
            branch = "main"

        print("\n============================================================")
        print("  OLAF Installer")
        print("============================================================")
        print(f"Seed source: {_seed_source_label(args_repo=args.repo, args_branch=args.branch, cfg_repo=cfg_repo, cfg_branch=cfg_branch)}")
        if cfg_repo or cfg_branch:
            print(f"olaf-config.json: repo={cfg_repo or '(unset)'} branch={cfg_branch or '(unset)'}")
        if isinstance(args.repo, str) and args.repo.strip():
            print(f"CLI override: repo={args.repo.strip()}")
        if isinstance(args.branch, str) and args.branch.strip():
            print(f"CLI override: branch={args.branch.strip()}")
        print(f"Effective seed: {repo}@{branch}\n")

        # fixed temp clone directory
        temp_base = Path(tempfile.gettempdir())
        clone_dir = temp_base / "haal_olaf_clone"

        target_dir = Path(os.path.expanduser(args.target)).resolve()
        if args.clean_global:
            if args.no_preserve_my_competencies:
                rmtree_if_exists(target_dir)
            else:
                preserve_root, _ = preserve_my_competencies(target_dir)
                rmtree_if_exists(target_dir)
                target_dir.mkdir(parents=True, exist_ok=True)
                restore_my_competencies(target_dir, preserve_root)

        local_olaf_dir = local_root / ".olaf"
        if args.clean_local:
            rmtree_if_exists(local_olaf_dir)

        print(f"Installing OLAF (global) -> {target_dir}")
        clone_repo_to(repo=repo, branch=branch, dst=clone_dir)

        # install .olaf to target (cumulative)
        print("Global install: updating ~/.olaf (cumulative registry install)")
        preserve_root = None
        if not args.clean_global and not args.no_preserve_my_competencies:
            preserve_root, _ = preserve_my_competencies(target_dir)

        secondary, registry_msg = load_registry_with_diagnostics(clone_dir)
        if secondary:
            print(f"Registry: found {len(secondary)} secondary repo(s) from {registry_msg}")
            print("Registry: applying secondary installs bottom-to-top (last entry first)")
            for srepo, sbranch in secondary:
                print(f"- secondary: {srepo}@{sbranch}")
            print("")
        else:
            print(f"Registry: no secondary repos ({registry_msg})")

        # Apply secondaries from bottom to top, then seed last (seed wins).
        secondary_to_apply = list(reversed(secondary))
        for idx, (srepo, sbranch) in enumerate(secondary_to_apply, start=1):
            sec_clone = temp_base / f"haal_olaf_clone_secondary_{idx}"
            print(f"Global install: merging secondary [{idx}/{len(secondary_to_apply)}] {srepo}@{sbranch}")
            clone_repo_to(repo=srepo, branch=sbranch, dst=sec_clone)
            try:
                merge_install_from_clone(clone_dir=sec_clone, target_dir=target_dir)
            except Exception as ex:
                print(f"⚠️  Secondary skipped (not an OLAF repo/branch?): {srepo}@{sbranch}")
                print(f"   Reason: {ex}")
                continue

        print(f"Global install: merging seed {repo}@{branch}")
        merge_install_from_clone(clone_dir=clone_dir, target_dir=target_dir)

        if preserve_root is not None:
            print("Global install: restoring user competency my-competencies")
            restore_my_competencies(target_dir, preserve_root)

        secondary_clone_dirs: list[Path] = []
        for idx in range(1, len(secondary_to_apply) + 1):
            sec_clone = temp_base / f"haal_olaf_clone_secondary_{idx}"
            if sec_clone.exists():
                secondary_clone_dirs.append(sec_clone)

        apply_prune_list(
            target_dir=target_dir,
            clone_dir=clone_dir,
            secondary_clone_dirs=secondary_clone_dirs,
            local_root=local_root,
            enabled=not bool(args.no_prune),
            prune_file=args.prune_file,
        )

        sanitize_global_competency_collections(target_dir)

        install_minimal_tools(target_dir, clone_dir)

        ensure_global_olaf_folder_protection(target_dir)

        # Seed wins for global active collection selection.
        sync_global_active_collection_from_seed(clone_dir=clone_dir, target_dir=target_dir)

        # Regenerate global index under ~/.olaf based on global collection selection.
        # This is separate from the repo-local index under <repo>/.olaf.
        global_collection_id = _pick_collection_id_from_file(target_dir / "reference" / "competency-collections.json")
        if local_root is None:
            if not global_collection_id:
                global_collection_id = "core"
            global_index_path = generate_query_competency_index(target_dir, collection_id=global_collection_id)
            print(f"Global install: competency index generated -> {global_index_path}")

        # Rewrite any hardcoded references to ~/.olaf inside the installed target
        rewritten = rewrite_olaf_paths(target_dir, target_dir)
        _ = rewritten

        # Prefer local competency-collections (user may have modified it). If missing, seed it from target.
        local_collections_file = ensure_local_competency_collections(local_root, target_dir)

        # Ensure local kernel competency 'team-competencies' exists.
        # Prefer copying the skeleton from the seed clone; fallback to generating a minimal manifest.
        try:
            copy_team_competencies_manifest(clone_dir, local_root)
        except Exception:
            pass
        _ = ensure_local_team_competencies_manifest(local_root)

        collection_id = _pick_collection_id_from_file(local_collections_file)
        if not collection_id:
            collection_id = _pick_collection_id_from_file(target_dir / "reference" / "competency-collections.json")

        index_path = generate_query_competency_index(target_dir, collection_id=collection_id, local_root=local_root)
        print(f"Local install: competency index generated -> {index_path}")

        print(f"Local install: syncing helper files into {local_root}")

        # Apply helper files cumulatively from secondary clones, then seed clone last.
        for idx, (srepo, sbranch) in enumerate(secondary_to_apply, start=1):
            sec_clone = temp_base / f"haal_olaf_clone_secondary_{idx}"
            if sec_clone.exists():
                sync_local_helper_files_from_clone(clone_root=sec_clone, local_root=local_root)

        sync_local_helper_files_from_clone(clone_root=clone_dir, local_root=local_root)

        # ensure local .olaf skeleton exists (only created if missing)
        ensure_local_olaf_skeleton(local_root)

        # copy only competencies marked as local in competency-collections.json
        locations = _load_competency_locations(local_collections_file)
        local_competency_ids = {k for k, v in locations.items() if k != "default" and v == "local"}
        # team-competencies is handled separately and should never be overwritten.
        local_competency_ids.discard("team-competencies")
        copy_local_competencies_from_clone(clone_dir, local_root, local_competency_ids)

        # copy installed target /data into local repo .olaf/data without overwriting anything
        copied_data = copy_data_from_target_no_overwrite(target_dir, local_root)
        print(f"Local install: updated -> {local_root / '.olaf'} (added {copied_data} files)")

        # Update an existing workspace if present, otherwise create a new one at local project root.
        existing_workspace = find_existing_code_workspace(local_root)
        if existing_workspace:
            changed = ensure_workspace_has_target(existing_workspace, target_dir, window_title=window_title)
            workspace_to_open = existing_workspace
        else:
            workspace_path = write_code_workspace(local_root, target_dir, window_title=window_title)
            workspace_to_open = workspace_path

        # ensure git excludes olaf-* in the local project
        ensure_git_exclude(local_root)

        print("Open workspace:")
        print(f"  windsurf {workspace_to_open}")
        print(f"  code {workspace_to_open}")
        print("Done")
        return 0

    except RuntimeError as ex:
        eprint(str(ex))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
