# MediaCrawler — Hướng dẫn cho Trend Agent

Nguồn: https://github.com/NanmiCoder/MediaCrawler

Dùng để crawl dữ liệu từ Douyin, Xiaohongshu, Kuaishou, Bilibili, Weibo.
Trend Agent đọc kết quả trong thư mục `data/` sau khi crawl xong.

## Cài đặt

```bash
git clone https://github.com/NanmiCoder/MediaCrawler.git
cd MediaCrawler
uv sync
uv run playwright install
```

## Chạy crawl

```bash
cd MediaCrawler
uv run main.py --platform dy --lt qrcode --type search
```

- Lần đầu quét QR.
- Kết quả lưu trong `data/<platform>/`.

## Nối với Trend Agent

```bash
export MEDIACRAWLER_PATH=~/MediaCrawler
```

Agent sẽ đọc `$MEDIACRAWLER_PATH/data/` khi chạy pipeline.
