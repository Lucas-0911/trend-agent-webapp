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
├── core/
│   └── event_bus.py          ← Event Bus (event-driven)
├── platforms/
│   └── handlers.py           ← Adapter TikTok / Instagram / Facebook
├── docs/
│   └── architecture.md       ← Kiến trúc event-driven
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

## Kiến trúc Event-Driven

Hệ thống đã được mở rộng theo hướng sự kiện để hỗ trợ tự động hóa nội dung đa nền tảng (TikTok, Instagram, Facebook).

Xem chi tiết: [docs/architecture.md](docs/architecture.md)

Luồng chính:
`trend.detected` → `content.generated` → `approval.granted` → `post.published`

## Gắn Hermes
```bash
cp -r skills/* ~/.hermes/profiles/<profile>/skills/
```

## Gắn OpenClaw
Đăng ký 3 tool trong skills/TOOLS.md.

## Seedline

Web studio nằm cùng repo này. Dán ghi chú trend, tách concept, rồi tạo ảnh in phẳng (title, mô tả, tag đi kèm). Agent Python phía trên giữ nguyên.

```bash
npm install
npm run dev
```
