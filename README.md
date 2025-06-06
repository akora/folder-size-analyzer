# Folder Size Analyzer

A Python script that analyzes and displays directory sizes in a tree-like structure, showing the total size and number of files for each directory and its subdirectories.

## Features

- Displays directory structure in an easy-to-read tree format
- Shows size in human-readable format (B, KB, MB, GB, TB)
- Displays total file count for each directory
- Provides breakdown of file types and their counts
- Detects and tracks hidden files
- Supports limiting the depth of directory traversal
- Handles permission errors gracefully
- Sorts subdirectories alphabetically (case-insensitive)
- Follows symbolic links safely

## Requirements

- Python 3.x

## Installation

Clone this repository or download the `folder_size_analyzer.py` script.

```bash
git clone <repository-url>
cd folder-size-analyzer
```

## Usage

```bash
python3 folder_size_analyzer.py [path] [-d MAX_DEPTH]
```

### Arguments

- `path`: The directory to analyze (optional, defaults to current directory)
- `-d, --max-depth`: Maximum depth level to analyze (optional)

### Examples

1. Analyze current directory:

```bash
python3 folder_size_analyzer.py
```

1. Analyze a specific directory:

```bash
python3 folder_size_analyzer.py /path/to/directory
```

1. Analyze with maximum depth of 2:

```bash
python3 folder_size_analyzer.py -d 2
```

### Sample Output

```text
Analyzing directory tree from: /path/to/directory
================================================================================
my_project/ [1.25 GB, 1,234 files (.py:500, .js:300, .css:200, hidden:150, .json:84)]
├── src/ [850.5 MB, 789 files (.js:300, .css:200, .json:50, hidden:20)]
│   ├── components/ [250.2 MB, 123 files (.js:100, .css:20, .json:3)]
│   └── utils/ [600.3 MB, 666 files (.js:200, .css:180, .json:47, hidden:20)]
└── tests/ [400.5 MB, 445 files (.py:500, .json:34, hidden:130)]
    ├── unit/ [200.3 MB, 223 files (.py:250, .json:20, hidden:65)]
    └── integration/ [200.2 MB, 222 files (.py:250, .json:14, hidden:65)]
```

The output shows:

- Directory name followed by its total size
- Total number of files in the directory
- Breakdown of file types in parentheses (sorted by frequency)
- File types include regular extensions (e.g., .py, .js), hidden files, and files with no extension

## Error Handling

- The script gracefully handles permission errors and continues execution
- Symbolic links are not followed to prevent infinite loops
- Invalid paths or inaccessible directories are handled appropriately
