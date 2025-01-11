import openpyxl
from aiogram import types
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

kb_back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Вернуться назад', callback_data='slots')]])

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
    [InlineKeyboardButton(text='📦 Выбор склада', callback_data='warehouse_choice')],
    [InlineKeyboardButton(text='⚙️ Настройка склада', callback_data='settings_change')],
    [InlineKeyboardButton(text='🔙 Вернуться назад', callback_data='func_menu')]
])


class buttons:  # класс для создания клавиатур различных категорий товаров

    def __init__(self, bot, message, kategoriya=None, keyboard_dict=None, back_value=None, subscritions_list=[],
                 back_button=None, next_button=None):
        self.bot = bot
        self.message = message
        self.subscritions_list = subscritions_list
        self.kategoriya = kategoriya
        self.keyboard_dict = keyboard_dict
        self.back_value = back_value
        self.back_button = back_button
        self.next_button = next_button

    async def warehouses_buttons(self):
        keys = {}
        keyboard_list = []
        keys_list = self.keyboard_dict
        for i in keys_list:
            index = keys_list.index(i)
            if self.subscritions_list is not None and f'{i[0]}' in self.subscritions_list:
                button = types.InlineKeyboardButton(text=f"🔘{i[1]}",
                                                    callback_data=f"warehouse_{i[2]}_{0 if self.back_button is None else int(self.back_button[2:])+1}")
                keys[f'but{index}'] = button
            else:
                button = types.InlineKeyboardButton(text=i[1],
                                                    callback_data=f"warehouse_{i[2]}_{0 if self.back_button is None else int(self.back_button[2:])+1}")
                keys[f'but{index}'] = button

            # Группируем кнопки попарно
            if index > 0 and index % 2 != 0:
                previous_button = keys[f'but{index - 1}']
                if len(i[1]) <= 16 and len(keys_list[index - 1][1]) <= 16:
                    keyboard_list.append([previous_button, button])
                else:
                    keyboard_list.append([previous_button])
                    keyboard_list.append([button])
            elif index == (len(keys_list) - 1):
                keyboard_list.append([button])
        if self.next_button is not None and self.back_button is not None:
            back_button = types.InlineKeyboardButton(text="⬅️️", callback_data=f"warehouse_{self.back_button}")
            next_button = types.InlineKeyboardButton(text="➡️", callback_data=f"warehouse_{self.next_button}")
            keyboard_list.append([back_button, next_button])
        elif self.next_button is not None:
            next_button = types.InlineKeyboardButton(text="➡️", callback_data=f"warehouse_{self.next_button}")
            keyboard_list.append([next_button])
        elif self.back_button is not None:
            back_button = types.InlineKeyboardButton(text="⬅️️", callback_data=f"warehouse_{self.back_button}")
            keyboard_list.append([back_button])
        if len(self.subscritions_list) > 1:
            dell_all_button = types.InlineKeyboardButton(text="❌ Удалить выбранные склады",
                                                         callback_data=f"warehouse_del_{0 if self.back_button is None else int(self.back_button[2:])+1}")
            keyboard_list.append([dell_all_button])
        if self.back_value is not None:
            back_value_button = types.InlineKeyboardButton(text="↩️ Вернуться в меню", callback_data=self.back_value)
            keyboard_list.append([back_value_button])
        kb2 = types.InlineKeyboardMarkup(inline_keyboard=keyboard_list, resize_keyboard=True)
        await self.bot.edit_message_text(
            text=f'Выберите интересующие склады (выбранные склады '
                 'отмечены: 🔘)', chat_id=self.message.chat.id, message_id=self.message.message_id)
        await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id, message_id=self.message.message_id,
                                                 reply_markup=kb2)

    async def setings_buttons(self):
        keys = {}
        keyboard_list = []
        if len(self.subscritions_list) == len(self.keyboard_dict) == 0:
            await self.bot.edit_message_text(
                text=f'Вы не выбрали ни одного склада', chat_id=self.message.chat.id, message_id=self.message.message_id)
            await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id, message_id=self.message.message_id,
                                                     reply_markup=kb_back_to_menu)
        else:
            if self.subscritions_list[0] is None:
                keys_list = [['📦 Типы приемки:', 'заглушка'],
                             ["Короба", "2"], ["Монопаллеты", "5"],
                             ["Суперсейф", "6"], ["QR-поставка", "отсутствует"],
                             [f"💸 Коэффициент приемки: до 2", 'заглушка'],
                             [f"➖", "minus"], [f"➕", "plus"]]
            elif int(self.subscritions_list[0]) == 1:
                keys_list = [['📦 Типы приемки:', 'заглушка'],
                             ["Короба", "2"], ["Монопаллеты", "5"],
                             ["Суперсейф", "6"], ["QR-поставка", "отсутствует"],
                             [f"💸 Коэффициент приемки: до {self.subscritions_list[0]}", 'заглушка'],
                             [f"➕", "plus"]]
            elif int(self.subscritions_list[0]) == 8:
                keys_list = [['📦 Типы приемки:', 'заглушка'],
                             ["Короба", "2"], ["Монопаллеты", "5"],
                             ["Суперсейф", "6"], ["QR-поставка", "отсутствует"],
                             [f"💸 Коэффициент приемки: до {self.subscritions_list[0]}", 'заглушка'],
                             [f"➖", "minus"]]
            else:
                keys_list = [['📦 Типы приемки:', 'заглушка'],
                             ["Короба", "2"], ["Монопаллеты", "5"],
                             ["Суперсейф", "6"], ["QR-поставка", "отсутствует"],
                             [f"💸 Коэффициент приемки: до {self.subscritions_list[0]}", 'заглушка'],
                             [f"➖", "minus"], [f"➕", "plus"]]
            for i in keys_list:
                index = keys_list.index(i)
                if len(self.subscritions_list) != 0 and (f'{i[0]}' in self.subscritions_list[1] or f'{i[0]} с коробами'
                                                         in self.subscritions_list[1]):
                    button = types.InlineKeyboardButton(text=f"🔘{i[0]}", callback_data=f"settings_{i[1]}")
                    keys[f'but{index}'] = button
                else:
                    button = types.InlineKeyboardButton(text=i[0], callback_data=f"settings_{i[1]}")
                    keys[f'but{index}'] = button

                if len(keys_list) == 8:
                    if index == 0 or index == 5:
                        keyboard_list.append([button])
                    elif index == 2 or index == 4 or index == 7:
                        previous_button = keys[f'but{index - 1}']
                        keyboard_list.append([previous_button, button])
                    else:
                        pass
                else:
                    if index == 0 or index >= 5:
                        keyboard_list.append([button])
                    elif index == 2 or index == 4:
                        previous_button = keys[f'but{index - 1}']
                        keyboard_list.append([previous_button, button])
                    else:
                        pass
            back_value_button = types.InlineKeyboardButton(text="↩️ Вернуться в меню", callback_data=self.back_value)
            keyboard_list.append([back_value_button])
            kb2 = types.InlineKeyboardMarkup(inline_keyboard=keyboard_list, resize_keyboard=True)
            await self.bot.edit_message_text(text=f'Выбраны следующие склады: {", ".join(self.keyboard_dict)}\n\n'
                                             f'Настройте необходимые параметры:', chat_id=self.message.chat.id,
                                             message_id=self.message.message_id)
            await self.bot.edit_message_reply_markup(chat_id=self.message.chat.id, message_id=self.message.message_id,
                                                     reply_markup=kb2)