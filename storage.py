import sqlite3
from datetime import datetime, timezone

DB_NAME = "satire_pulp.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
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
        conn.execute("""
                CREATE TABLE IF NOT EXISTS last_sent_news (
                     chat_id INTEGER PRIMARY KEY,
                     last_news_id INTEGER
                )
""")
        conn.commit()


def is_news_exists(url):
    with get_connection() as conn:
        cursor = conn.execute(
            """
                SELECT 1 FROM news WHERE url = ?
""",
            (url,),
        )
        return cursor.fetchone() is not None


def save_news(url, title, image, text):
    with get_connection() as conn:
        conn.execute(
            """
                INSERT INTO news (url, title, image, text, create_at) VALUES (?, ?, ?, ?, ?)
""",
            (url, title, image, text, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()


def get_news_after_id(last_id, n=10):
    with get_connection() as conn:
        cursor = conn.execute(
            """
                SELECT id, title, image, text, url FROM news WHERE id > ? ORDER BY id DESC LIMIT ?
""",
            (last_id, n),
        )
        return cursor.fetchall()[::-1]


def get_last_sent_id(chat_id):
    with get_connection() as conn:
        cursor = conn.execute(
            """
                SELECT last_news_id FROM last_sent_news WHERE chat_id = ?
""",
            (chat_id,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return 0


def save_last_sent_news_id(chat_id, last_id):
    with get_connection() as conn:
        conn.execute(
            """
                INSERT INTO last_sent_news (chat_id, last_news_id) VALUES (?, ?)
                ON CONFLICT(chat_id) DO UPDATE SET last_news_id = excluded.last_news_id""",
            (chat_id, last_id),
        )
        conn.commit()


def get_all_users():
    with get_connection() as conn:
        cursor = conn.execute("""
                SELECT chat_id FROM last_sent_news
""")
        return [row[0] for row in cursor.fetchall()]
