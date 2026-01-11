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
        src_select = clone_dir / ".olaf" / "core" / "skills" / "create-skill" / "scripts" / "select_collection.py"
        if src_select.exists() and src_select.is_file():
            shutil.copy2(src_select, tools_dir / "select-collection.py")


def generate_query_competency_index(
    target_dir: Path,
    *,
    collection_id: str | None = None,
    local_root: Path | None = None,
) -> Path:
    preferred = target_dir / "tools" / "select-collection.py"
    fallback = target_dir / "core" / "skills" / "create-skill" / "scripts" / "select_collection.py"
    script = preferred if preferred.exists() else fallback
    if not script.exists():
        raise RuntimeError(
            "Missing select-collection tool in installed target. Expected one of: "
            f"{preferred} or {fallback}"
        )

    if not collection_id:
        collection_id = "core"

    if local_root is not None:
        output_path = local_root / ".olaf" / "core" / "reference" / "query-competency-index.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_path = target_dir / "core" / "reference" / "query-competency-index.md"
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
    local_ref = local_root / ".olaf" / "core" / "reference"
    local_ref.mkdir(parents=True, exist_ok=True)
    local_file = local_ref / "competency-collections.json"
    if local_file.exists():
        return local_file

    src = target_dir / "core" / "reference" / "competency-collections.json"
    if src.exists() and src.is_file():
        shutil.copy2(src, local_file)
    return local_file


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


def copy_local_competencies_from_clone(clone_root: Path, local_root: Path, local_competency_ids: set[str]) -> None:
    if not local_competency_ids:
        return

    src_competencies = clone_root / ".olaf" / "core" / "competencies"
    if not src_competencies.exists():
        raise RuntimeError(f"Missing expected competencies folder in clone: {src_competencies}")

    local_olaf = ensure_local_olaf_skeleton(local_root)
    dest_competencies = local_olaf / "core" / "competencies"
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
    collections_file = target_dir / "core" / "reference" / "competency-collections.json"
    if not collections_file.exists():
        return

    try:
        data = json.load(open(collections_file, "r", encoding="utf-8"))
    except Exception:
        return

    collections = data.get("collections")
    if not isinstance(collections, list):
        return

    global_competencies_dir = target_dir / "core" / "competencies"

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


def ensure_git_available() -> None:
    try:
        subprocess.run(["git", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError as ex:
        raise RuntimeError("git is required but was not found on PATH. Please install Git and retry.") from ex
    except subprocess.CalledProcessError as ex:
        raise RuntimeError("git is required but could not be executed (git --version failed).") from ex


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


def _ensure_workspace_readonly_settings(settings: dict, target_dir: Path) -> None:
    target_pattern = f"{target_dir.as_posix()}/**"

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

    search_exclude = settings.get("search.exclude")
    if search_exclude is None:
        search_exclude = {}
        settings["search.exclude"] = search_exclude
    if isinstance(search_exclude, dict):
        search_exclude[target_pattern] = True

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
            {"path": str(target_dir)},
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

    target_str = str(target_dir)
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

    search_exclude = existing.get("search.exclude")
    if search_exclude is None:
        search_exclude = {}
        existing["search.exclude"] = search_exclude
    if isinstance(search_exclude, dict):
        _merge_dict_bool_settings(search_exclude, desired_exclude)

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
    target_str = str(target_dir)
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
    if local_olaf.exists():
        return local_olaf

    # create minimal skeleton only if missing
    (local_olaf / "core" / "competencies").mkdir(parents=True, exist_ok=True)
    (local_olaf / "core" / "reference").mkdir(parents=True, exist_ok=True)
    (local_olaf / "core" / "schemas").mkdir(parents=True, exist_ok=True)
    (local_olaf / "core" / "scripts").mkdir(parents=True, exist_ok=True)
    (local_olaf / "core" / "skills").mkdir(parents=True, exist_ok=True)
    (local_olaf / "data").mkdir(parents=True, exist_ok=True)
    (local_olaf / "work" / "staging").mkdir(parents=True, exist_ok=True)
    (local_olaf / "work" / "carry-over").mkdir(parents=True, exist_ok=True)
    (local_olaf / "work" / "stash").mkdir(parents=True, exist_ok=True)
    return local_olaf


def copy_team_competencies_manifest(clone_root: Path, repo_root: Path) -> None:
    src_competencies = clone_root / ".olaf" / "core" / "competencies"
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
            "Could not find team competencies manifest in clone under .olaf/core/competencies. "
            "Searched for common names and for manifest.json inside team-competencies/."
        )
        if likely:
            msg += "\nCandidates found (inspect/confirm which one to copy):\n" + "\n".join(
                f"  - {p.relative_to(clone_root)}" for p in likely
            )
        raise RuntimeError(msg)

    manifest = sorted(set(manifest_candidates), key=lambda p: len(str(p)))[0]

    local_olaf = ensure_local_olaf_skeleton(repo_root)
    dest_competencies = local_olaf / "core" / "competencies"

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
    parser.add_argument("--repo", default="haal-ai/haal-ide", help="GitHub repo in owner/repo form")
    parser.add_argument("--branch", default="main", help="Git branch name")
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

        # fixed temp clone directory
        temp_base = Path(tempfile.gettempdir())
        clone_dir = temp_base / "haal_olaf_clone"

        rmtree_if_exists(clone_dir)
        clone_dir.parent.mkdir(parents=True, exist_ok=True)

        url = f"https://github.com/{args.repo}.git"
        print(f"Installing OLAF (global) -> {Path(os.path.expanduser(args.target)).resolve()}")
        run(["git", "clone", "--depth", "1", "--branch", args.branch, url, str(clone_dir)], quiet=True)

        # install .olaf to target
        target_dir = Path(os.path.expanduser(args.target)).resolve()
        src_olaf = clone_dir / ".olaf"
        if not src_olaf.exists():
            raise RuntimeError(
                f"Clone does not contain .olaf folder: {src_olaf}. "
                "This branch may not include OLAF yet; try --branch develop."
            )

        print("Global install: updating ~/.olaf")
        copy_dir_excluding_top_level(src_olaf, target_dir, exclude_names={"docs", "tools"})

        sanitize_global_competency_collections(target_dir)

        install_minimal_tools(target_dir, clone_dir)

        ensure_global_olaf_folder_protection(target_dir)

        # Rewrite any hardcoded references to ~/.olaf inside the installed target
        rewritten = rewrite_olaf_paths(target_dir, target_dir)
        _ = rewritten

        # Prefer local competency-collections (user may have modified it). If missing, seed it from target.
        local_collections_file = ensure_local_competency_collections(local_root, target_dir)
        collection_id = _pick_collection_id_from_file(local_collections_file)
        if not collection_id:
            collection_id = _pick_collection_id_from_file(target_dir / "core" / "reference" / "competency-collections.json")

        index_path = generate_query_competency_index(target_dir, collection_id=collection_id, local_root=local_root)
        print(f"Local install: competency index generated -> {index_path}")

        print(f"Local install: syncing helper files into {local_root}")

        # Copy olaf-* files into local project folders
        for tool_dir in [".github", ".kiro", ".windsurf"]:
            src_dir = clone_dir / tool_dir
            dst_dir = local_root / tool_dir
            copied = copy_olaf_prefixed_files(src_dir, dst_dir)
            _ = copied

            # Rewrite any hardcoded references to ~/.olaf inside the synced olaf-* files
            rewritten = rewrite_olaf_paths(dst_dir, target_dir, name_prefix="olaf-")
            _ = rewritten

        # ensure local .olaf skeleton exists (only created if missing)
        ensure_local_olaf_skeleton(local_root)

        # copy only competencies marked as local in competency-collections.json
        locations = _load_competency_locations(local_collections_file)
        local_competency_ids = {k for k, v in locations.items() if k != "default" and v == "local"}
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
