#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime
import argparse
from typing import List, Set

# ANSI color codes
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Icons for different file types
ICONS = {
    'directory': '📁',
    'file': '📄',
    'python': '🐍',
    'image': '🖼️',
    'document': '📝',
    'archive': '📦',
    'config': '⚙️',
    'executable': '⚡',
}

# File extensions mapping
EXTENSIONS = {
    '.py': 'python',
    '.jpg': 'image',
    '.jpeg': 'image',
    '.png': 'image',
    '.gif': 'image',
    '.pdf': 'document',
    '.txt': 'document',
    '.md': 'document',
    '.zip': 'archive',
    '.tar': 'archive',
    '.gz': 'archive',
    '.json': 'config',
    '.yaml': 'config',
    '.yml': 'config',
    '.sh': 'executable',
    '.exe': 'executable',
}

def get_file_icon(file_path: str) -> str:
    """Get the appropriate icon for a file based on its extension."""
    ext = os.path.splitext(file_path)[1].lower()
    file_type = EXTENSIONS.get(ext, 'file')
    return ICONS.get(file_type, ICONS['file'])

def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"

def should_exclude(path: str, exclude_dirs: Set[str]) -> bool:
    """Check if the path should be excluded based on exclude patterns."""
    return any(excluded in path.split(os.sep) for excluded in exclude_dirs)

def generate_tree(
    start_path: str,
    exclude_dirs: Set[str],
    max_depth: int = None,
    current_depth: int = 0,
    prefix: str = '',
    is_last: bool = True
) -> None:
    """Generate and print the directory tree structure."""
    if max_depth is not None and current_depth > max_depth:
        return

    if should_exclude(start_path, exclude_dirs):
        return

    # Get directory contents
    try:
        entries = sorted(os.listdir(start_path))
    except PermissionError:
        print(f"{prefix}{Colors.RED}Permission denied: {start_path}{Colors.ENDC}")
        return

    # Filter out hidden files and directories
    entries = [e for e in entries if not e.startswith('.')]

    for i, entry in enumerate(entries):
        is_last_entry = i == len(entries) - 1
        path = os.path.join(start_path, entry)
        
        # Skip if it's an excluded directory
        if should_exclude(path, exclude_dirs):
            continue

        # Determine the prefix for the current entry
        current_prefix = prefix + ('    ' if is_last else '│   ')
        connector = '└── ' if is_last_entry else '├── '

        try:
            if os.path.isdir(path):
                # Directory
                print(f"{prefix}{connector}{Colors.BLUE}{ICONS['directory']} {entry}/{Colors.ENDC}")
                generate_tree(
                    path,
                    exclude_dirs,
                    max_depth,
                    current_depth + 1,
                    current_prefix,
                    is_last_entry
                )
            else:
                # File
                size = os.path.getsize(path)
                icon = get_file_icon(entry)
                print(f"{prefix}{connector}{Colors.GREEN}{icon} {entry}{Colors.ENDC} ({format_size(size)})")
        except (PermissionError, FileNotFoundError):
            print(f"{prefix}{connector}{Colors.RED}Error accessing: {entry}{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(description='Generate a directory tree structure')
    parser.add_argument('path', nargs='?', default='.', help='Path to generate tree for')
    parser.add_argument('-d', '--max-depth', type=int, help='Maximum depth of the tree')
    parser.add_argument('-e', '--exclude', nargs='+', default=['.git', '__pycache__', 'node_modules', 'venv'],
                      help='Directories to exclude')
    
    args = parser.parse_args()
    
    # Convert path to absolute path
    start_path = os.path.abspath(args.path)
    
    # Print header
    print(f"\n{Colors.BOLD}Project Tree Generator{Colors.ENDC}")
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Root path: {start_path}\n")
    
    # Generate and print the tree
    generate_tree(start_path, set(args.exclude), args.max_depth)

if __name__ == '__main__':
    main()
