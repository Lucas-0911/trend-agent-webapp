# Trend Crawl

## Purpose
Thu thập và chuẩn hóa dữ liệu xu hướng / sản phẩm hot.

## Triggers
- "soi trend"
- "crawl dữ liệu"
- "tìm sản phẩm hot"
- "scan mediacrawler"

## Steps
1. Kiểm tra thư mục MediaCrawler.
2. Nếu có file JSON/JSONL → đọc, chuẩn hóa, loại trùng.
3. Nếu không có → hỏi người dùng dán mô tả.
4. Trả về danh sách item rõ ràng.

## Output
- name, description, source

## Notes
Không bịa dữ liệu. Ưu tiên item có tín hiệu review/unboxing/giá.
