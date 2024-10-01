import openpyxl
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from wb_api import parse_date

kb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔔 Уведомление о слотах на складах', callback_data='slots')],
    [InlineKeyboardButton(text='🍇 Список складов wb', callback_data='wb_warehouses')],
    [InlineKeyboardButton(text='🏠 Список моих складов', callback_data='my_warehouses')],
    [InlineKeyboardButton(text='📋 Список товаров', callback_data='goods_list')],
    [InlineKeyboardButton(text='🔙 Тарифы на возвраты', callback_data='tariffs_returns')],
    [InlineKeyboardButton(text='📦 Тарифы на коробы', callback_data='tariffs_box')],
    [InlineKeyboardButton(text='🏗️Тарифы на монопаллеты', callback_data='tariffs_pallet')],
    [InlineKeyboardButton(text='🙊 Необработанные отзывы по товарам', callback_data='feedbacks')],
    [InlineKeyboardButton(text='❓Необработанные вопросы по товарам', callback_data='questions')],
    [InlineKeyboardButton(text='📈 Отчет о поставках', callback_data='suplier_list')]])


kb_choice_tovar = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сухой корм PREMIATO 🐕', callback_data='PREMIATO')]])

kb_back_to_reasons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Вернуться к выбору причины', callback_data='PREMIATO')]])


kb_choice_reasons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚚 Закупка оптом', callback_data='opt')],
    [InlineKeyboardButton(text='📦 Проблемы с упаковкой', callback_data='package')],
    [InlineKeyboardButton(text='🍇 Пришел не тот вкус', callback_data='wrong_taste')],
    [InlineKeyboardButton(text='🐕 Перевод на корм PREMIATO', callback_data='transfer')],
    [InlineKeyboardButton(text='📋 Состав корма', callback_data='structure')],
    [InlineKeyboardButton(text='❗ Прием при проблемах со здоровьем', callback_data='health')],
    [InlineKeyboardButton(text='❓ Другое', callback_data='other')],
    [InlineKeyboardButton(text='🔙 Вернуться к выбору товара', callback_data='choice_good')]
])


kb_slots_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📦 Выбор склада', callback_data='choice_warehouse')],
    [InlineKeyboardButton(text='⚙️ Настройка склада', callback_data='warehouse_settings')],
    [InlineKeyboardButton(text='🔙 Вернуться назад', callback_data='func_menu')]
])


class buttons:  # класс для создания клавиатур различных категорий товаров

    def __init__(self, bot, message, kategoriya=None, keyboard_dict=None, back_value=None, subscritions_list=None,
                 all_button=None):
        self.bot = bot
        self.message = message
        self.subscritions_list = subscritions_list
        self.kategoriya = kategoriya
        self.keyboard_dict = keyboard_dict
        self.back_value = back_value
        self.all_button = all_button

    async def warehouses_buttons(self):
        await parse_date().get_coeffs_warehouses()
        wb = openpyxl.load_workbook("tables/Коэффициенты складов.xlsx")
        sheet = wb.active  # Берем активный лист (или можно указать по имени, если нужно)
        # Проходим по строкам начиная с первой строки (или с другой, если есть заголовки)
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=3, max_col=4):
            # Проверяем значение в 3-м столбце
            if str(row[2].value) == value_col3:
                # Если соответствует, проверяем значение в 6-м столбце
                if str(row[5].value) == value_col6:
                    print(True)
                    return True  # Если оба условия выполняются, возвращаем True
        answer_base = await database_func(self.bot, self.message).chek_user_in_users_by_chat_id()
        if answer_base is False:
            but1 = types.KeyboardButton(text='✅ Войти в аккаунт')
            but2 = types.KeyboardButton(text='🆕 Регистрация')
            kb1 = types.ReplyKeyboardMarkup(keyboard=[[but1, but2]], resize_keyboard=True, row_width=3)
            if self.message.from_user.first_name:
                await self.bot.send_message(self.message.chat.id,
                                            text=f'Здравствуйте, {self.message.from_user.first_name}\n'
                                                 f'Вы не авторизованы',
                                            reply_markup=kb1)
            else:
                await self.bot.send_message(self.message.chat.id,
                                            text=f'Здравствуйте!\n'
                                                 f'Вы не авторизованы',
                                            reply_markup=kb1)

    async def zayavki_buttons(self):
        keys = {}
        keyboard_list = []
        keys_list = list(self.keyboard_dict[0].keys())
        if self.back_value != 'razdely_buttons':
            if self.all_button is not None:
                add_list = []
                del_list = []
                for i in keys_list:
                    if f'{self.keyboard_dict[1]}_{i}' in self.subscritions_list:
                        del_list.append(i)
                    else:
                        add_list.append(i)
                if len(del_list) == 0:
                    add_button = types.InlineKeyboardButton(text="📁 Выбрать все", callback_data=f'{self.keyboard_dict[1]}_add_{self.all_button}')
                    keyboard_list.append([add_button])
                elif len(add_list) == 0:
                    del_button = types.InlineKeyboardButton(text="🗑 Удалить все", callback_data=f'{self.keyboard_dict[1]}_del_{self.all_button}')
                    keyboard_list.append([del_button])
                else:
                    add_button = types.InlineKeyboardButton(text="📁 Выбрать все", callback_data=f'{self.keyboard_dict[1]}_add_{self.all_button}')
                    del_button = types.InlineKeyboardButton(text="🗑 Удалить все", callback_data=f'{self.keyboard_dict[1]}_del_{self.all_button}')
                    keyboard_list.append([add_button, del_button])
            else:
                pass

        if keys_list[0] == 'date':
            keys_list = keys_list[1:]

        for i in keys_list:
            index = keys_list.index(i)
            if self.subscritions_list is not None and f'{self.keyboard_dict[1]}_{i}' in self.subscritions_list:
                button = types.InlineKeyboardButton(text=f"🔘{self.keyboard_dict[0][i]['name']}",
                                                    callback_data=f"{self.keyboard_dict[1]}_{self.keyboard_dict[0][i]['id']}")
                keys[f'but{index}'] = button
            else:
                button = types.InlineKeyboardButton(text=self.keyboard_dict[0][i]['name'],
                                                    callback_data=f"{self.keyboard_dict[1]}_{self.keyboard_dict[0][i]['id']}")
                keys[f'but{index}'] = button

            # Группируем кнопки попарно
            if index > 0 and index % 2 != 0:
                previous_button = keys[f'but{index - 1}']
                if len(self.keyboard_dict[0][i]['name']) <= 16 and len(
                        self.keyboard_dict[0][keys_list[index - 1]]['name']) <= 16:
                    keyboard_list.append([previous_button, button])
                else:
                    keyboard_list.append([previous_button])
                    keyboard_list.append([button])
            elif index == (len(keys_list) - 1):
                keyboard_list.append([button])
        if self.back_value is not None:
            back_button = types.InlineKeyboardButton(text="↩️ Вернуться назад", callback_data=self.back_value)
            keyboard_list.append([back_button])
        kb2 = types.InlineKeyboardMarkup(inline_keyboard=keyboard_list, resize_keyboard=True)

        await self.bot.edit_message_text(text=f'Выберите категории рассылки которых хотите получать (выбранные категории '
                                         'отмечены: 🔘)', chat_id=self.message.chat.id, message_id=self.message.message_id)
        await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id, message_id=self.message.message_id,
                                                 reply_markup=kb2)