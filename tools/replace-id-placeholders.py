#!/usr/bin/env python3
"""
Script to replace [id:xxxxx] placeholders with actual hardcoded paths
based on the memory-map definitions.
"""

import os
import re
from pathlib import Path

# Memory-map derived path mappings
PATH_MAPPINGS = {
    # Core directories
    '[id:core_olaf_dir]': '.olaf/',
    '[id:global_olaf_dir]': '~/.olaf/',
    '[id:core_dir]': '',  # Root of target repository
    
    # Derived directories
    '[id:docs_dir]': '.olaf/docs/',
    '[id:work_dir]': '.olaf/work/',
    '[id:staging_dir]': '.olaf/work/staging/',
    '[id:carryover_dir]': '.olaf/work/carry-over/',
    '[id:stash_dir]': '.olaf/work/stash/',
    
    # Skills and competencies
    '[id:skills_dir]': 'skills/',
    '[id:local_skills_dir]': 'skills/',
    '[id:global_skills_dir]': '~/.olaf/core/skills/',
    '[id:competencies_dir]': 'competencies/',
    '[id:schemas_dir]': 'schemas/',
    '[id:reference_dir]': 'reference/',
    
    # Framework files
    '[id:olaf_registry]': 'reference/olaf-registry.json',
    '[id:competency_collections]': 'reference/competency-collections.json',
    '[id:condensed_dir]': 'reference/.condensed/',
    '[id:condensed_framework]': 'reference/.condensed/olaf-framework-condensed.md',
    '[id:competency_index]': 'reference/query-competency-index.md',
    '[id:core_principles]': 'reference/core-principles.md',
    '[id:team_delegation]': 'reference/team-delegation.md',
    '[id:memory_map]': 'reference/memory-map.md',
    '[id:llm_vs_ide_task_guide]': 'reference/llm-vs-ide-task-guide.md',
    
    # Data environment
    '[id:data_dir]': '.olaf/data/',
    '[id:context_dir]': '.olaf/data/context/',
    '[id:context_default]': '.olaf/data/context/context-default.md',
    '[id:context_current]': '.olaf/data/context/context-current.md',
    '[id:peoples_dir]': '.olaf/data/peoples/',
    '[id:people_register]': '.olaf/data/peoples/people-register.md',
    '[id:projects_dir]': '.olaf/data/projects/',
    '[id:jobs_register]': '.olaf/data/projects/jobs-register.md',
    '[id:changelog_register]': '.olaf/data/projects/changelog-register.md',
    '[id:changelog_register_archive]': '.olaf/data/projects/changelog-archive.md',
    
    # Product directories
    '[id:product_dir]': '.olaf/data/product/',
    '[id:functional_dir]': '.olaf/data/product/functional/',
    '[id:technical_dir]': '.olaf/data/product/technical/',
    '[id:decision_records_dir]': '.olaf/data/product/decision-records/',
    '[id:documentations_dir]': '.olaf/data/product/documentations/',
    
    # Practices
    '[id:practices_dir]': '.olaf/data/practices/',
    '[id:standards_dir]': '.olaf/data/practices/standards/',
    '[id:handover]': '.olaf/data/handover-conversation*.md',
    
    # Tools and scripts
    '[id:tools_dir]': 'tools/',
    '[id:scripts_dir]': 'scripts/',
    
    # Additional missing placeholders found
    '[id:daily_dir]': '.olaf/data/product/daily/',
    '[id:carryo_dir]': '.olaf/work/carry-over/',
    '[id:jobs_dir]': '.olaf/data/projects/jobs/',
    '[id:changelog_registry_dir]': '.olaf/data/projects/changelog-register.md',
    '[id:jobs]': '.olaf/data/projects/jobs-register.md',
    '[id:kb_dir]': '.olaf/data/kb/',
    '[id:ads_dir]': '.olaf/work/staging/',
}

def replace_placeholders_in_file(file_path):
    """Replace [id:xxxxx] placeholders with actual paths in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace all placeholders
        for placeholder, actual_path in PATH_MAPPINGS.items():
            content = content.replace(placeholder, actual_path)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, len([p for p in PATH_MAPPINGS.keys() if p in original_content])
        
        return False, 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0

def process_directory(directory_path):
    """Process all .md files in a directory and its subdirectories."""
    dir_path = Path(directory_path)
    total_files_processed = 0
    total_placeholders_replaced = 0
    
    if not dir_path.exists():
        print(f"Directory not found: {directory_path}")
        return total_files_processed, total_placeholders_replaced
    
    # Process all .md, .py, and .json files in directory and subdirectories
    for md_file in dir_path.rglob("*"):
        if md_file.is_file() and md_file.suffix in ['.md', '.py', '.json']:
            processed, replacements = replace_placeholders_in_file(md_file)
            if processed:
                total_files_processed += 1
                total_placeholders_replaced += replacements
                print(f"Processed: {md_file.relative_to(dir_path)} ({replacements} replacements)")
    
    return total_files_processed, total_placeholders_replaced

if __name__ == "__main__":
    directories_to_process = ["skills", "docs"]
    
    print("Starting placeholder replacement...")
    print()
    
    total_files = 0
    total_replacements = 0
    
    for directory in directories_to_process:
        print(f"Processing directory: {directory}")
        files_processed, placeholders_replaced = process_directory(directory)
        total_files += files_processed
        total_replacements += placeholders_replaced
        print()
    
    print("Summary:")
    print(f"Files processed: {total_files}")
    print(f"Total placeholders replaced: {total_replacements}")
    print("Done!")
