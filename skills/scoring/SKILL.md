# Scoring Agent Skill

## Purpose
Score a product/trend with Jev API or local laya-mlx.

## When to use
- "score this product"
- "check if this trend is worth selling"

## Input
```json
{ "item": "...", "domain": "grocery", "source": "douyin", "use_local": false }
```

## Output
```json
{ "passed": true, "answers": {}, "model": "jev" }
```

## Implementation
Call ScoringAgent().run(context) or POST /api/score

## Notes
Set USE_LAYA_MLX=true on Apple Silicon for local model.
