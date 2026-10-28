# Trend Agent — Agent + Skill Architecture

Chạy độc lập và gắn được vào Hermes Agent hoặc OpenClaw.

## Cấu trúc

```
.
├── main.py
├── config.py
├── db.py
├── routes.py
├── agents/
│   ├── base.py
│   ├── crawl_agent.py
│   ├── scoring_agent.py
│   ├── analysis_agent.py
│   └── orchestrator.py
├── skills/
│   ├── crawl/SKILL.md
│   ├── scoring/SKILL.md
│   ├── analysis/SKILL.md
│   └── TOOLS.md
├── index.html
└── requirements.txt
```

## Chạy webapp
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Gắn Hermes
```bash
cp -r skills/* ~/.hermes/profiles/<profile>/skills/
```

## Gắn OpenClaw
Đăng ký 3 tool trong skills/TOOLS.md.
