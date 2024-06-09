import sqlite3
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

create_users_table = ("CREATE TABLE IF NOT EXISTS users (telegram_id TEXT, tovar TEXT, reasons TEXT, "
                      "reason_text TEXT, number_of_requests INT);")


class database:
    def __init__(self):
        self.base = sqlite3.connect('users.db')
        self.cur = self.base.cursor()
        self.base.execute(create_users_table)
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    async def search_in_table(self, search_telegram_id):
        result = self.cur.execute(f"SELECT * FROM users WHERE telegram_id == ?", (search_telegram_id,)).fetchall()
        if result:
            return result
        else:
            return False

    async def add_user(self, update_telegram_id, update_tovar=None, update_reasons=None,
                       update_reason_text=None):
        self.cur.execute(f"INSERT INTO users (telegram_id, tovar, reasons, reason_text, number_of_requests) "
                         f"VALUES (?, ?, ?, ?, ?);",
                         (update_telegram_id, update_tovar, update_reasons, update_reason_text, 1))
        self.base.commit()

    async def update_table(self, telegram_id, update_tovar=None, update_reasons=None,
                           update_number_of_requests=None):
        if update_tovar is not None:
            self.cur.execute("UPDATE users SET tovar=? WHERE telegram_id=?",
                             (update_tovar, telegram_id))
        if update_reasons is not None:
            self.cur.execute("UPDATE users SET reasons=? WHERE telegram_id=?", (update_reasons, telegram_id))
        if update_number_of_requests is not None:
            self.cur.execute("UPDATE users SET number_of_requests=? WHERE telegram_id=?",
                             (update_number_of_requests, telegram_id))
        self.base.commit()

    # async def delete_user(self, telegram_id):
    #     self.cur.execute(f"DELETE FROM users WHERE telegram_id = ?;", (telegram_id,))
    #     self.base.commit()
    #     self.base.close()
    async def delete_all_users(self):
        self.cur.execute(f'DELETE FROM users')
        self.base.commit()
        self.base.close()

    def schedule_task(self):
        self.scheduler.add_job(self.delete_all_users, "cron", day_of_week='mon-sun', hour=00)

