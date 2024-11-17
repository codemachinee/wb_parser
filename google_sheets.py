# библиотека работы с гугл таблицами
import gspread
from loguru import logger

from passwords import *
admin_account = admin_id
# библиотека проверки даты
from datetime import *
import pytz
moscow_tz = pytz.timezone('Europe/Moscow')


class clients_base:  # класс базы данных

    def __init__(self, bot, message, tovar_name=None):
        self.bot = bot
        self.message = message
        self.tovar_name = tovar_name
        gc = gspread.service_account(filename='pidor-of-the-day-5880592e7067.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
        # открытие таблицы по юрл адресу:
        sh = gc.open('clients_base_WB')
        self.worksheet_base = sh.worksheet('base')
        self.worksheet_client_base = sh.worksheet('client_base')# выбор листа 'общая база клиентов' таблицы

    async def record_in_base(self, reasons=None, reason_text=None):  # функция поиска и записи в базу
        try:
            worksheet_len = len(self.worksheet_base.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
            self.worksheet_base.update(f'A{worksheet_len}:I{worksheet_len}', [[self.message.chat.id,
                                       self.message.from_user.username, self.message.from_user.first_name,
                                       self.message.from_user.last_name, None, self.tovar_name, reasons, reason_text,
                                       str(datetime.now(moscow_tz).strftime('%d.%m.%y %H:%M'))]])
            await self.chec_and_record_in_client_base(reasons, reason_text)
        except Exception as e:
            logger.exception('Исключение вызванное функцией проверки и записи клиента в гугл-таблицу', e)
            await self.bot.send_message(loggs_acc, f'Исключение вызванное функцией проверки и записи клиента в '
                                                       f'гугл-таблицу: {e}')

    async def chec_and_record_in_client_base(self, reasons=None, reason_text=None):  # функция поиска и записи в базу
        try:
            worksheet_len = len(self.worksheet_client_base.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
            if str(self.message.chat.id) in self.worksheet_client_base.col_values(1):
                pass
            else:
                self.worksheet_client_base.update(f'A{worksheet_len}:I{worksheet_len}', [[self.message.chat.id,
                                                  self.message.from_user.username, self.message.from_user.first_name,
                                                  self.message.from_user.last_name, None, self.tovar_name, reasons,
                                                                                          reason_text,
                                                  str(datetime.now(moscow_tz).strftime('%d.%m.%y %H:%M'))]])
        except Exception as e:
            logger.exception('Исключение вызванное функцией проверки и записи клиента в гугл-таблицу', e)
            await self.bot.send_message(loggs_acc, f'Исключение вызванное функцией проверки и записи клиента в '
                                                   f'гугл-таблицу: {e}')

    async def rasylka_v_bazu(self):  # функция рассылки постов в базы
        telegram_ids_values_list = self.worksheet_client_base.col_values(1)
        telegram_names_values_list = self.worksheet_client_base.col_values(2)
        for i in range(1, len(telegram_ids_values_list)):
            try:
                await self.bot.copy_message(telegram_ids_values_list[i], admin_account, self.message.message_id)
                    #self.bot.send_message(self.worksheet.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
            except Exception as e:
                logger.exception('Рассылка в базу данных', f'Босс, с @{telegram_names_values_list[i]} проблема{e}')
                await self.bot.send_message(loggs_acc, f'Босс, с @{telegram_names_values_list[i]} проблема{e}')
        await self.bot.send_message(self.message.chat.id, 'Босс, рассылка в базу клиентов выполнена ✅')
