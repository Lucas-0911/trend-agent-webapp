"""Platform adapters — lắng nghe sự kiện approval.granted và đăng lên từng nền tảng."""
from core.event_bus import bus


def register_platform_handlers():
    @bus.on("approval.granted")
    def on_approved(payload):
        platform = payload["data"].get("platform")
        if platform == "tiktok":
            # TODO: gọi TikTok Content Posting API
            bus.emit("post.published", {"platform": "tiktok", "content_id": payload["data"].get("content_id")}, "tiktok")
        elif platform == "instagram":
            # TODO: Meta Graph API
            bus.emit("post.published", {"platform": "instagram", "content_id": payload["data"].get("content_id")}, "instagram")
        elif platform == "facebook":
            # TODO: Meta Graph API
            bus.emit("post.published", {"platform": "facebook", "content_id": payload["data"].get("content_id")}, "facebook")
