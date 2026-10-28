"""Trend Agent — main entry."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from db import init_db
from routes import router

init_db()

app = FastAPI(title="Trend Agent")
app.include_router(router)

@app.get("/", response_class=HTMLResponse)
def index():
    return open("index.html", encoding="utf-8").read()
