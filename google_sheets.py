# библиотека работы с гугл таблицами
import gspread
from passwords import *
admin_account = admin_id
# библиотека проверки даты
from datetime import *


class clients_base:  # класс базы данных

    def __init__(self, bot, message, tovar_name=None):
        self.bot = bot
        self.message = message
        self.tovar_name = tovar_name
        gc = gspread.service_account(filename='pidor-of-the-day-5880592e7067.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
        # открытие таблицы по юрл адресу:
        sh = gc.open('clients_base_WB')
        self.worksheet = sh.worksheet('base')  # выбор листа 'общая база клиентов' таблицы

    async def chec_and_record(self, reasons=None, reason_text=None):  # функция поиска и записи в базу
        try:
            worksheet_len = len(self.worksheet.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
            mes = await self.bot.send_message(admin_account, 'Пробиваю базу..⏳')
            if str(self.message.chat.id) in self.worksheet.col_values(1):
                await self.bot.edit_message_text('Клиент есть в базе', admin_account, mes.message_id)
                self.worksheet.update(f'H{self.worksheet.find(str(self.message.chat.id)).row}:'
                                      f'I{self.worksheet.find(str(self.message.chat.id)).row}', [[reason_text,
                                                              str(datetime.now().date())]])
            else:
                self.worksheet.update(f'A{worksheet_len}:I{worksheet_len}', [[self.message.chat.id,
                                      self.message.from_user.username, self.message.from_user.first_name,
                                      self.message.from_user.last_name, None, self.tovar_name, reasons, reason_text,
                                      str(datetime.now().date())]])
                await self.bot.edit_message_text(f'Клиент добавлен в базу\n'
                                                 f'База: '
                                                 f'https://docs.google.com/spreadsheets/d/1gPsql3jmemmNbUbN0SQ16NTlY'
                                                 f'F8omWO4dsbRllJBElw/edit?usp=sharing',
                                                 admin_account, mes.message_id)
        except Exception as e:
            await self.bot.send_message(admin_account, f'Исключение вызванное функцией проверки и записи клиента в '
                                                       f'гугл-таблицу: {e}')

    async def rasylka_v_bazu(self):  # функция рассылки постов в базы
        telegram_ids_values_list = self.worksheet.col_values(1)
        telegram_names_values_list = self.worksheet.col_values(2)
        for i in range(1, len(telegram_ids_values_list)):
            try:
                self.bot.copy_message(telegram_ids_values_list[i], admin_account, self.message)
                #self.bot.send_message(self.worksheet.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
            except Exception:
                await self.bot.send_message(admin_account, f'Босс, @{telegram_names_values_list[i]} заблочил меня.')
        await self.bot.send_message(self.message.chat.id, 'Босс, рассылка в базу клиентов выполнена ✅')