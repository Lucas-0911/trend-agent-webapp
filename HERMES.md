# Trend Agent Skills for Hermes

Copy thư mục skills vào Hermes để agent tự thực hiện luồng trend.

## Cài nhanh

```bash
hermes profiles create trend
cp -r skills/trend-* ~/.hermes/profiles/trend/skills/
hermes --profile trend
```

Nói: `chạy trend pipeline`

## Skills

- **trend-crawl** — thu thập / chuẩn hóa dữ liệu
- **trend-score** — chấm điểm Jev hoặc laya-mlx
- **trend-analyze** — gợi ý video theo nền tảng
- **trend-pipeline** — chạy full flow

## Biến môi trường

```bash
export TYPESAFE_API_KEY=...
export USE_LAYA_MLX=true
export MEDIACRAWLER_PATH=~/MediaCrawler
```
