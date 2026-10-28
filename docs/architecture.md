# Kiến trúc Event-Driven — Trend Agent WebApp

## Tổng quan

Hệ thống mở rộng từ Trend Agent hiện tại theo hướng **event-driven** để hỗ trợ tự động hóa nội dung đa nền tảng (TikTok, Instagram, Facebook) với một Trung tâm Hot Trend.

```
trend.detected
    ↓
content.requested
    ↓
content.generated
    ↓
approval.requested
    ↓
approval.granted
    ↓
post.published
```

## Sự kiện chính

| Sự kiện | Nguồn | Người lắng nghe | Mô tả |
|---------|-------|------------------|-------|
| `trend.detected` | Crawl / Trends | Content Engine, Dashboard | Xu hướng mới được phát hiện |
| `content.generated` | Content Engine | Approval, Dashboard | Nội dung (script/video) đã tạo |
| `approval.granted` | Approval Gate | Platform Adapters | Người dùng đã phê duyệt |
| `post.published` | Platform Adapter | Analytics, Dashboard | Đăng thành công lên nền tảng |
| `analytics.collected` | Analytics | Learning / Dashboard | Dữ liệu hiệu suất |

## Tối ưu theo nền tảng

- **TikTok**: Vertical 9:16, hook 3 giây đầu, trending sound, velocity cao.
- **Instagram**: Reels + aesthetic, cover đẹp, hashtag mix, CTA lưu bài.
- **Facebook**: Reach rộng, nhóm, caption thân thiện, có thể dài hơn.

## Tích hợp với code hiện tại

- `agents/orchestrator.py` có thể phát sự kiện sau khi scoring/analysis.
- Endpoint `/api/analyze` đã có gợi ý theo nền tảng — có thể nâng cấp thành phát `content.generated`.
- Event Bus nằm tại `core/event_bus.py` (singleton `bus`).

## Mở rộng

- Thêm platform adapter trong `platforms/` lắng nghe `approval.granted`.
- Dashboard có thể gọi `/api/events` để hiển thị lịch sử sự kiện.
