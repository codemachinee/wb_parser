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
        gc = gspread.service_account(filename='base_key.json')  # доступ к гугл табл по ключевому файлу аккаунта разраба
        # открытие таблицы по юрл адресу:
        sh = gc.open('База данных WB')
        self.worksheet = sh.worksheet('база')  # выбор листа 'общая база клиентов' таблицы

    async def chec_and_record(self):  # функция поиска и записи в базу
        worksheet_len = len(self.worksheet.col_values(1)) + 1  # поиск первой свободной ячейки для записи во 2 столбце
        m = await self.bot.send_message(admin_account, 'Пробиваю базу..⏳')
        if str(self.message.chat.id) in self.worksheet.col_values(1):
            await self.bot.edit_message_text('Клиент есть в базе', self.message.chat.id, m.message_id)
        else:
            await self.bot.edit_message_text(f'Клиент добавлен в базу\n'
                                             f'База: '
                                             f'https://docs.google.com/spreadsheets/d/1gPsql3jmemmNbUbN0SQ16NTlY'
                                             f'F8omWO4dsbRllJBElw/edit?usp=sharing',
                                             self.message.chat.id, m.message_id)
            self.worksheet.update(f'A{worksheet_len}:I{worksheet_len}', [[self.message.chat.id,
                                  self.message.from_user.username, self.message.from_user.first_name,
                                  self.message.from_user.last_name, None, self.tovar_name, None, None,
                                  str(datetime.now().date())]])

    async def rasylka_v_bazu(self):  # функция рассылки постов в базы
        telegram_ids_values_list = self.worksheet.col_values(1)
        telegram_names_values_list = self.worksheet.col_values(2)
        for i in range(1, len(telegram_ids_values_list)):
            try:
                self.bot.copy_message(telegram_ids_values_list[i], admin_account, self.message)
                #self.bot.send_message(self.worksheet.col_values(1)[i], 'Участвовать в акции?', reply_markup=kb6)
            except Exception:
                self.bot.send_message(admin_account, f'Босс, @{telegram_names_values_list[i]} заблочил меня.')
        self.bot.send_message(self.message.chat.id, 'Босс, рассылка в базу клиентов выполнена ✅')