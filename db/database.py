import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "shelf.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Создать таблицы. Пока пусто — допишем при добавлении хранения."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                name TEXT NOT NULL,
                expiry_date TEXT NOT NULL,
                notified_7 INTEGER DEFAULT 0,
                notified_3 INTEGER DEFAULT 0,
                notified_1 INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
