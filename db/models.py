import sqlite3 as sq


class DataBase:
    def __init__(self, path):
        self.connect = sq.connect(path)
        self.cursor = self.connect.cursor()
        self.create_table()

    async def create_table(self) -> None:
        """Create DataBase"""
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "tg_id INTEGER,"
            "tg_name TEXT,"
            "username TEXT,"
            "mailing INTEGER DEFAULT 1,"
            "city TEXT);"
        )
        self.connect.commit()

    async def add_user_to_db(self, tg_id: int, tg_name: str, username: str) -> None:
        """Add a new user to DataBase"""
        with self.connect:
            self.cursor.execute("SELECT tg_id FROM users where tg_id = ?", (tg_id,))
            if self.cursor.fetchone() is None:
                self.cursor.execute("INSERT INTO users(tg_id, tg_name, username) VALUES (?, ?, ?)",
                                    (tg_id, tg_name, username,))

    async def get_users_info(self) -> list:
        """Get information about user from DataBase"""
        with self.connect:
            users = self.cursor.execute("SELECT tg_id, tg_name, username, mailing, city FROM users").fetchall()
        return users

    async def update_user(self, tg_id: int, tg_name: str, username: str) -> None:
        """Update tg_id, username and tg_name of user in DataBase"""
        with self.connect:
            if username is None:
                username = 'Скрыто'
            else:
                username = '@' + username
            self.cursor.execute("UPDATE users SET tg_name = ?, username = ? WHERE tg_id = ?",
                                (tg_name, username, tg_id,))

    async def add_settings(self, tg_id: int, mailing: int, city: str) -> None:
        """Update mailing settings(agreement to receive messages) of user in DataBase"""
        with self.connect:
            self.cursor.execute("UPDATE users SET mailing = ?, city = ? WHERE tg_id = ?",
                                (mailing, city, tg_id,))

    async def delete_user(self, tg_id: int) -> None:
        """Delete selected user by tg_id"""
        with self.connect:
            self.cursor.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))

    async def get_mailing_users(self):
        with self.connect:
            mailing_users = self.cursor.execute("SELECT tg_id, tg_name, city FROM users WHERE mailing IS NOT 0").fetchall()
        return mailing_users


db = DataBase('../tg.db')
backup_db = DataBase('../backup.db')
