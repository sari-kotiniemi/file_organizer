# Python File Organizer

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/sari-kotiniemi/file_organizer)](https://github.com/sari-kotiniemi/file_organizer/commits/main)

A simple script to organize files into folders by type.

## Features

- Organizes files by extension (Images, Documents, Audio, Code, etc.)
- Prevents filename collisions (`file.txt` -> `file_1.txt`)
- Supports recursive mode
- Supports dry-run preview
- Uses only Python standard library

## Run

```bash
python file_organizer.py [folder] [--recursive] [--dry-run]
```

### Example

```bash
python file_organizer.py "C:\Users\You\Downloads" --dry-run
```

## Options

- `folder` (optional): target folder (default: current folder)
- `-r, --recursive`: include files in subfolders
- `--dry-run`: preview without moving files

## Categories

Default groups: Images, Documents, Spreadsheets, Presentations, Audio, Video, Archives, Code, Other.

You can customize them in `FILE_CATEGORIES` inside `file_organizer.py`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.