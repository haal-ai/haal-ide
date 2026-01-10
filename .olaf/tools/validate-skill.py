#!/usr/bin/env python3
"""
Skill Validation Script for OLAF Framework
Validates skills against:
1. Folder structure requirements
2. Skill manifest schema compliance
3. BOM completeness (files referenced in manifest exist)
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re

class SkillValidator:
    def __init__(self, skills_dir: Path, schema_path: Path):
        self.skills_dir = skills_dir
        self.schema_path = schema_path
        self.schema = self._load_schema()
        
    def _load_schema(self) -> Dict:
        """Load the skill manifest schema"""
        with open(self.schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def validate_skill(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate a single skill
        Returns: (is_valid, list_of_errors)
        """
        errors = []
        skill_name = skill_path.name
        
        # Hard-block deprecated/forbidden skills
        if skill_name == "deploy-imported-prompts":
            errors.append("Skill 'deploy-imported-prompts' is forbidden and must be removed")
            return False, errors
        
        # Check 1: skill-manifest.json exists
        manifest_path = skill_path / "skill-manifest.json"
        if not manifest_path.exists():
            errors.append(f"Missing skill-manifest.json")
            return False, errors
        
        # Load manifest
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON in skill-manifest.json: {e}")
            return False, errors
        
        # Check 2: Validate metadata section
        if "metadata" not in manifest:
            errors.append("Missing 'metadata' section")
        else:
            metadata_errors = self._validate_metadata(manifest["metadata"], skill_name)
            errors.extend(metadata_errors)
        
        # Check 3: Validate BOM section
        if "bom" not in manifest:
            errors.append("Missing 'bom' section")
        else:
            bom_errors = self._validate_bom(manifest["bom"], skill_path)
            errors.extend(bom_errors)
        
        # Check 4: Validate folder structure
        structure_errors = self._validate_folder_structure(skill_path, manifest.get("bom", {}))
        errors.extend(structure_errors)
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def _validate_metadata(self, metadata: Dict, skill_name: str) -> List[str]:
        """Validate metadata section against schema"""
        errors = []
        required_fields = [
            "id", "name", "shortDescription", "objectives", 
            "tags", "status", "exposure", "version", "protocol"
        ]
        
        for field in required_fields:
            if field not in metadata:
                errors.append(f"Missing required metadata field: {field}")
        
        # Validate id format (kebab-case, 2-6 words)
        if "id" in metadata:
            id_val = metadata["id"]
            if not re.match(r'^[a-z]+(-[a-z]+){1,5}$', id_val):
                errors.append(f"Invalid id format: '{id_val}' (must be kebab-case, 2-6 words)")
            if id_val != skill_name:
                errors.append(f"Skill id '{id_val}' doesn't match folder name '{skill_name}'")
        
        # Validate version format (semver)
        if "version" in metadata:
            if not re.match(r'^\d+\.\d+\.\d+$', metadata["version"]):
                errors.append(f"Invalid version format: '{metadata['version']}' (must be semver)")
        
        # Validate status enum
        if "status" in metadata:
            valid_statuses = ["experimental", "proven", "mainstream", "deprecated"]
            if metadata["status"] not in valid_statuses:
                errors.append(f"Invalid status: '{metadata['status']}' (must be one of {valid_statuses})")
        
        # Validate exposure enum
        if "exposure" in metadata:
            valid_exposures = ["export", "internal", "kernel"]
            if metadata["exposure"] not in valid_exposures:
                errors.append(f"Invalid exposure: '{metadata['exposure']}' (must be one of {valid_exposures})")
        
        # Validate protocol enum
        if "protocol" in metadata:
            valid_protocols = ["Act", "Propose-Act", "Propose-Confirm-Act"]
            if metadata["protocol"] not in valid_protocols:
                errors.append(f"Invalid protocol: '{metadata['protocol']}' (must be one of {valid_protocols})")
        
        # Validate objectives (1-5 items)
        if "objectives" in metadata:
            objectives = metadata["objectives"]
            if not isinstance(objectives, list):
                errors.append("objectives must be an array")
            elif len(objectives) < 1 or len(objectives) > 5:
                errors.append(f"objectives must have 1-5 items (found {len(objectives)})")
        
        # Validate tags (at least 1)
        if "tags" in metadata:
            tags = metadata["tags"]
            if not isinstance(tags, list):
                errors.append("tags must be an array")
            elif len(tags) < 1:
                errors.append("tags must have at least 1 item")
        
        return errors
    
    def _validate_bom(self, bom: Dict, skill_path: Path) -> List[str]:
        """Validate BOM section and file existence"""
        errors = []
        
        # prompts is required
        if "prompts" not in bom:
            errors.append("BOM missing required 'prompts' array")
        else:
            if not isinstance(bom["prompts"], list):
                errors.append("BOM 'prompts' must be an array")
            elif len(bom["prompts"]) < 1:
                errors.append("BOM 'prompts' must have at least 1 item")
            else:
                # Validate each prompt entry
                for idx, prompt in enumerate(bom["prompts"]):
                    if "name" not in prompt:
                        errors.append(f"prompts[{idx}] missing 'name' field")
                    if "path" not in prompt:
                        errors.append(f"prompts[{idx}] missing 'path' field")
                    else:
                        # Check file exists
                        prompt_path = skill_path / prompt["path"].lstrip("/")
                        if not prompt_path.exists():
                            errors.append(f"prompts[{idx}] file not found: {prompt['path']}")
                        # Check path starts with /prompts/
                        if not prompt["path"].startswith("/prompts/"):
                            errors.append(f"prompts[{idx}] path must start with '/prompts/' (found: {prompt['path']})")
        
        # Validate optional BOM sections
        optional_sections = ["helpers", "templates", "tools", "docs", "kb", "skill_dependencies"]
        for section in optional_sections:
            if section in bom:
                if not isinstance(bom[section], list):
                    errors.append(f"BOM '{section}' must be an array")
                else:
                    # Validate each entry
                    for idx, item in enumerate(bom[section]):
                        if "name" not in item:
                            errors.append(f"{section}[{idx}] missing 'name' field")
                        if "path" not in item:
                            errors.append(f"{section}[{idx}] missing 'path' field")
                        elif section != "skill_dependencies":
                            # Check file exists (not for dependencies)
                            item_path = skill_path / item["path"].lstrip("/")
                            if not item_path.exists():
                                errors.append(f"{section}[{idx}] file not found: {item['path']}")
        
        return errors
    
    def _validate_folder_structure(self, skill_path: Path, bom: Dict) -> List[str]:
        """Validate folder structure based on BOM"""
        errors = []
        
        # prompts/ directory is required
        prompts_dir = skill_path / "prompts"
        if not prompts_dir.exists():
            errors.append("Missing required 'prompts/' directory")
        elif not prompts_dir.is_dir():
            errors.append("'prompts/' exists but is not a directory")
        
        # Check for directories based on BOM
        if "templates" in bom and len(bom["templates"]) > 0:
            templates_dir = skill_path / "templates"
            if not templates_dir.exists():
                errors.append("BOM references templates but 'templates/' directory not found")
        
        if "tools" in bom and len(bom["tools"]) > 0:
            tools_dir = skill_path / "tools"
            if not tools_dir.exists():
                errors.append("BOM references tools but 'tools/' directory not found")
        
        if "helpers" in bom and len(bom["helpers"]) > 0:
            helpers_dir = skill_path / "helpers"
            if not helpers_dir.exists():
                errors.append("BOM references helpers but 'helpers/' directory not found")
        
        if "kb" in bom and len(bom["kb"]) > 0:
            kb_dir = skill_path / "kb"
            if not kb_dir.exists():
                errors.append("BOM references kb but 'kb/' directory not found")
        
        if "docs" in bom and len(bom["docs"]) > 0:
            docs_dir = skill_path / "docs"
            if not docs_dir.exists():
                errors.append("BOM references docs but 'docs/' directory not found")
        
        return errors
    
    def validate_all_skills(self) -> Dict[str, Tuple[bool, List[str]]]:
        """Validate all skills in the skills directory"""
        results = {}
        
        for skill_dir in sorted(self.skills_dir.iterdir()):
            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                # Skip common and task-registry.json
                if skill_dir.name == "common":
                    continue
                
                is_valid, errors = self.validate_skill(skill_dir)
                results[skill_dir.name] = (is_valid, errors)
        
        return results


def main():
    # Setup paths
    repo_root = Path(__file__).parent.parent.parent
    skills_dir = repo_root / ".olaf" / "core" / "skills"
    schema_path = repo_root / ".olaf" / "core" / "schemas" / "olaf-skill-manifest.schema.json"
    
    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        sys.exit(1)
    
    if not schema_path.exists():
        print(f"Error: Schema file not found: {schema_path}")
        sys.exit(1)
    
    print("=" * 80)
    print("OLAF Skill Validation Report")
    print("=" * 80)
    print()
    
    validator = SkillValidator(skills_dir, schema_path)
    results = validator.validate_all_skills()
    
    # Categorize results
    valid_skills = []
    invalid_skills = []
    
    for skill_name, (is_valid, errors) in results.items():
        if is_valid:
            valid_skills.append(skill_name)
        else:
            invalid_skills.append((skill_name, errors))
    
    # Print summary
    print(f"Total skills scanned: {len(results)}")
    print(f"✓ Valid skills: {len(valid_skills)}")
    print(f"✗ Invalid skills: {len(invalid_skills)}")
    print()
    
    # Print valid skills
    if valid_skills:
        print("=" * 80)
        print("VALID SKILLS (Ready to move)")
        print("=" * 80)
        for skill_name in valid_skills:
            print(f"  ✓ {skill_name}")
        print()
    
    # Print invalid skills with errors
    if invalid_skills:
        print("=" * 80)
        print("INVALID SKILLS (Need fixing)")
        print("=" * 80)
        for skill_name, errors in invalid_skills:
            print(f"\n✗ {skill_name}")
            for error in errors:
                print(f"    - {error}")
        print()
    
    # Generate JSON report
    report_path = repo_root / ".olaf" / "work" / "skill-validation-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    report = {
        "total_skills": len(results),
        "valid_count": len(valid_skills),
        "invalid_count": len(invalid_skills),
        "valid_skills": valid_skills,
        "invalid_skills": [
            {"skill": name, "errors": errors}
            for name, errors in invalid_skills
        ]
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    
    print(f"Full report saved to: {report_path}")
    print()
    
    # Exit code
    sys.exit(0 if len(invalid_skills) == 0 else 1)


if __name__ == "__main__":
    main()
