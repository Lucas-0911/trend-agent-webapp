# Trend Agent WebApp

MediaCrawler → chấm điểm (Jev / laya-mlx) → lưu DB → gợi ý video theo nền tảng.

## Tính năng mới
Sau khi item đạt điểm, app gợi ý cách làm video phù hợp cho:
- TikTok / Reels
- Facebook / Zalo
- YouTube Shorts
- Instagram

Mỗi nền tảng có: thời lượng, hook, cấu trúc, mẹo.

## Chạy
```bash
git pull
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
