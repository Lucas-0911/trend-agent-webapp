"""
Trend Agent WebApp
MediaCrawler → Jev API or local laya-mlx → DB → Analysis
Supports Apple Silicon (MacBook M1+) via laya-mlx.
"""

import os
import json
import glob
import sqlite3
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests

app = FastAPI(title="Trend Agent")

JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MEDIACRAWLER_PATH = os.getenv("MEDIACRAWLER_PATH", os.path.expanduser("~/MediaCrawler"))
DB_PATH = os.getenv("TREND_DB_PATH", "trend_data.db")
USE_LAYA_MLX = os.getenv("USE_LAYA_MLX", "false").lower() == "true"

laya_agent = None
if USE_LAYA_MLX:
    try:
        import laya_mlx as laya
        laya_agent = laya.load("aac6fef/laya-mlx", dtype="float16")
        print("Loaded laya-mlx local model")
    except Exception as e:
        print(f"laya-mlx not available: {e}")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS trend_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, description TEXT, source TEXT,
            raw_data TEXT, scores TEXT, status TEXT DEFAULT 'passed',
            domain TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS trend_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER, analysis_text TEXT, suggestions TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

init_db()

class ScoreRequest(BaseModel):
    item: str
    domain: str = "grocery"
    source: str = "manual"
    api_key: Optional[str] = None
    use_local: bool = False

class AnalyzeRequest(BaseModel):
    item_id: int
    item: str
    scores: Dict[str, Any]

def call_jev(api_key: str, state: dict, questions: dict) -> dict:
    payload = {"model": "jev-latest", "state": state, "questions": questions}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    r = requests.post(JEV_ENDPOINT, json=payload, headers=headers, timeout=45)
    r.raise_for_status()
    return r.json()

def call_laya(state: dict, questions: dict) -> dict:
    if laya_agent is None:
        raise HTTPException(400, "laya-mlx chưa được load. Cài laya-mlx và set USE_LAYA_MLX=true")
    result = laya_agent.predict(json.dumps(state) if isinstance(state, dict) else state, questions)
    return {"answers": result.get("answers", result)}

def normalize_item(raw: dict, platform: str) -> dict:
    name = raw.get("title") or raw.get("desc") or raw.get("content", "")[:80] or raw.get("note_title") or "unknown"
    desc = raw.get("desc") or raw.get("content") or raw.get("title") or ""
    return {"name": str(name)[:200], "description": str(desc)[:1000], "source": platform, "raw_data": raw}

@app.get("/api/scan")
def scan():
    results = []
    data_root = os.path.join(MEDIACRAWLER_PATH, "data")
    if not os.path.isdir(data_root):
        return {"items": [], "count": 0, "message": f"Không thấy {data_root}"}
    for platform in os.listdir(data_root):
        pdir = os.path.join(data_root, platform)
        if not os.path.isdir(pdir):
            continue
        for fpath in glob.glob(os.path.join(pdir, "**/*.json*"), recursive=True):
            try:
                with open(fpath, encoding="utf-8") as f:
                    if fpath.endswith(".jsonl"):
                        for line in f:
                            if line.strip():
                                results.append(normalize_item(json.loads(line), platform))
                    else:
                        data = json.load(f)
                        items = data if isinstance(data, list) else [data]
                        for raw in items:
                            if isinstance(raw, dict):
                                results.append(normalize_item(raw, platform))
            except Exception:
                continue
    seen, unique = set(), []
    for it in results:
        k = it["name"].lower().strip()
        if k and k not in seen:
            seen.add(k)
            unique.append(it)
    return {"items": unique[:200], "count": len(unique), "laya_available": laya_agent is not None}

@app.post("/api/score")
def score(req: ScoreRequest):
    state = {"item": req.item, "domain": req.domain, "source": req.source}
    questions = {
        "sell_potential": {"type": "score", "instructions": "Khả năng bán được.", "criteria": ["low", "medium", "high", "very_high"]},
        "easy_to_source": {"type": "score", "instructions": "Dễ nhập hàng.", "criteria": ["hard", "medium", "easy"]},
        "low_risk": {"type": "noul", "instructions": "Rủi ro thấp."}
    }
    use_local = req.use_local or USE_LAYA_MLX
    if use_local and laya_agent is not None:
        result = call_laya(state, questions)
    else:
        api_key = req.api_key or os.getenv("TYPESAFE_API_KEY")
        if not api_key:
            raise HTTPException(400, "Thiếu API key (hoặc bật USE_LAYA_MLX)")
        result = call_jev(api_key, state, questions)

    answers = result.get("answers", {})
    sp = answers.get("sell_potential", {}).get("score")
    risk = answers.get("low_risk", {}).get("noul", 0)
    passed = sp in ("high", "very_high") and risk > 0.7
    item_id = None
    if passed:
        conn = get_db()
        cur = conn.execute(
            "INSERT INTO trend_items (name, description, source, raw_data, scores, domain, status) VALUES (?,?,?,?,?,?,?)",
            (req.item[:200], req.item, req.source, json.dumps({"text": req.item}), json.dumps(answers), req.domain, "passed")
        )
        item_id = cur.lastrowid
        conn.commit()
        conn.close()
    return {"passed": passed, "item_id": item_id, "answers": answers, "model": "laya-mlx" if use_local else "jev"}

@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    sell = req.scores.get("sell_potential", {}).get("score", "?")
    risk = req.scores.get("low_risk", {}).get("noul", 0)
    text = f"""Sản phẩm: {req.item[:100]}
Điểm: sell={sell}, risk={risk:.2f}
Ý tưởng: Unboxing + nêu giá + cảm nhận ngắn.
Việc cần làm: Nhập thử số lượng nhỏ, quay video, đăng kênh chính."""
    conn = get_db()
    conn.execute(
        "INSERT INTO trend_analysis (item_id, analysis_text, suggestions) VALUES (?,?,?)",
        (req.item_id, text, json.dumps({"actions": ["nhập thử", "quay video"]}))
    )
    conn.commit()
    conn.close()
    return {"analysis": text, "telegram": f"✅ {req.item[:40]}\nSell: {sell} | Risk: {risk:.2f}"}

@app.get("/api/saved")
def saved():
    conn = get_db()
    rows = conn.execute("""
        SELECT i.id, i.name, i.source, i.domain, i.created_at, a.analysis_text
        FROM trend_items i LEFT JOIN trend_analysis a ON a.item_id = i.id
        ORDER BY i.id DESC LIMIT 100
    """).fetchall()
    conn.close()
    return {"items": [dict(r) for r in rows]}

@app.get("/", response_class=HTMLResponse)
def index():
    return open("index.html", encoding="utf-8").read()
