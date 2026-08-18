from __future__ import annotations

import shutil
import argparse
from pathlib import Path


FILE_CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".md"},
    "Spreadsheets": {".xls", ".xlsx", ".csv"},
    "Presentations": {".ppt", ".pptx"},
    "Audio": {".mp3", ".wav", ".aac", ".flac", ".ogg"},
    "Video": {".mp4", ".mkv", ".mov", ".avi", ".wmv", ".webm"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".java",
        ".c",
        ".cpp",
        ".cs",
        ".go",
        ".php",
        ".html",
        ".css",
        ".json",
        ".yml",
        ".yaml",
        ".xml",
        ".sql",
    },
}


def category_for(file_path: Path) -> str:
    extension = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"


def unique_destination_path(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem}_{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def iter_files(folder: Path, recursive: bool):
    iterator = folder.rglob("*") if recursive else folder.iterdir()
    for item in iterator:
        if item.is_file():
            yield item


def organize(folder: Path, recursive: bool, dry_run: bool) -> tuple[int, int]:
    moved = 0
    skipped = 0

    for file_path in list(iter_files(folder, recursive)):
        if file_path.parent == folder and file_path.name == "file_organizer.py":
            skipped += 1
            continue

        category = category_for(file_path)
        destination_dir = folder / category
        destination = unique_destination_path(destination_dir / file_path.name)

        if destination == file_path:
            skipped += 1
            continue

        if dry_run:
            print(f"[DRY RUN] {file_path} -> {destination}")
            moved += 1
            continue

        destination_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(destination))
        print(f"Moved: {file_path.name} -> {category}/{destination.name}")
        moved += 1

    return moved, skipped


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organize files in a folder into category subfolders."
    )
    parser.add_argument(
        "folder",
        nargs="?",
        default=".",
        help="Folder to organize (default: current directory).",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Include files in subfolders.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview moves without changing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    folder = Path(args.folder).expanduser().resolve()

    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {folder}")

    moved, skipped = organize(folder, recursive=args.recursive, dry_run=args.dry_run)
    print(f"\nDone. Files moved: {moved}, skipped: {skipped}")
    print("Organization ready.")


if __name__ == "__main__":
    main()