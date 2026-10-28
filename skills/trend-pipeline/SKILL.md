# Trend Pipeline

## Purpose
Điều phối toàn bộ luồng: Crawl → Score → Analyze.

## Triggers
- "chạy trend pipeline"
- "soi sản phẩm hot hôm nay"
- "làm full flow"

## Quy trình
1. Gọi trend-crawl → lấy danh sách item
2. Gọi trend-score → chỉ giữ item passed
3. Gọi trend-analyze → gợi ý video theo nền tảng
4. Tổng hợp kết quả tiếng Việt, ưu tiên hành động

## Quy tắc
Luôn đi đúng thứ tự. Không bỏ qua bước score.
