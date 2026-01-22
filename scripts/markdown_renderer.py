#!/usr/bin/env python3
"""
Markdown renderer that matches the React MarkdownRenderer styling.
Opens rendered markdown in a browser window.
"""

import re
import webbrowser
import tempfile
import os
from html import escape
from typing import List, Tuple, Optional


class MarkdownRenderer:
    """Renders markdown to HTML with custom styling matching React component."""

    # Color scheme
    BG_COLOR = "#FDFDFC"
    TEXT_COLOR = "#2E2E2E"
    GRAY_LIGHT = "#F2F2F2"
    GRAY_MID = "#989897"

    def __init__(self):
        self.html_parts: List[str] = []

    def parse_inline(self, text: str) -> str:
        """Parse inline markdown (bold, italic, links, code)."""
        result = escape(text)

        # Bold + Italic (must come before bold and italic separately)
        result = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", result)

        # Bold
        result = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", result)

        # Italic
        result = re.sub(r"\*(.+?)\*", r"<em>\1</em>", result)

        # Links
        result = re.sub(
            r"\[([^\]]+)\]\(([^)]+)\)",
            r'<a href="\2" target="_blank" rel="noopener noreferrer" class="link">\1</a>',
            result,
        )

        # Inline code
        result = re.sub(r"`([^`]+)`", r'<code class="inline-code">\1</code>', result)

        return result

    def tokenize(self, markdown: str) -> List[dict]:
        """Tokenize markdown into structured blocks."""
        lines = markdown.split("\n")
        tokens = []
        i = 0

        while i < len(lines):
            line = lines[i]

            # Skip empty lines
            if not line.strip():
                i += 1
                continue

            # Horizontal rule
            if re.match(r"^---+$", line.strip()):
                tokens.append({"type": "hr"})
                i += 1
                continue

            # Headers
            h1_match = re.match(r"^# (.+)$", line)
            if h1_match:
                tokens.append({"type": "h1", "content": h1_match.group(1)})
                i += 1
                continue

            h2_match = re.match(r"^## (.+)$", line)
            if h2_match:
                tokens.append({"type": "h2", "content": h2_match.group(1)})
                i += 1
                continue

            h3_match = re.match(r"^### (.+)$", line)
            if h3_match:
                tokens.append({"type": "h3", "content": h3_match.group(1)})
                i += 1
                continue

            # Table
            if line.startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    row = [cell.strip() for cell in lines[i].split("|")[1:-1]]
                    # Skip separator rows
                    if not all(re.match(r"^[-:]+$", cell) for cell in row):
                        rows.append(row)
                    i += 1
                tokens.append({"type": "table", "rows": rows})
                continue

            # Unordered list
            if re.match(r"^- ", line):
                items = []
                while i < len(lines) and re.match(r"^- ", lines[i]):
                    items.append(re.sub(r"^- ", "", lines[i]))
                    i += 1
                tokens.append({"type": "ul", "items": items})
                continue

            # Blockquote
            if line.startswith(">"):
                content = re.sub(r"^>\s?", "", line)
                i += 1
                while i < len(lines) and lines[i].startswith(">"):
                    content += "\n" + re.sub(r"^>\s?", "", lines[i])
                    i += 1
                tokens.append({"type": "blockquote", "content": content})
                continue

            # Paragraph
            content = line
            i += 1
            while (
                i < len(lines)
                and lines[i].strip()
                and not re.match(r"^[#\-|>]", lines[i])
                and not re.match(r"^---+$", lines[i])
            ):
                content += " " + lines[i]
                i += 1
            tokens.append({"type": "paragraph", "content": content})

        return tokens

    def render_token(self, token: dict) -> str:
        """Render a single token to HTML."""
        token_type = token["type"]

        if token_type == "h1":
            return f'<h1 class="h1">{self.parse_inline(token["content"])}</h1>'

        elif token_type == "h2":
            return f'<h2 class="h2">{self.parse_inline(token["content"])}</h2>'

        elif token_type == "h3":
            return f'<h3 class="h3">{self.parse_inline(token["content"])}</h3>'

        elif token_type == "hr":
            return '<hr class="hr">'

        elif token_type == "ul":
            items_html = []
            for item in token["items"]:
                items_html.append(
                    f'<li class="li">'
                    f'<span class="bullet">•</span>'
                    f"<span>{self.parse_inline(item)}</span>"
                    f"</li>"
                )
            return f'<ul class="ul">{"".join(items_html)}</ul>'

        elif token_type == "table":
            rows = token["rows"]
            if not rows:
                return ""

            # Header row
            header_html = '<thead><tr class="table-header-row">'
            for cell in rows[0]:
                header_html += (
                    f'<th class="table-header-cell">{self.parse_inline(cell)}</th>'
                )
            header_html += "</tr></thead>"

            # Body rows
            body_html = "<tbody>"
            for i, row in enumerate(rows[1:]):
                is_last = i == len(rows) - 2
                row_class = (
                    "table-body-row"
                    if not is_last
                    else "table-body-row table-body-row-last"
                )
                body_html += f'<tr class="{row_class}">'
                for cell in row:
                    body_html += (
                        f'<td class="table-cell">{self.parse_inline(cell)}</td>'
                    )
                body_html += "</tr>"
            body_html += "</tbody>"

            return f'<div class="table-container"><table class="table">{header_html}{body_html}</table></div>'

        elif token_type == "blockquote":
            return f'<blockquote class="blockquote">{self.parse_inline(token["content"])}</blockquote>'

        elif token_type == "paragraph":
            return f'<p class="paragraph">{self.parse_inline(token["content"])}</p>'

        return ""

    def render(self, markdown: str) -> str:
        """Render markdown to HTML."""
        tokens = self.tokenize(markdown)
        html_parts = [self.render_token(token) for token in tokens]
        return "\n".join(html_parts)

    def create_html_document(self, markdown: str, title: str = "Twitter Digest") -> str:
        """Create a complete HTML document with styling."""
        content_html = self.render(markdown)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: {self.BG_COLOR};
            color: {self.TEXT_COLOR};
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            line-height: 1.5;
            min-height: 100vh;
        }}

        .container {{
            max-width: 768px;
            margin: 0 auto;
            padding: 3rem 1.5rem;
        }}

        /* Headers */
        .h1 {{
            font-size: 1.875rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: {self.TEXT_COLOR};
        }}

        .h2 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: {self.TEXT_COLOR};
        }}

        .h3 {{
            font-size: 1.125rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: {self.TEXT_COLOR};
        }}

        /* Horizontal rule */
        .hr {{
            margin: 1.5rem 0;
            border: 0;
            border-top: 1px solid {self.GRAY_LIGHT};
        }}

        /* Lists */
        .ul {{
            margin: 1rem 0;
            list-style: none;
        }}

        .li {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 0.375rem;
            line-height: 1.375;
            color: {self.TEXT_COLOR};
        }}

        .bullet {{
            color: {self.GRAY_MID};
            user-select: none;
        }}

        /* Table */
        .table-container {{
            margin: 1.5rem 0;
            overflow: hidden;
            border-radius: 0.5rem;
            border: 1px solid {self.GRAY_LIGHT};
        }}

        .table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .table-header-row {{
            background: {self.GRAY_LIGHT};
        }}

        .table-header-cell {{
            padding: 0.75rem 1rem;
            text-align: left;
            font-size: 0.875rem;
            font-weight: 600;
            color: {self.TEXT_COLOR};
        }}

        .table-body-row {{
            border-bottom: 1px solid {self.GRAY_LIGHT};
            transition: background-color 0.2s;
        }}

        .table-body-row:hover {{
            background: #FAFAFA;
        }}

        .table-body-row-last {{
            border-bottom: none;
        }}

        .table-cell {{
            padding: 0.75rem 1rem;
            font-size: 0.875rem;
            color: {self.TEXT_COLOR};
        }}

        /* Blockquote */
        .blockquote {{
            margin: 1rem 0;
            padding-left: 1rem;
            border-left: 2px solid {self.GRAY_MID};
            color: {self.GRAY_MID};
            font-style: italic;
        }}

        /* Paragraph */
        .paragraph {{
            margin: 0.75rem 0;
            line-height: 1.375;
            color: {self.TEXT_COLOR};
        }}

        /* Inline elements */
        .link {{
            color: {self.TEXT_COLOR};
            text-decoration: underline;
            text-underline-offset: 2px;
            transition: opacity 0.2s;
        }}

        .link:hover {{
            opacity: 0.7;
        }}

        .inline-code {{
            background: {self.GRAY_LIGHT};
            padding: 0.125rem 0.375rem;
            border-radius: 0.25rem;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
            font-size: 0.875rem;
        }}

        strong {{
            font-weight: 600;
        }}

        em {{
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content_html}
    </div>
</body>
</html>"""


def render_and_open(
    markdown_content: str,
    title: str = "Twitter Digest",
    output_file: Optional[str] = None,
) -> str:
    """
    Render markdown to HTML and open in browser.

    Args:
        markdown_content: Markdown string to render
        title: HTML page title
        output_file: Optional path to save HTML file. If None, uses temp file.

    Returns:
        Path to the HTML file
    """
    renderer = MarkdownRenderer()
    html = renderer.create_html_document(markdown_content, title)

    if output_file:
        html_path = output_file
    else:
        # Create temp file
        fd, html_path = tempfile.mkstemp(suffix=".html", prefix="digest_")
        os.close(fd)

    # Write HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    # Open in browser
    webbrowser.open(f"file://{os.path.abspath(html_path)}")

    return html_path


if __name__ == "__main__":
    # Test with sample markdown
    sample_markdown = """# Twitter Digest — Last 12 Hours
**500 tweets | 8 clusters | 3 viral highlights**

---

## AI Developments

**Key narrative or theme:**
- OpenAI announces GPT-5 with significant reasoning improvements [(source)](https://x.com/openai/status/123)
- New research shows emergent capabilities in smaller models [(source)](https://x.com/researcher/status/456)

---

## Viral Highlights

*High-engagement tweets that don't fit into topic clusters but clearly resonated:*

| Content | Likes | Source |
|---------|-------|--------|
| Hilarious cat video breaks the internet | 20.6k | [(source)](https://x.com/user/status/789) |

---

## Top Engagement

| Tweet | Likes | Link |
|-------|-------|------|
| "This is the way" - famous quote | 15k | [(source)](https://x.com/user/status/999) |
"""

    print("Opening sample digest in browser...")
    html_file = render_and_open(sample_markdown)
    print(f"Rendered to: {html_file}")
