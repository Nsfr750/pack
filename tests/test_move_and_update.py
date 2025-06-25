#!/usr/bin/env python3
"""
Script to move Python files from app/ to project root and update imports.
"""
import os
import re
import shutil
from pathlib import Path

def move_files():
    """Move all Python files from app/ to project root."""
    app_dir = Path('app')
    root_dir = Path('.')
    
    # Move all .py files from app/ to root
    for py_file in app_dir.glob('*.py'):
        dest = root_dir / py_file.name
        if dest.exists():
            print(f"Skipping {py_file.name} as it already exists in root")
            continue
        shutil.move(str(py_file), str(dest))
        print(f"Moved {py_file} to {dest}")

def update_imports_in_file(file_path):
    """Update import statements in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update imports like 'from app.module' to 'from module'
    updated_content = re.sub(
        r'from\s+app\.(\w+)\s+import',
        r'from \1 import',
        content
    )
    
    # Update imports like 'import app.module' to 'import module'
    updated_content = re.sub(
        r'import\s+app\.(\w+)',
        r'import \1',
        updated_content
    )
    
    if updated_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"Updated imports in {file_path}")

def update_all_imports():
    """Update imports in all Python files in the project."""
    # Update files in root directory
    for py_file in Path('.').glob('*.py'):
        if py_file.name != 'move_and_update.py':
            update_imports_in_file(py_file)
    
    # Update files in test directory
    test_dir = Path('test')
    if test_dir.exists():
        for py_file in test_dir.glob('*.py'):
            update_imports_in_file(py_file)

def main():
    print("Moving files from app/ to project root...")
    move_files()
    
    print("\nUpdating imports in all Python files...")
    update_all_imports()
    
    print("\nDone! You may now delete the app/ directory if it's empty.")

if __name__ == "__main__":
    main()
