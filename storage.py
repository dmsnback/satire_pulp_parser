import sqlite3
from datetime import datetime, timezone

DB_NAME = "satire_pulp.db"


def get_connecttion():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connecttion() as conn:
        conn.execute("""
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE,
                    title TEXT,
                    create_at TEXT
                )
""")
        conn.commit()


def is_news_exists(url):
    with get_connecttion() as conn:
        cursor = conn.execute(
            """
                SELECT 1 FROM news WHERE url = ?
""",
            (url,),
        )
        return cursor.fetchone() is not None


def save_news(url, title):
    with get_connecttion() as conn:
        conn.execute(
            """
                INSERT INTO news (url, title, create_at) VALUES (?, ?, ?)
""",
            (url, title, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
