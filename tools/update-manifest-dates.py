#!/usr/bin/env python3
"""
Script to update the "updated" field in all skill-manifest.json files to today's date.
"""

import os
import json
from pathlib import Path
from datetime import datetime

def update_manifest_date(file_path, today_date):
    """Update the updated field in a manifest.json file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_date = data.get('metadata', {}).get('updated', 'Not found')
        
        # Update the date in the metadata section
        if 'metadata' in data and 'updated' in data['metadata']:
            data['metadata']['updated'] = today_date
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, original_date, today_date
        
        return False, original_date, "No updated field"
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False, "Error", str(e)

def process_skills_directory(skills_dir):
    """Process all skill-manifest.json files."""
    skills_path = Path(skills_dir)
    today_date = datetime.now().strftime('%Y-%m-%d')
    total_files_processed = 0
    
    print(f"Updating manifest files to date: {today_date}")
    print()
    
    # Process all skill-manifest.json files in skills directory and subdirectories
    for manifest_file in skills_path.rglob("skill-manifest.json"):
        if manifest_file.is_file():
            processed, old_date, new_date = update_manifest_date(manifest_file, today_date)
            if processed:
                total_files_processed += 1
                print(f"Updated: {manifest_file.relative_to(skills_path)}")
                print(f"  {old_date} → {new_date}")
            else:
                print(f"Skipped: {manifest_file.relative_to(skills_path)} ({new_date})")
    
    return total_files_processed

if __name__ == "__main__":
    skills_directory = "skills"
    
    print("Updating skill-manifest.json files...")
    print(f"Processing directory: {skills_directory}")
    print()
    
    files_processed = process_skills_directory(skills_directory)
    
    print()
    print(f"Summary: {files_processed} manifest files updated")
    print("Done!")
