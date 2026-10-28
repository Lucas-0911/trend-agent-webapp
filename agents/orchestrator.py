"""Orchestrator — coordinates Crawl → Scoring → Analysis agents."""
from typing import Any, Dict
from agents.crawl_agent import CrawlAgent
from agents.scoring_agent import ScoringAgent
from agents.analysis_agent import AnalysisAgent

class Orchestrator:
    def __init__(self):
        self.crawl = CrawlAgent()
        self.scoring = ScoringAgent()
        self.analysis = AnalysisAgent()

    def scan(self) -> Dict[str, Any]:
        return self.crawl.run({})

    def score(self, item: str, domain: str, source: str, api_key: str = None, use_local: bool = False) -> Dict[str, Any]:
        ctx = {"item": item, "domain": domain, "source": source, "api_key": api_key, "use_local": use_local}
        return self.scoring.run(ctx)

    def analyze(self, item: str, scores: dict) -> Dict[str, Any]:
        return self.analysis.run({"item": item, "answers": scores})
