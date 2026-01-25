#!/usr/bin/env python3
"""
Script to replace <olaf> tags in skill.md files with the header content from header-for-olaf.md
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

def replace_olaf_tag_in_file(file_path, header_content):
    """Replace <olaf> tag with header content in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace <olaf> tag (with or without trailing whitespace/newlines)
        content = content.replace('<olaf>', header_content)
        content = content.replace('<olaf>\n', header_content + '\n')
        content = content.replace('<olaf>\n\n', header_content + '\n\n')
        
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
    """Process all skill.md files for <olaf> tag replacement."""
    skills_path = Path(skills_dir)
    header_content = get_header_content(header_file)
    
    if not header_content:
        print("Failed to read header content")
        return 0
    
    total_files_processed = 0
    
    print(f"Replacing <olaf> tags with header content from: {header_file}")
    print(f"Processing directory: {skills_dir}")
    print()
    
    # Process all skill.md files in skills directory and subdirectories
    for skill_file in skills_path.rglob("skill.md"):
        if skill_file.is_file():
            processed = replace_olaf_tag_in_file(skill_file, header_content)
            if processed:
                total_files_processed += 1
                print(f"Updated: {skill_file.relative_to(skills_path)}")
    
    return total_files_processed

if __name__ == "__main__":
    skills_directory = "skills"
    header_file = "tools/header-for-olaf.md"
    
    files_processed = process_skills_directory(skills_directory, header_file)
    
    print()
    print(f"Summary: {files_processed} skill.md files updated")
    print("Done!")
