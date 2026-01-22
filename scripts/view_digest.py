#!/usr/bin/env python3
"""
View a markdown digest in the browser with pretty styling.

Usage:
    python scripts/view_digest.py data/digest_2026-01-22.md
    python scripts/view_digest.py twitter-digest.md
"""

import argparse
import sys
from pathlib import Path
from markdown_renderer import render_and_open


def main():
    parser = argparse.ArgumentParser(description="View markdown digest in browser")
    parser.add_argument("digest_file", help="Path to markdown digest file")
    parser.add_argument(
        "--output", "-o", help="Optional: Save HTML to this path (default: temp file)"
    )
    args = parser.parse_args()

    # Read markdown file
    digest_path = Path(args.digest_file)
    if not digest_path.exists():
        print(f"Error: File not found: {digest_path}")
        sys.exit(1)

    print(f"Reading digest from: {digest_path}")
    with open(digest_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Extract title from first line if it's an h1
    title = "Twitter Digest"
    first_line = markdown_content.split("\n")[0]
    if first_line.startswith("# "):
        title = first_line[2:].strip()

    # Render and open
    html_path = render_and_open(markdown_content, title=title, output_file=args.output)

    print(f"✓ Opened in browser: {html_path}")


if __name__ == "__main__":
    main()
