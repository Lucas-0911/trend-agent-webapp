"""App settings and paths."""
import os

JEV_ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MEDIACRAWLER_PATH = os.getenv("MEDIACRAWLER_PATH", os.path.expanduser("~/MediaCrawler"))
DB_PATH = os.getenv("TREND_DB_PATH", "trend_data.db")
USE_LAYA_MLX = os.getenv("USE_LAYA_MLX", "false").lower() == "true"
TYPESAFE_API_KEY = os.getenv("TYPESAFE_API_KEY", "")
