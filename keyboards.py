from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from wb_api import

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
    [InlineKeyboardButton(text='📦 Выбор склада', callback_data='opt')],
    [InlineKeyboardButton(text='⚙️ Настройка склада', callback_data='package')],
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