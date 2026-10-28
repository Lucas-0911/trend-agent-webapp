# Trend Agent — Hướng dẫn cho Hermes

## Cài đặt

```bash
hermes profiles create trend
cp skills/AGENT.md ~/.hermes/profiles/trend/
cp -r skills/trend-pipeline ~/.hermes/profiles/trend/skills/
cp skills/MEDIACRAWLER.md ~/.hermes/profiles/trend/skills/
```

## MediaCrawler

```bash
git clone https://github.com/NanmiCoder/MediaCrawler.git
cd MediaCrawler
uv sync
uv run playwright install
uv run main.py --platform dy --lt qrcode --type search

export MEDIACRAWLER_PATH=~/MediaCrawler
```

Chi tiết: `skills/MEDIACRAWLER.md`

## Chạy

```bash
hermes --profile trend
```

Nói: `chạy trend pipeline`
