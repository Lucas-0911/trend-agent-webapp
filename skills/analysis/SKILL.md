# Analysis Agent Skill

## Purpose
Produce platform-specific video suggestions for a passed item.

## When to use
- "suggest video ideas for this product"
- "how to make content for tiktok facebook youtube"

## Input
```json
{ "item": "...", "answers": { "sell_potential": {}, "low_risk": {} } }
```

## Output
Platforms: TikTok/Reels, Facebook/Zalo, YouTube Shorts, Instagram
Each with hook, structure, tips.

## Implementation
Call AnalysisAgent().run(context) or POST /api/analyze
