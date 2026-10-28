# Trend Agent

Kiến trúc đã tách module.

## Cấu trúc

```
.
├── main.py          # Entry point (FastAPI app)
├── config.py        # Cấu hình (path, API, flags)
├── db.py            # SQLite init + connection
├── crawler.py       # Quét + chuẩn hóa MediaCrawler
├── scoring.py       # Jev API hoặc laya-mlx
├── analysis.py      # Gợi ý video theo nền tảng
├── routes.py        # API endpoints
├── index.html       # Giao diện dark theme
└── requirements.txt
```

## Chạy

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Biến môi trường (tuỳ chọn)

```bash
export MEDIACRAWLER_PATH=~/MediaCrawler
export TYPESAFE_API_KEY=your_key
export USE_LAYA_MLX=true          # chỉ trên Apple Silicon
```
