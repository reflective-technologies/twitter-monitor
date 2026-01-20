# Installing Twitter Monitor

> **Note to installing agent**: Use the question tool to present multiple choice options whenever you need user input. This makes installation easier.

## What This Does

AI-powered Twitter timeline analysis. Fetches your X/Twitter home timeline via internal GraphQL API, clusters tweets by topic using semantic embeddings, and generates narrative digests with cited sources.

## Prerequisites

- Python 3.10+
- An X/Twitter account (for auth tokens)
- Claude Code or Claude API access (for summarization)

## Installation

1. Copy the project files to your desired location

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install sentence-transformers hdbscan
   ```

## Configuration

### Environment Variables

This app requires X/Twitter authentication tokens. These must be extracted from a logged-in browser session:

1. Open x.com and log in
2. Open DevTools (F12) → Application → Cookies → `https://x.com`
3. Copy these cookie values:
   - `auth_token` (40 character hex string)
   - `ct0` (128 character hex string)

4. Set as environment variables:
   ```bash
   export X_AUTH_TOKEN="your_auth_token_here"
   export X_CT0="your_ct0_token_here"
   ```

**Note:** These tokens expire periodically. If you get 401 errors, re-extract from browser.

See `docs/x-api-reverse-engineering.md` for detailed instructions.

## Running the App

### Full Pipeline

```bash
# Fetch 1000 tweets and cluster them
python scripts/generate_digest.py --fetch --count 1000
```

### Step by Step

```bash
# 1. Fetch tweets
python scripts/fetch_timeline.py --count 1000 --output data/tweets.json

# 2. Extract topics and deduplicate
python scripts/extract_topics.py data/tweets.json --output data/enriched.json

# 3. Cluster by topic
python scripts/cluster_and_summarize.py data/enriched.json --output data/clusters/
```

### Summarization

After clustering, summarize each cluster using Claude:
- **Option A**: Use Claude Code to read each cluster file in `data/clusters/` and summarize
- **Option B**: Use Claude API directly on each cluster file

## Output

- `data/tweets.json` — Raw fetched tweets
- `data/enriched.json` — Tweets with extracted topics and metadata
- `data/clusters/*.txt` — Topic clusters ready for LLM summarization
- Final digest with citations linking to source tweets

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `fetch_timeline.py` | Fetch tweets from X's GraphQL API |
| `extract_topics.py` | Extract topics and deduplicate tweets |
| `cluster_and_summarize.py` | Cluster tweets by topic |
| `generate_digest.py` | Run the full pipeline |
