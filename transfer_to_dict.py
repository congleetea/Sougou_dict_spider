#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to batch convert sougou scel files to fcitx5 pinyin dict format.
This includes both the file collection step (find) and the conversion step.
"""

import pathlib
import subprocess
import argparse
import os
import sys
import shutil
from typing import List, Optional


def collect_scel_files(
    source_dir: str,
    target_dir: str,
    exclude_patterns: Optional[List[str]] = None
) -> List[pathlib.Path]:
    """
    Collect all .scel files from source directory and copy them to target directory.

    Args:
        source_dir: Directory to search for .scel files
        target_dir: Directory to copy .scel files to
        exclude_patterns: List of path patterns to exclude

    Returns:
        List of collected .scel file paths
    """
    source_path = pathlib.Path(source_dir)
    target_path = pathlib.Path(target_dir)
    target_path.mkdir(exist_ok=True)

    if exclude_patterns is None:
        exclude_patterns = []

    scel_files = []
    for file_path in source_path.rglob("*.scel"):
        # Check if file path matches any exclude pattern
        should_exclude = False
        for pattern in exclude_patterns:
            if pattern in str(file_path):
                should_exclude = True
                break

        if not should_exclude:
            target_file = target_path / file_path.name
            # Copy file to target directory
            import shutil
            shutil.copy2(file_path, target_file)
            scel_files.append(target_file)
            print(f"Copied: {file_path} -> {target_file}")

    print(f"Collected {len(scel_files)} .scel files to {target_dir}")
    return scel_files


def convert_scel_to_dict(scel_dir: str, txt_dir: str, dict_dir: str):
    """
    Convert .scel files to .dict format via .txt intermediate format.

    Args:
        scel_dir: Directory containing .scel files
        txt_dir: Directory for intermediate .txt files
        dict_dir: Directory for final .dict files
    """
    scel_path = pathlib.Path(scel_dir)
    txt_path = pathlib.Path(txt_dir)
    dict_path = pathlib.Path(dict_dir)

    # Create directories if they don't exist
    txt_path.mkdir(exist_ok=True)
    dict_path.mkdir(exist_ok=True)

    print("Step 1: Converting .scel to .txt using scel2org5...")
    # Convert .scel to .txt
    scel_files = list(scel_path.glob("*.scel"))
    for file in scel_files:
        txt_file = txt_path / f"{file.stem}.txt"
        print(f"Converting {file} to {txt_file}")
        result = subprocess.run([
            "scel2org5",
            str(file),
            "-o",
            str(txt_file)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error converting {file}: {result.stderr}")
        else:
            print(f"Successfully converted {file}")

    print("Step 2: Converting .txt to .dict using libime_pinyindict...")
    # Convert .txt to .dict
    txt_files = list(txt_path.glob("*.txt"))
    for file in txt_files:
        dict_file = dict_path / f"{file.stem}.dict"
        print(f"Converting {file} to {dict_file}")
        result = subprocess.run([
            "libime_pinyindict",
            str(file),
            str(dict_file)
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error converting {file}: {result.stderr}")
        else:
            print(f"Successfully converted {file} to {dict_file}")


def copy_dict_files_to_fcitx5(dict_dir: str, fcitx5_dir: str = "~/.local/share/fcitx5/pinyin/dictionaries/"):
    """
    Copy .dict files to fcitx5 dictionaries directory.

    Args:
        dict_dir: Directory containing .dict files
        fcitx5_dir: Target fcitx5 dictionaries directory (default: ~/.local/share/fcitx5/pinyin/dictionaries/)
    """
    dict_path = pathlib.Path(dict_dir)
    expanded_fcitx5_dir = pathlib.Path(fcitx5_dir).expanduser()

    # Create fcitx5 directory if it doesn't exist
    expanded_fcitx5_dir.mkdir(parents=True, exist_ok=True)

    dict_files = list(dict_path.glob("*.dict"))
    if not dict_files:
        print(f"No .dict files found in {dict_dir}")
        return

    copied_count = 0
    for dict_file in dict_files:
        target_file = expanded_fcitx5_dir / dict_file.name
        print(f"Copying {dict_file} to {target_file}")
        shutil.copy2(dict_file, target_file)
        copied_count += 1

    print(f"Successfully copied {copied_count} .dict files to {expanded_fcitx5_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Batch convert sougou scel files to fcitx5 pinyin dict format"
    )
    parser.add_argument(
        "--source-dir",
        default="/home/xuancong/sogou/ciku",  # Same as SavePath in main.py
        help="Source directory to search for .scel files (default: /home/xuancong/sogou/ciku)"
    )
    parser.add_argument(
        "--collect-target",
        default="scel/",
        help="Target directory for collected .scel files (default: scel/)"
    )
    parser.add_argument(
        "--txt-dir",
        default="txt/",
        help="Directory for intermediate .txt files (default: txt/)"
    )
    parser.add_argument(
        "--dict-dir",
        default="dict/",
        help="Directory for final .dict files (default: dict/)"
    )
    parser.add_argument(
        "--exclude-patterns",
        nargs="*",
        default=["/436/", "/403/"],
        help="Path patterns to exclude (default: ['/436/', '/403/'])"
    )
    parser.add_argument(
        "--no-collect",
        action="store_true",
        help="Skip the collection step and only perform conversion"
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Skip copying .dict files to fcitx5 directory"
    )
    parser.add_argument(
        "--fcitx5-dir",
        default="~/.local/share/fcitx5/pinyin/dictionaries/",
        help="Target fcitx5 dictionaries directory (default: ~/.local/share/fcitx5/pinyin/dictionaries/)"
    )

    args = parser.parse_args()

    if not args.no_collect:
        print(f"Collecting .scel files from {args.source_dir} to {args.collect_target}")
        print(f"Excluding patterns: {args.exclude_patterns}")
        collect_scel_files(
            args.source_dir,
            args.collect_target,
            args.exclude_patterns
        )

    print(f"Converting files in {args.collect_target} to dict format...")
    convert_scel_to_dict(args.collect_target, args.txt_dir, args.dict_dir)

    print(f"Conversion complete! .dict files are in {args.dict_dir}")

    if not args.no_copy:
        print(f"Copying .dict files to fcitx5 directory: {args.fcitx5_dir}")
        copy_dict_files_to_fcitx5(args.dict_dir, args.fcitx5_dir)
        print("Process complete! Restart fcitx5 to use the new dictionaries.")
    else:
        print("To use these files, copy them to ~/.local/share/fcitx5/pinyin/dictionaries/ or run without --no-copy")


if __name__ == "__main__":
    main()