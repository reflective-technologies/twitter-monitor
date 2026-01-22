# Markdown Digest Renderer

A Python-based markdown renderer that displays your Twitter digests in a beautiful, styled format matching your React component design.

## Features

- **Styled rendering** with the same color scheme and typography as your React app
- **Auto-opens in browser** for instant viewing
- **Supports all markdown features**: headers, lists, tables, blockquotes, links, inline code, bold, italic
- **Responsive layout** with a clean, readable design

## Quick Start

### View most recent digest

```bash
python3 scripts/open_digest.py
```

### View specific digest

```bash
python3 scripts/view_digest.py twitter-digest.md
python3 scripts/view_digest.py data/digest_2026-01-22.md
```

### Save HTML output

```bash
python3 scripts/view_digest.py twitter-digest.md --output digest.html
```

## Usage in Code

```python
from scripts.markdown_renderer import render_and_open

# Read your digest
with open("data/digest_2026-01-22.md") as f:
    markdown = f.read()

# Render and open in browser
html_path = render_and_open(markdown, title="My Twitter Digest")
print(f"Opened: {html_path}")
```

## Styling

The renderer uses the exact same color scheme as your React component:

- **Background**: `#FDFDFC` (off-white)
- **Text**: `#2E2E2E` (near-black)
- **Gray tones**: `#F2F2F2` (light gray), `#989897` (mid gray)
- **Font**: Inter with system font fallbacks

## Integration with Digest Generation

After generating a digest, automatically open it:

```python
import subprocess
from scripts.markdown_renderer import render_and_open

# Generate digest (your existing code)
subprocess.run(["python3", "scripts/cluster_hybrid.py", "data/tweets.json"])

# Read and display
with open("data/digest_2026-01-22.md") as f:
    render_and_open(f.read())
```

## Files

| File                   | Purpose                             |
| ---------------------- | ----------------------------------- |
| `markdown_renderer.py` | Core rendering engine               |
| `view_digest.py`       | CLI tool to view specific digest    |
| `open_digest.py`       | CLI tool to open most recent digest |

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)
