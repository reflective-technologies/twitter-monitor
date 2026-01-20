# Twitter Monitor

AI-powered Twitter timeline analysis with semantic clustering. Fetches your home timeline via X's internal API, clusters tweets by topic using embeddings, and generates narrative digests with cited sources.

## Features

- **Fetch tweets** via X's internal GraphQL API (no official API access needed)
- **Semantic clustering** using sentence-transformers embeddings + K-means
- **Parallel summarization** with Claude for efficient processing
- **Verified citations** — every claim links to the source tweet

## Quick Start

```bash
# 1. Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install sentence-transformers hdbscan

# 2. Set auth tokens (see docs/x-api-reverse-engineering.md)
export X_AUTH_TOKEN="your_auth_token"
export X_CT0="your_ct0_token"

# 3. Fetch tweets
python scripts/fetch_timeline.py --count 1000 --output data/tweets.json

# 4. Cluster with embeddings
python scripts/cluster_embeddings.py data/tweets.json --output data/clusters/

# 5. Summarize clusters (via Claude Code or API)
```

## Architecture

```
Raw tweets (5000)
    │
    ▼
Deduplicate → 2287 unique
    │
    ▼
Embed with all-MiniLM-L6-v2 (local, ~3 sec)
    │
    ▼
K-means clustering → 20 topic clusters
    │
    ▼
Parallel LLM summarization (one per cluster)
    │
    ▼
Merge into final digest with verified citations
```

### Why Semantic Clustering?

| Approach | Problem |
|----------|---------|
| Arbitrary chunks | Splits related tweets across chunks |
| Keyword matching | Misses semantic similarity ("Claude" vs "Anthropic's model") |
| **Embeddings** | Groups by meaning, finds natural topics |

## Scripts

| Script | Purpose |
|--------|---------|
| `fetch_timeline.py` | Fetch tweets from X's GraphQL API |
| `extract_topics.py` | Lightweight topic extraction via regex |
| `cluster_embeddings.py` | Semantic clustering with embeddings |
| `cluster_and_summarize.py` | Keyword-based clustering (simpler) |
| `generate_digest.py` | Orchestrates the full pipeline |

## Getting Auth Tokens

1. Open x.com and log in
2. DevTools → Application → Cookies → `https://x.com`
3. Copy `auth_token` and `ct0` values
4. Set as environment variables

See [docs/x-api-reverse-engineering.md](docs/x-api-reverse-engineering.md) for details.

## Output

The pipeline generates:
- `data/tweets.json` — Raw fetched tweets
- `data/clusters/*.txt` — Topic clusters ready for summarization
- `twitter-digest-v2.md` — Final narrative digest with citations

Example citation format:
```markdown
Trump has been posting AI-generated images of himself taking over Greenland
[source](https://x.com/harryjsisson/status/2013502243362803807)
```

## Sample Digest

See [twitter-digest-v2.md](twitter-digest-v2.md) for a full example analyzing 2,046 tweets across 20 semantic clusters.

## License

MIT
