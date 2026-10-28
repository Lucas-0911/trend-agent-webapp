"""Scoring with Jev API or local laya-mlx."""
import json
import requests
from fastapi import HTTPException
from config import JEV_ENDPOINT, USE_LAYA_MLX, TYPESAFE_API_KEY

laya_agent = None
if USE_LAYA_MLX:
    try:
        import laya_mlx as laya
        laya_agent = laya.load("aac6fef/laya-mlx", dtype="float16")
        print("Loaded laya-mlx")
    except Exception as e:
        print(f"laya-mlx not available: {e}")

def call_jev(api_key: str, state: dict, questions: dict) -> dict:
    payload = {"model": "jev-latest", "state": state, "questions": questions}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(JEV_ENDPOINT, json=payload, headers=headers, timeout=45)
    r.raise_for_status()
    return r.json()

def call_laya(state: dict, questions: dict) -> dict:
    if laya_agent is None:
        raise HTTPException(400, "laya-mlx chưa load. Set USE_LAYA_MLX=true")
    result = laya_agent.predict(json.dumps(state), questions)
    return {"answers": result.get("answers", result)}

def score_item(item: str, domain: str, source: str, api_key: str = None, use_local: bool = False) -> dict:
    state = {"item": item, "domain": domain, "source": source}
    questions = {
        "sell_potential": {
            "type": "score",
            "instructions": "Khả năng bán được.",
            "criteria": ["low", "medium", "high", "very_high"]
        },
        "easy_to_source": {
            "type": "score",
            "instructions": "Dễ nhập hàng.",
            "criteria": ["hard", "medium", "easy"]
        },
        "low_risk": {"type": "noul", "instructions": "Rủi ro thấp."}
    }
    use_laya = use_local or USE_LAYA_MLX
    if use_laya and laya_agent is not None:
        result = call_laya(state, questions)
        model = "laya-mlx"
    else:
        key = api_key or TYPESAFE_API_KEY
        if not key:
            raise HTTPException(400, "Thiếu API key hoặc bật USE_LAYA_MLX")
        result = call_jev(key, state, questions)
        model = "jev"

    answers = result.get("answers", {})
    sp = answers.get("sell_potential", {}).get("score")
    risk = answers.get("low_risk", {}).get("noul", 0)
    passed = sp in ("high", "very_high") and risk > 0.7
    return {"passed": passed, "answers": answers, "model": model}
