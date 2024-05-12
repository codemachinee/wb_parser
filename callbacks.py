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
        if database().search_in_table(callback.message.chat.id) is True:
            database().update_table(telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')
        else:
            database().add_user(update_telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')

    elif callback.data == 'package':
        await bot.send_message(callback.message.chat.id, f'Пожалуйста опишите подробнее свою ситуацию, прикрепите в '
                                                         f'сообщение фото, видео (при их наличии).\n\n'
                                                         f'Постарайтесь уместить все в одном сообщении. В конце укажите'
                                                         f'свой номер телефона или ссылку на аккаунт в телеграм, чтобы'
                                                         f'с Вами связался специалист.',
                               message_thread_id=callback.message.message_thread_id)
        if database().search_in_table(callback.message.chat.id) is not False:
            database().update_table(telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')
        else:
            database().add_user(update_telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')
