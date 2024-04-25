from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Список складов wb', callback_data='wb_warehouses')],
    [InlineKeyboardButton(text='Список моих складов', callback_data='my_warehouses')],
    [InlineKeyboardButton(text='Список товаров', callback_data='goods_list')],
    [InlineKeyboardButton(text='Тарифы на возвраты', callback_data='tariffs_returns')],
    [InlineKeyboardButton(text='Тарифы на коробы', callback_data='tariffs_box')],
    [InlineKeyboardButton(text='Тарифы на монопаллеты', callback_data='tariffs_pallet')],
    [InlineKeyboardButton(text='Необработанные отзывы по товарам', callback_data='feedbacks')],
    [InlineKeyboardButton(text='Необработанные вопросы по товарам', callback_data='questions')],
    [InlineKeyboardButton(text='Отчет о поставках', callback_data='suplier_list')]])