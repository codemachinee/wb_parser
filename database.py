import sqlite3
import time

create_users_table = ("CREATE TABLE IF NOT EXISTS users (telegram_id TEXT, tovar TEXT, reasons TEXT, "
                      "reason_text TEXT);")


class database:
    def __init__(self):
        self.base = sqlite3.connect('users.db')
        self.cur = self.base.cursor()
        self.base.execute(create_users_table)

    async def search_in_table(self, search_telegram_id):
        result = self.cur.execute(f"SELECT * FROM users WHERE telegram_id == ?", (search_telegram_id,)).fetchall()
        if result:
            return result
        else:
            return False

    async def add_user(self, update_telegram_id, update_tovar=None, update_reasons=None,
                 update_reason_text=None):
        self.cur.execute(f"INSERT INTO users (telegram_id, tovar, reasons, reason_text) VALUES (?, ?, ?, ?);",
                         (update_telegram_id, update_tovar, update_reasons, update_reason_text))
        self.base.commit()

    async def update_table(self, telegram_id, update_tovar=None, update_reasons=None, update_reason_text=None):
        if update_tovar is not None:
            self.cur.execute("UPDATE users SET tovar=? WHERE telegram_id=?", (update_tovar, telegram_id))
        if update_reasons is not None:
            self.cur.execute("UPDATE users SET reasons=? WHERE telegram_id=?", (update_reasons, telegram_id))
        if update_reason_text is not None:
            self.cur.execute("UPDATE users SET reason_text=? WHERE telegram_id=?", (update_reason_text, telegram_id))
        self.base.commit()

    async def delete_user(self, telegram_id):
        self.cur.execute(f"DELETE FROM users WHERE telegram_id = ?;", (telegram_id,))
        self.base.commit()
        self.base.close()
