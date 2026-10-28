# Trend Agent — Agent Architecture

Hệ thống theo hướng agent. Mỗi bước là một agent riêng, Orchestrator điều phối.

## Cấu trúc

```
.
├── main.py
├── config.py
├── db.py
├── routes.py
├── index.html
├── agents/
│   ├── base.py
│   ├── crawl_agent.py
│   ├── scoring_agent.py
│   ├── analysis_agent.py
│   └── orchestrator.py
└── requirements.txt
```

## Luồng

1. CrawlAgent — đọc MediaCrawler, chuẩn hóa
2. ScoringAgent — Jev hoặc laya-mlx
3. AnalysisAgent — gợi ý video theo nền tảng
4. Orchestrator — điều phối

## Chạy

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
