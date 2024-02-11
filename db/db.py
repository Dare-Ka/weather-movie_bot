import sqlite3 as sq

db = sq.connect('../tg.db')
cur = db.cursor()


async def add_user_to_db(tg_id: int, tg_name: str, username: str) -> None:
    """Create DataBase and add a new user"""
    cur.execute("CREATE TABLE IF NOT EXISTS users ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                " tg_id INTEGER,"
                " tg_name TEXT,"
                " username TEXT)")
    cur.execute("SELECT tg_id FROM users where tg_id = ?", (tg_id,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(tg_id, tg_name, username) VALUES (?, ?, ?)", (tg_id, tg_name, username,))
        db.commit()


async def get_users_info() -> list:
    """Get tg_id, username and tg_name from DataBase"""
    cur.execute("SELECT tg_id, tg_name, username FROM users")
    return cur.fetchall()


async def update_user(tg_id: int, tg_name: str, username: str) -> None:
    """Update tg_id, username and tg_name of user in DataBase"""
    cur.execute("UPDATE users SET tg_name = ?, username = ? WHERE tg_id = ?", (tg_name, username, tg_id,))
    db.commit()


async def delete_user(tg_id: int) -> None:
    """Delete selected user by tg_id"""
    cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
    db.commit()
