"""FastAPI routes."""
import json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict, Any

from db import get_db
from scoring import score_item
from analysis import build_platform_suggestions
from crawler import scan_crawler_data

router = APIRouter()

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

@router.get("/api/scan")
def scan():
    data = scan_crawler_data()
    from scoring import laya_agent
    data["laya_available"] = laya_agent is not None
    return data

@router.post("/api/score")
def score(req: ScoreRequest):
    result = score_item(req.item, req.domain, req.source, req.api_key, req.use_local)
    item_id = None
    if result["passed"]:
        conn = get_db()
        cur = conn.execute(
            """INSERT INTO trend_items (name, description, source, raw_data, scores, domain, status)
               VALUES (?,?,?,?,?,?,?)""",
            (
                req.item[:200],
                req.item,
                req.source,
                json.dumps({"text": req.item}),
                json.dumps(result["answers"]),
                req.domain,
                "passed",
            ),
        )
        item_id = cur.lastrowid
        conn.commit()
        conn.close()
    result["item_id"] = item_id
    return result

@router.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    out = build_platform_suggestions(req.item, req.scores)
    conn = get_db()
    conn.execute(
        "INSERT INTO trend_analysis (item_id, analysis_text, suggestions) VALUES (?,?,?)",
        (req.item_id, out["analysis"], out["suggestions_json"]),
    )
    conn.commit()
    conn.close()
    name = req.item[:40]
    sell = req.scores.get("sell_potential", {}).get("score", "?")
    risk = req.scores.get("low_risk", {}).get("noul", 0)
    out["telegram"] = f"✅ {name}\nSell: {sell} | Risk: {risk:.2f}\nĐã có gợi ý video theo nền tảng."
    return out

@router.get("/api/saved")
def saved():
    conn = get_db()
    rows = conn.execute(
        """SELECT i.id, i.name, i.source, i.domain, i.created_at, a.analysis_text
           FROM trend_items i
           LEFT JOIN trend_analysis a ON a.item_id = i.id
           ORDER BY i.id DESC LIMIT 100"""
    ).fetchall()
    conn.close()
    return {"items": [dict(r) for r in rows]}
