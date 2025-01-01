import asyncio
import aiosqlite
import time
from loguru import logger

from apscheduler.schedulers.asyncio import AsyncIOScheduler

create_users_table_users = ("CREATE TABLE IF NOT EXISTS users (telegram_id TEXT, tovar TEXT, reasons TEXT, "
                            "reason_text TEXT, number_of_requests INT);")

create_users_table_users_for_notification = ("CREATE TABLE IF NOT EXISTS users_for_notification (telegram_id TEXT NOT "
                                             "NULL, name TEXT DEFAULT NULL, warehouses TEXT DEFAULT NULL, max_koeff	"
                                             "INTEGER DEFAULT 2, type_of_delivery TEXT DEFAULT NULL, dates TEXT);")


class Database:
    def __init__(self):
        self.db_path = "users.db"
        self.connection = None

    async def connect(self):
        try:
            if not self.connection:
                self.connection = await aiosqlite.connect(self.db_path)
                await self.connection.execute("PRAGMA journal_mode=WAL;")
                await self.connection.commit()
            """Подключение к базе данных."""
            return self.connection
        except Exception as e:
            logger.exception('Ошибка в database/Database().connect', e)

    async def close(self):
        """Закрывает подключение к базе данных."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def chek_tables(self):
        conn = await self.connect()
        try:
            await conn.execute(create_users_table_users)
            await conn.execute(create_users_table_users_for_notification)
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().chek_tables', e)

    async def search_in_table(self, search_telegram_id, table="users"):
        conn = await self.connect()
        try:
            async with conn.execute(f"SELECT * FROM {table} WHERE telegram_id = ?", (search_telegram_id,)) as cursor:
                result = await cursor.fetchall()
                return [True, result] if result else [False, None]
        except Exception as e:
            logger.exception('Ошибка в database/Database().search_in_table', e)

    async def add_user(self, update_telegram_id, update_tovar=None, update_reasons=None, update_reason_text=None):
        conn = await self.connect()
        try:
            await conn.execute(
                f"INSERT INTO users (telegram_id, tovar, reasons, reason_text, number_of_requests) "
                f"VALUES (?, ?, ?, ?, ?);",
                (update_telegram_id, update_tovar, update_reasons, update_reason_text, 1),
            )
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().add_user', e)

    async def add_user_in_users_for_notification(self, telegram_id, name=None, warehouses=None, max_koeff=None,
                                                 type_of_delivery=None, dates=None):
        conn = await self.connect()
        try:
            await conn.execute(f"INSERT INTO users_for_notification (telegram_id, name, warehouses, max_koeff, "
                               f"type_of_delivery, dates) VALUES (?, ?, ?, ?, ?, ?);", (telegram_id, name, warehouses,
                                                                                        max_koeff, type_of_delivery,
                                                                                        dates))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().add_user_in_users_for_notification', e)

    async def update_table_in_users_for_notification(self, telegram_id, update_data):
        set_clause = ", ".join([f"{key}=?" for key in update_data.keys()])
        conn = await self.connect()
        try:
            await conn.execute(f"UPDATE users_for_notification SET {set_clause} WHERE telegram_id=?",
                               (*update_data.values(), telegram_id))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().update_table_in_users_for_notification', e)

    async def update_table(self, telegram_id, update_tovar=None, update_reasons=None,
                           update_number_of_requests=None):
        try:
            conn = await self.connect()
            if update_tovar is not None:
                await conn.execute("UPDATE users SET tovar=? WHERE telegram_id=?",
                                   (update_tovar, telegram_id))
            if update_reasons is not None:
                await conn.execute("UPDATE users SET reasons=? WHERE telegram_id=?", (update_reasons, telegram_id))
            if update_number_of_requests is not None:
                await conn.execute("UPDATE users SET number_of_requests=? WHERE telegram_id=?",
                                   (update_number_of_requests, telegram_id))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().update_table', e)

    async def delete_user(self, telegram_id, table):
        conn = await self.connect()
        try:
            await conn.execute(f"DELETE FROM {table} WHERE telegram_id = ?;", (telegram_id,))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().delete_user', e)

    async def delete_users_for_notification(self, telegram_id, warehouses):
        conn = await self.connect()
        try:
            await conn.execute(f"DELETE FROM users_for_notification WHERE telegram_id = ? AND warehouses=?;",
                               (telegram_id, warehouses))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().delete_users_for_notification', e)

    async def delete_all_users(self, table='users'):
        conn = await self.connect()
        try:
            await conn.execute(f'DELETE FROM {table}')
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().delete_all_users', e)

    async def update_users_with_multiple_entries(self, telegram_id, column_name, values_list,
                                                 table='users_for_notification'):
        values_str = ', '.join(map(str, values_list))
        update_query = f"""
        UPDATE {table}
        SET {column_name} = ?
        WHERE telegram_id = ?;
        """
        conn = await self.connect()
        try:
            await conn.execute(update_query, (values_str, telegram_id))
            await conn.commit()
            return [True, "Записи успешно обновлены."]
        except Exception as e:
            logger.exception('Ошибка в database/Database().update_users_with_multiple_entries', e)

    async def return_base_data(self):
        conn = await self.connect()
        try:
            async with conn.execute("SELECT telegram_id, warehouses, max_koeff, type_of_delivery "
                                    "FROM users_for_notification") as cursor:
                rows = await cursor.fetchall()
                if len(rows) == 0:
                    return False
                return rows
        except Exception as e:
            logger.exception('Ошибка в database/Database().return_base_data', e)


# print(asyncio.run(database().search_in_table('11111', 'users_for_notification')))
