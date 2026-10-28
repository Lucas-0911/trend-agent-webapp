"""Crawl Agent — scan and normalize MediaCrawler data."""
import os
import json
import glob
from typing import Any, Dict
from agents.base import BaseAgent
from config import MEDIACRAWLER_PATH

class CrawlAgent(BaseAgent):
    name = "crawl"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
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
                                    results.append(self._normalize(json.loads(line), platform))
                        else:
                            data = json.load(f)
                            items = data if isinstance(data, list) else [data]
                            for raw in items:
                                if isinstance(raw, dict):
                                    results.append(self._normalize(raw, platform))
                except Exception:
                    continue

        seen, unique = set(), []
        for it in results:
            k = it["name"].lower().strip()
            if k and k not in seen:
                seen.add(k)
                unique.append(it)

        return {"items": unique[:200], "count": len(unique)}

    def _normalize(self, raw: dict, platform: str) -> dict:
        name = raw.get("title") or raw.get("desc") or raw.get("content", "")[:80] or raw.get("note_title") or "unknown"
        desc = raw.get("desc") or raw.get("content") or raw.get("title") or ""
        return {"name": str(name)[:200], "description": str(desc)[:1000], "source": platform, "raw_data": raw}
