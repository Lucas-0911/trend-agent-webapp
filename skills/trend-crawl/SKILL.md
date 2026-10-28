# Trend Crawl

## Purpose
Thu thập và chuẩn hóa dữ liệu xu hướng từ MediaCrawler hoặc từ người dùng.

## Triggers
- soi trend
- crawl dữ liệu
- tìm sản phẩm hot
- scan mediacrawler

## MediaCrawler
Nguồn: https://github.com/NanmiCoder/MediaCrawler
Xem chi tiết cài đặt trong `skills/MEDIACRAWLER.md`.

### Agent phải làm
1. Kiểm tra `$MEDIACRAWLER_PATH/data/` (mặc định `~/MediaCrawler/data`).
2. Đọc file `.json` và `.jsonl`.
3. Chuẩn hóa: name, description, source.
4. Loại trùng theo tên.
5. Ưu tiên item có review, unboxing, giá, mua.
6. Giữ 10–15 item tốt nhất.

## Nếu không có MediaCrawler
Hỏi người dùng dán mô tả hoặc từ khóa.

## Output
Danh sách item để đưa sang bước Score.
