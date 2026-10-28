# Trend Pipeline

## Purpose
Skill chính. Điều phối toàn bộ luồng agent: thu thập → chấm điểm → gợi ý nội dung.

## Triggers
- chạy trend pipeline
- soi sản phẩm hot
- soi trend hôm nay
- làm full flow
- tìm cái đáng bán

## Quy trình agent phải làm

### Bước 1 — Thu thập (Crawl)
- Kiểm tra có dữ liệu MediaCrawler không.
- Nếu có: đọc JSON/JSONL, chuẩn hóa, loại trùng.
- Nếu không: hỏi người dùng dán mô tả hoặc từ khóa.
- Giữ tối đa 10 item chất lượng cao.

### Bước 2 — Chấm điểm (Score)
Đánh giá:
- sell_potential: low / medium / high / very_high
- easy_to_source: hard / medium / easy
- low_risk: 0.0 – 1.0

Chỉ giữ khi sell_potential ≥ high và low_risk > 0.7.

### Bước 3 — Phân tích (Analyze)
Tạo gợi ý cho:
- TikTok / Reels (15–25s)
- Facebook / Zalo (20–40s)
- YouTube Shorts (30–50s)
- Instagram (Reel/carousel)

### Bước 4 — Trả kết quả
Tiếng Việt:
1. Item đã pass (kèm điểm)
2. Gợi ý video theo nền tảng
3. Việc nên làm ngay

## Quy tắc
- Không bỏ bước score.
- Không đề xuất item chưa pass.
- Không bịa số liệu.
