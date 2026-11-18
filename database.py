
import sqlite3

def connect_db():
    return sqlite3.connect("fitbot.db")

def create_table():
    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_message(user_message, bot_response):
    conn = connect_db()

    conn.execute(
        "INSERT INTO chat_history (user_message, bot_response) VALUES (?, ?)",
        (user_message, bot_response)
    )

    conn.commit()
    conn.close()

def get_history():
    conn = connect_db()

    cursor = conn.execute(
        "SELECT user_message, bot_response FROM chat_history ORDER BY id"
    )

    history = cursor.fetchall()
    conn.close()

    return history
