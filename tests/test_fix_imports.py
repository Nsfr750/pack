#!/usr/bin/env python3
"""
Script to fix imports in all Python files after moving from app/ to root.
"""
import os
import re
from pathlib import Path

def update_imports_in_file(file_path):
    """Update import statements in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update imports like 'from app.module' to 'from module'
        updated_content = re.sub(
            r'from\s+app\.(\w+)\s+import',
            r'from \1 import',
            content
        )
        
        # Update imports like 'import module' to 'import module'
        updated_content = re.sub(
            r'import\s+app\.(\w+)',
            r'import \1',
            updated_content
        )
        
        # Update relative imports if needed
        updated_content = re.sub(
            r'from\s+\.(\w+)\s+import',
            r'from \1 import',
            updated_content
        )
        
        if updated_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated imports in {file_path}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    updated_count = 0
    
    # Process all Python files in the project
    for py_file in Path('.').rglob('*.py'):
        if update_imports_in_file(str(py_file)):
            updated_count += 1
    
    print(f"\nUpdated imports in {updated_count} files.")

if __name__ == "__main__":
    main()
