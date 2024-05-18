from wb_api import *
from aiogram.types import FSInputFile
from keyboards import *
from google_sheets import *
from database import *


async def callbacks(bot, callback):
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
        await bot.send_message(callback.message.chat.id, f'Пожалуйста выберите причину обращения',
                               message_thread_id=callback.message.message_thread_id, reply_markup=kb_choice_reasons)
        if await database().search_in_table(callback.message.chat.id) is True:
            await database().update_table(telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')

    elif callback.data == 'package':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')

    elif callback.data == 'wrong_taste':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')

    elif callback.data == 'transfer':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на корм '
                                                                                               'PREMIATO')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на '
                                                                                                  'корм PREMIATO')

    elif callback.data == 'structure':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Состав корма')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Состав корма')

    elif callback.data == 'health':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                               'проблемах со здоровьем')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                                  'проблемах со '
                                                                                                  'здоровьем')

    elif callback.data == 'other':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                                         f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                                         f'телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Другое')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Другое')

    elif callback.data == 'opt':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста <b>укажите свой номер телефона или ссылку</b> на '
                                                         f'аккаунт в телеграм, чтобы с Вами мог связался специалист.',
                               message_thread_id=callback.message.message_thread_id, parse_mode='html')
        if await database().search_in_table(callback.message.chat.id) is not False:
            await database().update_table(telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')
        else:
            await database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')