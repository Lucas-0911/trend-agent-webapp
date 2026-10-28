# Trend Score

## Purpose
Chấm điểm sản phẩm/xu hướng bằng Jev API hoặc laya-mlx local.

## Triggers
- "chấm điểm"
- "score item"
- "jev đánh giá"
- "có đáng bán không"

## Tiêu chí
- sell_potential (low / medium / high / very_high)
- easy_to_source (hard / medium / easy)
- low_risk (noul)

**Pass khi:** sell_potential ≥ high và low_risk > 0.7

## Model
- USE_LAYA_MLX=true trên Apple Silicon → laya-mlx
- Ngược lại → Jev API

## Output
passed, scores, model, lý do ngắn
