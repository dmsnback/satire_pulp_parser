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
                    image TEXT,
                    text TEXT,
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


def save_news(url, title, image, text):
    with get_connecttion() as conn:
        conn.execute(
            """
                INSERT INTO news (url, title, image, text, create_at) VALUES (?, ?, ?, ?, ?)
""",
            (url, title, image, text, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()


def get_last_news(limit=5):
    with get_connecttion() as conn:
        curcor = conn.execute(
            """
                SELECT title, image, text, url FROM news ORDER BY id DESC LIMIT ?
""",
            (limit,),
        )
    return curcor.fetchall()


def get_news_id(last_id):
    with get_connecttion() as conn:
        cursor = conn.execute(
            """
                SELECT id, title, text, image, url FORM news WHERE id > ?
""",
            (last_id,),
        )
        return cursor.fetchall()
