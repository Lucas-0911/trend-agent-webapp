"""Database setup and helpers."""
import sqlite3
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS trend_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            source TEXT,
            raw_data TEXT,
            scores TEXT,
            status TEXT DEFAULT 'passed',
            domain TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS trend_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            analysis_text TEXT,
            suggestions TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
