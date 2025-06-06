#!/usr/bin/env python3

import os
from pathlib import Path
import argparse
from datetime import datetime

def get_directory_stats(directory):
    """Calculate the total size, file count, and file type breakdown of a directory including all subdirectories."""
    total_size = 0
    total_files = 0
    file_types = {}
    try:
        for entry in os.scandir(directory):
            try:
                if entry.is_file(follow_symlinks=False):
                    file_size = entry.stat().st_size
                    total_size += file_size
                    total_files += 1
                    
                    # Track file type
                    file_type = get_file_type(entry.name)
                    if file_type not in file_types:
                        file_types[file_type] = {'count': 0, 'size': 0}
                    file_types[file_type]['count'] += 1
                    file_types[file_type]['size'] += file_size
                    
                elif entry.is_dir(follow_symlinks=False):
                    subdir_size, subdir_files, subdir_types = get_directory_stats(entry.path)
                    total_size += subdir_size
                    total_files += subdir_files
                    
                    # Merge file type dictionaries
                    for ftype, stats in subdir_types.items():
                        if ftype not in file_types:
                            file_types[ftype] = {'count': 0, 'size': 0}
                        file_types[ftype]['count'] += stats['count']
                        file_types[ftype]['size'] += stats['size']
            except (PermissionError, OSError):
                continue
    except PermissionError:
        return 0, 0, {}
    return total_size, total_files, file_types

def get_file_type(filename):
    """Determine the type of file based on its name."""
    if filename.startswith('.'):
        return 'hidden'
    ext = os.path.splitext(filename)[1].lower()
    return ext[1:] if ext else 'no_extension'

def format_size(size):
    """Convert size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def print_directory_tree(directory, prefix="", is_last=True, base_path=None, current_depth=0, max_depth=None):
    """Print directory tree with sizes, file counts, and file type breakdown in a tree-like structure."""
    if max_depth is not None and current_depth > max_depth:
        return
        
    if base_path is None:
        base_path = directory
    
    size, file_count, file_types = get_directory_stats(directory)
    human_size = format_size(size)
    
    # Calculate relative path for display
    rel_path = os.path.relpath(directory, base_path) if directory != base_path else os.path.basename(directory)
    
    # Format file type breakdown
    type_breakdown = ""
    if file_count > 0:
        sorted_types = sorted(file_types.items(), key=lambda x: x[1]['count'], reverse=True)
        type_details = []
        for ftype, stats in sorted_types:
            type_name = "hidden" if ftype == "hidden" else f".{ftype}" if ftype != "no_extension" else "no_ext"
            type_details.append(f"{type_name}:{stats['count']}")
        type_breakdown = f" ({', '.join(type_details)})"
    
    # Create the tree branches
    if directory == base_path:
        print(f"{rel_path}/ [{human_size}, {file_count:,} files{type_breakdown}]")
    else:
        branch = "└── " if is_last else "├── "
        print(f"{prefix}{branch}{os.path.basename(directory)}/ [{human_size}, {file_count:,} files{type_breakdown}]")
    
    # Get list of subdirectories
    try:
        subdirs = [d for d in os.scandir(directory) if d.is_dir(follow_symlinks=False)]
        subdirs.sort(key=lambda x: x.name.lower())  # Sort alphabetically, case-insensitive
        
        for i, subdir in enumerate(subdirs):
            try:
                new_prefix = prefix + ("    " if is_last else "│   ")
                print_directory_tree(
                    subdir.path,
                    new_prefix,
                    i == len(subdirs) - 1,
                    base_path,
                    current_depth + 1,
                    max_depth
                )
            except (PermissionError, OSError):
                continue
    except (PermissionError, OSError):
        return

def main():
    parser = argparse.ArgumentParser(description='Analyze folder sizes recursively.')
    parser.add_argument('path', nargs='?', default='.', 
                      help='Starting path for analysis (default: current directory)')
    parser.add_argument('-d', '--max-depth', type=int,
                      help='Maximum depth level to analyze (default: unlimited)')
    args = parser.parse_args()
    
    start_path = os.path.abspath(args.path)
    print(f"\nAnalyzing directory tree from: {start_path}")
    if args.max_depth is not None:
        print(f"Maximum depth level: {args.max_depth}")
    print("=" * 80)
    
    print_directory_tree(start_path, max_depth=args.max_depth)

if __name__ == "__main__":
    main()
