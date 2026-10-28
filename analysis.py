"""Generate platform-specific video suggestions."""
import json

def build_platform_suggestions(item: str, scores: dict) -> dict:
    name = item[:80]
    sell = scores.get("sell_potential", {}).get("score", "?")
    risk = scores.get("low_risk", {}).get("noul", 0)

    platforms = {
        "TikTok / Reels": {
            "duration": "15–25 giây",
            "hook": f"Sản phẩm này đang hot — {name[:40]} có đáng mua không?",
            "structure": "Hook 2s → Unboxing nhanh → Giá + 1 điểm nổi bật → CTA",
            "tips": "Dùng trending sound, chữ to, zoom cận sản phẩm."
        },
        "Facebook / Zalo": {
            "duration": "20–40 giây hoặc carousel",
            "hook": f"Mình vừa test {name[:30]} — kết quả thật",
            "structure": "Vấn đề → Giới thiệu → Demo → Giá + nơi mua",
            "tips": "Caption rõ, comment ghim, dùng ảnh thật nếu không quay."
        },
        "YouTube Shorts": {
            "duration": "30–50 giây",
            "hook": f"Review nhanh {name[:35]} sau khi dùng thử",
            "structure": "Hook → Mở hộp → 2–3 điểm thực tế → Kết luận",
            "tips": "Có subtitle, thumbnail chữ to, kết bằng câu hỏi."
        },
        "Instagram": {
            "duration": "Reel 15–30s hoặc carousel",
            "hook": f"{name[:30]} — đáng để thử?",
            "structure": "Hình đẹp → Điểm nổi bật → Giá → Lưu lại",
            "tips": "Ưu tiên hình ảnh đẹp, hashtag vừa phải."
        }
    }

    analysis_text = f"Sản phẩm: {name}\nĐiểm: sell={sell}, risk={risk:.2f}\n\nGợi ý video theo nền tảng:\n"
    for p, info in platforms.items():
        analysis_text += f"\n[{p}]\n- Thời lượng: {info['duration']}\n- Hook: {info['hook']}\n- Cấu trúc: {info['structure']}\n- Mẹo: {info['tips']}\n"

    return {
        "analysis": analysis_text,
        "platforms": platforms,
        "suggestions_json": json.dumps({"platforms": platforms}, ensure_ascii=False)
    }
