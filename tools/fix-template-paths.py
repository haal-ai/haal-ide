#!/usr/bin/env python3
"""
Script to fix template path references in skill files.
Converts various template path formats to consistent relative paths.
"""

import os
import re
from pathlib import Path

def fix_template_paths_in_file(file_path):
    """Fix template path references in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Convert skills/skill-name/templates/ to templates/
        content = re.sub(r'skills/[^/]+/templates/', 'templates/', content)
        
        # Pattern 2: Convert /templates/ to templates/ (remove leading slash)
        content = re.sub(r'"/templates/', '"templates/', content)
        content = re.sub(r'`/templates/', '`templates/', content)
        
        # Pattern 3: Convert absolute paths with skills/ to relative
        content = re.sub(r'`skills/[^/]+/templates/([^`]+)`', r'`templates/\1`', content)
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, len(re.findall(r'templates/', content))
        
        return False, 0
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, 0

def process_skills_directory(skills_dir):
    """Process all files for template path fixes."""
    skills_path = Path(skills_dir)
    total_files_processed = 0
    total_template_refs = 0
    
    # Process all relevant files in skills directory and subdirectories
    for file_path in skills_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in ['.md', '.json']:
            processed, template_refs = fix_template_paths_in_file(file_path)
            if processed:
                total_files_processed += 1
                total_template_refs += template_refs
                print(f"Fixed template paths: {file_path.relative_to(skills_path)} ({template_refs} template references)")
    
    return total_files_processed, total_template_refs

if __name__ == "__main__":
    skills_directory = "skills"
    
    print("Fixing template path references...")
    print(f"Processing directory: {skills_directory}")
    print()
    
    files_processed, template_refs = process_skills_directory(skills_directory)
    
    print()
    print("Summary:")
    print(f"Files processed: {files_processed}")
    print(f"Template references fixed: {template_refs}")
    print("Done!")
