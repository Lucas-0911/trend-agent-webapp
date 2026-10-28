# Crawl Agent Skill

## Purpose
Scan MediaCrawler data folders and return normalized, deduplicated items.

## When to use
- "scan crawler data"
- "get hot items from mediacrawler"
- "normalize crawled products"

## Input
Optional: mediacrawler_path (default from env)

## Output
```json
{ "items": [{ "name": "...", "description": "...", "source": "dy" }], "count": 12 }
```

## Implementation
Call CrawlAgent().run({}) or GET /api/scan

## Notes
Safe to call from Hermes or OpenClaw as a tool.
