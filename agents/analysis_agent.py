"""Analysis Agent — platform-specific video suggestions."""
import json
from typing import Any, Dict
from agents.base import BaseAgent

class AnalysisAgent(BaseAgent):
    name = "analysis"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        item = context.get("item", "")
        scores = context.get("answers", {})
        name = item[:80]
        sell = scores.get("sell_potential", {}).get("score", "?")
        risk = scores.get("low_risk", {}).get("noul", 0)

        platforms = {
            "TikTok / Reels": {
                "duration": "15–25 giây",
                "hook": f"Sản phẩm này đang hot — {name[:40]} có đáng mua không?",
                "structure": "Hook 2s → Unboxing nhanh → Giá + điểm nổi bật → CTA",
                "tips": "Trending sound, chữ to, zoom cận."
            },
            "Facebook / Zalo": {
                "duration": "20–40 giây hoặc carousel",
                "hook": f"Mình vừa test {name[:30]} — kết quả thật",
                "structure": "Vấn đề → Giới thiệu → Demo → Giá",
                "tips": "Caption rõ, comment ghim."
            },
            "YouTube Shorts": {
                "duration": "30–50 giây",
                "hook": f"Review nhanh {name[:35]}",
                "structure": "Hook → Mở hộp → Điểm thực tế → Kết luận",
                "tips": "Subtitle, thumbnail chữ to."
            },
            "Instagram": {
                "duration": "Reel hoặc carousel",
                "hook": f"{name[:30]} — đáng thử?",
                "structure": "Hình đẹp → Điểm nổi bật → Giá → Lưu",
                "tips": "Ưu tiên hình ảnh đẹp."
            }
        }

        text = f"Sản phẩm: {name}\nĐiểm: sell={sell}, risk={risk:.2f}\n\nGợi ý theo nền tảng:\n"
        for p, info in platforms.items():
            text += f"\n[{p}]\n- {info['duration']}\n- Hook: {info['hook']}\n- {info['structure']}\n- {info['tips']}\n"

        return {
            "analysis": text,
            "platforms": platforms,
            "suggestions_json": json.dumps({"platforms": platforms}, ensure_ascii=False),
            "item": item,
            "answers": scores
        }
