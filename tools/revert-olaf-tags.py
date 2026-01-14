#!/usr/bin/env python3
"""
Script to revert <olaf> tag replacements back to original <olaf> tags in skill.md files.
"""

import os
from pathlib import Path

def get_header_content(header_file):
    """Read the header content from the header file."""
    try:
        with open(header_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
    except Exception as e:
        print(f"Error reading header file {header_file}: {e}")
        return None

def revert_olaf_tag_in_file(file_path, header_content):
    """Replace header content back to <olaf> tag in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace the header content back to <olaf> tag
        content = content.replace(header_content, '<olaf>')
        content = content.replace(header_content + '\n', '<olaf>\n')
        content = content.replace(header_content + '\n\n', '<olaf>\n\n')
        
        # Only write if content changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def process_skills_directory(skills_dir, header_file):
    """Process all skill.md files to revert <olaf> tag replacements."""
    skills_path = Path(skills_dir)
    header_content = get_header_content(header_file)
    
    if not header_content:
        print("Failed to read header content")
        return 0
    
    total_files_processed = 0
    
    print(f"Reverting <olaf> tag replacements in: {skills_dir}")
    print(f"Using header content from: {header_file}")
    print()
    
    # Process all skill.md files in skills directory and subdirectories
    for skill_file in skills_path.rglob("skill.md"):
        if skill_file.is_file():
            processed = revert_olaf_tag_in_file(skill_file, header_content)
            if processed:
                total_files_processed += 1
                print(f"Reverted: {skill_file.relative_to(skills_path)}")
    
    return total_files_processed

if __name__ == "__main__":
    skills_directory = "skills"
    header_file = "tools/header-for-olaf.md"
    
    files_processed = process_skills_directory(skills_directory, header_file)
    
    print()
    print(f"Summary: {files_processed} skill.md files reverted")
    print("Done!")
