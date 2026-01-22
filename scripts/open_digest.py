#!/usr/bin/env python3
"""
Utility to open the most recent digest in browser.

Usage:
    python scripts/open_digest.py                    # Opens most recent digest
    python scripts/open_digest.py specific-file.md   # Opens specific file
"""

import sys
from pathlib import Path
from markdown_renderer import render_and_open


def find_most_recent_digest(data_dir: Path = None) -> Path:
    """Find the most recent digest file."""
    if data_dir is None:
        data_dir = Path(__file__).parent.parent / "data"

    # Look for digest_*.md files
    digest_files = list(data_dir.glob("digest_*.md"))

    if not digest_files:
        # Fall back to root directory
        root_dir = Path(__file__).parent.parent
        digest_files = [
            f
            for f in root_dir.glob("*.md")
            if "digest" in f.name.lower() or "twitter" in f.name.lower()
        ]

    if not digest_files:
        raise FileNotFoundError("No digest files found")

    # Sort by modification time
    return max(digest_files, key=lambda p: p.stat().st_mtime)


def main():
    # If a file is provided, use it
    if len(sys.argv) > 1:
        digest_path = Path(sys.argv[1])
        if not digest_path.exists():
            print(f"Error: File not found: {digest_path}")
            sys.exit(1)
    else:
        # Find most recent
        try:
            digest_path = find_most_recent_digest()
            print(f"Opening most recent digest: {digest_path}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Read and render
    with open(digest_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Extract title
    title = "Twitter Digest"
    first_line = markdown_content.split("\n")[0]
    if first_line.startswith("# "):
        title = first_line[2:].strip()

    # Open in browser
    html_path = render_and_open(markdown_content, title=title)
    print(f"✓ Opened in browser: {html_path}")


if __name__ == "__main__":
    main()
