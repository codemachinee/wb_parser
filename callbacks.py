from aiogram.fsm.context import FSMContext

from wb_api import *
from aiogram.types import FSInputFile, CallbackQuery
from keyboards import *
from google_sheets import *
from database import *


async def callbacks(callback: CallbackQuery, bot, state: FSMContext):
    if callback.data == 'wb_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список складов wb.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'my_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список моих складов.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'goods_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список товаров.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_returns':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на возвраты.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_box':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на короб.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_pallet':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на монопалет.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'feedbacks':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/report_feedbacks.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'questions':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/report_questions.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'suplier_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Отчет о поставках.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'PREMIATO':
        mes = await bot.edit_message_text(f'Пожалуйста выберите причину обращения', callback.message.chat.id,
                                          callback.message.message_id, reply_markup=kb_choice_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            data_from_database = await database().search_in_table(callback.message.chat.id)
            if data_from_database[0][4] >= 4:
                await bot.edit_message_text(f'Превышен дневной лимит обращений.', callback.message.chat.id,
                                            mes.message_id)
                pass
            else:
                await database().update_table(telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')

    elif callback.data == 'choice_good':
        await bot.edit_message_text(f'Пожалуйста выберите интересующий товар:', callback.message.chat.id,
                                    callback.message.message_id, reply_markup=kb_choice_tovar)

    elif callback.data == 'package':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')

    elif callback.data == 'wrong_taste':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')

    elif callback.data == 'transfer':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на корм '
                                                                                               'PREMIATO')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на '
                                                                                                  'корм PREMIATO')

    elif callback.data == 'structure':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Состав корма')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Состав корма')

    elif callback.data == 'health':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                               'проблемах со здоровьем')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                                  'проблемах со '
                                                                                                  'здоровьем')

    elif callback.data == 'other':
        await bot.edit_message_text(f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', callback.message.chat.id,
                                    callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Другое')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Другое')

    elif callback.data == 'opt':
        await bot.edit_message_text(f'Пожалуйста <b>напишите в сообщении свой номер телефона или ссылку</b> на '
                                    f'аккаунт в телеграм, чтобы с Вами мог связался специалист.',
                                    callback.message.chat.id, callback.message.message_id, parse_mode='html',
                                    reply_markup=kb_back_to_reasons)
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')

    elif callback.data == 'slots':
        await bot.edit_message_text(f'Меню настройки уведомлений о слотах на приемку товаров.',
                                    chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=kb_slots_menu)
    elif callback.data == 'func_menu':
        await bot.edit_message_text(f'Выберите функцию:',  chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=kb1)

    elif callback.data.startswith('warehouse_'):
        ids = []
        keys_list = []
        await parse_date().get_coeffs_warehouses()
        await database().search_in_table(callback.message.chat.id, 'users_for_notification')
        wb = openpyxl.load_workbook("tables/Коэффициенты складов.xlsx")
        sheet = wb.active  # Берем активный лист (или можно указать по имени, если нужно)
        # Проходим по строкам начиная с первой строки (или с другой, если есть заголовки)
        callback.data = callback.data[10:]
        for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=3, max_col=4):
            # Проверяем значение в 3-м столбце
            if row[0].value not in ids:
                ids.append(row[0].value)
                keys_list.append([row[0].value, row[1].value])
                if row[0] == callback.data:
                    row_number = row[0].row
                    iter_0 = (int(row_number)//16)*16
                    iter_1 = (1 + int(row_number)//16)*16
                    keys_list = keys_list[iter_0:iter_1 + 1]
                    break
                else:
                    pass
            else:
                pass
        await buttons(bot, callback, keyboard_dict=keys_list, back_value='slots').warehouses_buttons()
        await bot.edit_message_text(f'Выберите интересующие склады:',  chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=kb1)

    else:
        await callback.message.reply(f'Данный раздел в разработке')
