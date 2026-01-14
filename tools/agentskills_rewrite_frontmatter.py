import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _parse_frontmatter_block(block: str) -> Dict[str, str]:
    """Parse a very small subset of YAML frontmatter.

    Supports only flat 'key: value' lines.
    This is sufficient for our current OLAF skill headers.
    """
    out: Dict[str, str] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def _yaml_quote_one_line(value: str) -> str:
    v = value.replace("\n", " ").strip()
    # Quote if it contains characters that could break YAML or be misread.
    if not v or any(ch in v for ch in [":", "#", '"']):
        v = v.replace('"', "\\\"")
        return f'"{v}"'
    return v


def _derive_description(
    *,
    fm: Dict[str, str],
    body: str,
    manifest_path: Path,
) -> str:
    desc = fm.get("description", "").strip().strip('"')
    if desc:
        return desc

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8", errors="replace"))
            if isinstance(manifest, dict):
                md = manifest.get("metadata")
                if isinstance(md, dict):
                    cand = md.get("description") or md.get("shortDescription")
                    if isinstance(cand, str) and cand.strip():
                        return cand.strip()
        except Exception:
            pass

    # Fallback: first heading or first non-empty line
    for line in body.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            return s.lstrip("#").strip() or "See skill content."
        return s

    return "See skill content."


def _build_agentskills_frontmatter(
    *,
    name: str,
    description: str,
    tags_raw: Optional[str],
    protocol_raw: Optional[str],
) -> str:
    lines: list[str] = [
        "---",
        f"name: {name}",
        f"description: {_yaml_quote_one_line(description)}",
        "license: Apache-2.0",
    ]

    meta_lines: list[str] = []
    if tags_raw:
        meta_lines.append(f"  olaf_tags: {_yaml_quote_one_line(tags_raw)}")
    if protocol_raw:
        meta_lines.append(f"  olaf_protocol: {_yaml_quote_one_line(protocol_raw)}")

    if meta_lines:
        lines.append("metadata:")
        lines.extend(meta_lines)

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def rewrite_skill_file(skill_md: Path) -> Tuple[bool, str]:
    name = skill_md.parent.name
    text = skill_md.read_text(encoding="utf-8", errors="replace")

    m = _FRONTMATTER_RE.match(text)
    if m:
        fm_block = m.group(1)
        body = text[m.end() :]
    else:
        fm_block = ""
        body = text

    fm = _parse_frontmatter_block(fm_block) if fm_block else {}

    desc = _derive_description(fm=fm, body=body, manifest_path=skill_md.parent / "skill-manifest.json")

    new_fm = _build_agentskills_frontmatter(
        name=name,
        description=desc,
        tags_raw=fm.get("tags"),
        protocol_raw=fm.get("protocol"),
    )

    new_text = new_fm + "\n" + body.lstrip("\n")
    if new_text == text:
        return False, "unchanged"

    skill_md.write_text(new_text, encoding="utf-8")
    return True, "updated"


def main() -> int:
    skills_root = Path("skills")
    if not skills_root.exists() or not skills_root.is_dir():
        print("skills/ not found")
        return 2

    skill_files = sorted([p for p in skills_root.glob("*/skill.md") if p.is_file()])

    updated = 0
    unchanged = 0
    failed: list[str] = []

    for skill_md in skill_files:
        try:
            did_update, status = rewrite_skill_file(skill_md)
            if did_update:
                updated += 1
            else:
                unchanged += 1
        except Exception as ex:
            failed.append(f"{skill_md}: {ex}")

    print(f"skills scanned: {len(skill_files)}")
    print(f"updated: {updated}")
    print(f"unchanged: {unchanged}")
    print(f"failed: {len(failed)}")
    if failed:
        print("FAILURES:")
        for f in failed[:50]:
            print(f"- {f}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
