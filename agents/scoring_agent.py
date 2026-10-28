"""Scoring Agent — Jev or local laya-mlx."""
import json
import requests
from typing import Any, Dict
from fastapi import HTTPException
from agents.base import BaseAgent
from config import JEV_ENDPOINT, USE_LAYA_MLX, TYPESAFE_API_KEY

laya_agent = None
if USE_LAYA_MLX:
    try:
        import laya_mlx as laya
        laya_agent = laya.load("aac6fef/laya-mlx", dtype="float16")
    except Exception:
        pass

class ScoringAgent(BaseAgent):
    name = "scoring"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        item = context.get("item", "")
        domain = context.get("domain", "grocery")
        source = context.get("source", "manual")
        api_key = context.get("api_key") or TYPESAFE_API_KEY
        use_local = context.get("use_local", False) or USE_LAYA_MLX

        state = {"item": item, "domain": domain, "source": source}
        questions = {
            "sell_potential": {"type": "score", "instructions": "Khả năng bán được.", "criteria": ["low", "medium", "high", "very_high"]},
            "easy_to_source": {"type": "score", "instructions": "Dễ nhập hàng.", "criteria": ["hard", "medium", "easy"]},
            "low_risk": {"type": "noul", "instructions": "Rủi ro thấp."}
        }

        if use_local and laya_agent is not None:
            result = laya_agent.predict(json.dumps(state), questions)
            answers = result.get("answers", result)
            model = "laya-mlx"
        else:
            if not api_key:
                raise HTTPException(400, "Thiếu API key hoặc bật USE_LAYA_MLX")
            payload = {"model": "jev-latest", "state": state, "questions": questions}
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            r = requests.post(JEV_ENDPOINT, json=payload, headers=headers, timeout=45)
            r.raise_for_status()
            answers = r.json().get("answers", {})
            model = "jev"

        sp = answers.get("sell_potential", {}).get("score")
        risk = answers.get("low_risk", {}).get("noul", 0)
        passed = sp in ("high", "very_high") and risk > 0.7

        return {"passed": passed, "answers": answers, "model": model, "item": item, "domain": domain, "source": source}
