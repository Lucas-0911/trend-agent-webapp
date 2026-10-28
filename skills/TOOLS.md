# OpenClaw / Hermes Tool Definitions

## Tools

### scan_crawler
- Description: Scan MediaCrawler data
- Returns: { items, count }

### score_item
- Parameters: item (required), domain, source, api_key, use_local
- Returns: { passed, answers, model }

### analyze_item
- Parameters: item, scores
- Returns: { analysis, platforms }

## Hermes
Copy skills/ into ~/.hermes/profiles/<profile>/skills/

## OpenClaw
Register the three tools and point them to Orchestrator methods or HTTP endpoints.
