import aiofiles
from aiogram.fsm.context import FSMContext
from datetime import datetime
from wb_api import *
from aiogram.types import FSInputFile, CallbackQuery
from keyboards import *
from google_sheets import *
from database import *


async def callbacks(callback: CallbackQuery, bot, state: FSMContext):
    if callback.data == 'wb_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/list of warehouses.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'my_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/list of my warehouses.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'goods_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/list of products.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_returns':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/rates for refunds.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_box':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/box rates.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'tariffs_pallet':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/monopallet rates.xlsx")
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
            file_path = FSInputFile("tables/delivery report.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    elif callback.data == 'PREMIATO':
        mes = await bot.edit_message_text(text=f'Пожалуйста выберите причину обращения', chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id, reply_markup=kb_choice_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            data_from_database = await db.search_in_table(callback.message.chat.id)
            if data_from_database is not False:
                if data_from_database[1][0][4] >= 4:
                    await bot.edit_message_text(text=f'Превышен дневной лимит обращений.', chat_id=callback.message.chat.id,
                                                message_id=mes.message_id)
                    pass
            else:
                await db.update_table(telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_tovar='Сухой корм Premeato')

    elif callback.data == 'choice_good':
        await bot.edit_message_text(text='Пожалуйста выберите интересующий товар:', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, reply_markup=kb_choice_tovar)

    elif callback.data == 'package':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html',
                                    reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Проблемы с упаковкой')

    elif callback.data == 'wrong_taste':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html',
                                    reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Пришел не тот вкус')

    elif callback.data == 'transfer':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html',
                                    reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на корм '
                                                                                               'PREMIATO')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Перевод собаки на '
                                                                                                  'корм PREMIATO')

    elif callback.data == 'structure':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Состав корма')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Состав корма')

    elif callback.data == 'health':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                               'проблемах со здоровьем')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Употребление при '
                                                                                                  'проблемах со '
                                                                                                  'здоровьем')

    elif callback.data == 'other':
        await bot.edit_message_text(text=f'Пожалуйста опишите подробнее свою ситуацию, укажите номер '
                                    f'заказа, прикрепите в '
                                    f'сообщение фото, видео (при их наличии).\n\n'
                                    f'<b>Важно отправить все данные одним сообщением.</b> В конце '
                                    f'<b>укажите свой номер телефона или ссылку</b> на аккаунт в '
                                    f'телеграм, чтобы с Вами мог связался специалист.', chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id, parse_mode='html', reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Другое')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Другое')

    elif callback.data == 'opt':
        await bot.edit_message_text(text=f'Пожалуйста <b>напишите в сообщении свой номер телефона или ссылку</b> на '
                                    f'аккаунт в телеграм, чтобы с Вами мог связался специалист.',
                                    chat_id=callback.message.chat.id, message_id=callback.message.message_id, parse_mode='html',
                                    reply_markup=kb_back_to_reasons)
        if await db.search_in_table(callback.message.chat.id) is not False:
            await db.update_table(telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')
        else:
            await db.add_user(update_telegram_id=callback.message.chat.id, update_reasons='Закупка оптом')

    elif callback.data == 'slots':
        await asyncio.sleep(0.3)
        await bot.edit_message_text(text=f'Меню настройки уведомлений о слотах на приемку товаров.',
                                    chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=kb_slots_menu)
    elif callback.data == 'func_menu':
        await asyncio.sleep(0.3)
        await bot.edit_message_text(text=f'Выберите функцию:',  chat_id=callback.message.chat.id,
                                    message_id=callback.message.message_id)
        await bot.edit_message_reply_markup(chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                                            reply_markup=kb1)

    elif callback.data.startswith('warehouse_'):
        max_row = False
        keys_list = []
        user_data = await db.search_in_table(callback.message.chat.id, 'users_for_notification')
        if user_data is False:
            await db.add_user_in_users_for_notification(callback.message.chat.id,
                                                                callback.message.chat.first_name, dates=datetime.now())
            subscritions_list = []
        elif user_data[1][0][2]:
            subscritions_list = user_data[1][0][2].split(', ')
        else:
            subscritions_list = []
        call_data = callback.data[10:]
        if call_data == 'choice':
            try:
                await parse_date().get_coeffs_warehouses()
            except Exception as e:
                logger.exception('Ошибка в подключения к api(parse_date().get_coeffs_warehouses())', e)
                await bot.send_message(loggs_acc,
                                       f'Ошибка в подключения к api(parse_date().get_coeffs_warehouses()) {e}')
            async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
            box_id = data[0]["boxTypeID"]
            for index_row, row in enumerate(data):
                if len(keys_list) == 16:
                    break
                elif str(row["date"])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                    max_row = True
                    break
                elif row["boxTypeID"] == box_id:
                    keys_list.append([row["warehouseID"], row["warehouseName"], index_row])
                else:
                    pass
            if max_row is True:
                next_button = None
            else:
                next_button = f'nb{int(keys_list[-1][2]) + 1}'
            back_button = None

        elif call_data[0:2] == 'nb':
            async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
            box_id = data[0]["boxTypeID"]
            call_data = call_data[2:]
            for index_row, row in enumerate(data[int(call_data):], start=int(call_data)):
                if len(keys_list) == 16:
                    if str(row["date"])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                        max_row = True
                        break
                    break
                elif row["boxTypeID"] == box_id and str(row["date"])[0:10] == datetime.now().strftime("%Y-%m-%d"):
                    keys_list.append([row["warehouseID"], row["warehouseName"], index_row])
                elif str(row["date"])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                    max_row = True
                    break
                else:
                    pass
            if max_row is True:
                next_button = None
            else:
                next_button = f'nb{int(keys_list[-1][2])+1}'
            back_button = f'bb{int(keys_list[0][2])-1}'
        elif call_data[0:2] == 'bb':
            call_data = call_data[2:]
            async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
            box_id = data[0]["boxTypeID"]
            for index_row, row in enumerate(data[int(call_data)::-1], start=-int(call_data)):
                if len(keys_list) == 16:
                    break
                elif row["boxTypeID"] == box_id and str(row["date"])[0:10] == datetime.now().strftime("%Y-%m-%d"):
                    keys_list.append([row["warehouseID"], row["warehouseName"], abs(index_row)])
                    if index_row == 0:
                        break
                else:
                    pass
            keys_list = keys_list[::-1]
            next_button = f'nb{int(keys_list[-1][2])+1}'
            if int(keys_list[0][2]) == 0:
                back_button = None
            else:
                back_button = f'bb{int(keys_list[0][2])-1}'
        else:
            call_data = call_data.split('_')
            async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
            box_id = data[0]["boxTypeID"]
            if call_data[0] == 'del':
                subscritions_list = []
            elif str(data[int(call_data[0])]["warehouseID"]) in subscritions_list:
                subscritions_list.remove(str(data[int(call_data[0])]["warehouseID"]))
            else:
                subscritions_list.append(str(data[int(call_data[0])]["warehouseID"]))

            for index_row, row in enumerate(data[int(call_data[1]):], start=int(call_data[1])):
                if len(keys_list) == 16:
                    break
                elif row["boxTypeID"] == box_id and str(row["date"])[0:10] == datetime.now().strftime("%Y-%m-%d"):
                    keys_list.append([row["warehouseID"], row["warehouseName"], index_row])
                elif str(row['date'])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                    max_row = True
                    break
                else:
                    pass
            if max_row is True:
                next_button = None
            else:
                next_button = f'nb{int(keys_list[-1][2])+1}'
            if int(keys_list[0][2]) == 0:
                back_button = None
            else:
                back_button = f'bb{int(keys_list[0][2])-1}'
            await db.update_users_with_multiple_entries(callback.message.chat.id, 'warehouses',
                                                                subscritions_list)
        await buttons(bot, callback.message, keyboard_dict=keys_list, back_value='slots',
                      subscritions_list=subscritions_list, back_button=back_button, next_button=next_button).warehouses_buttons()

    elif callback.data.startswith('settings_'):
        if callback.data == 'settings_заглушка':
            pass
        else:
            keys_list = []
            user_data = await db.search_in_table(callback.message.chat.id, 'users_for_notification')
            if user_data is False:
                await db.add_user_in_users_for_notification(callback.message.chat.id,
                                                                    callback.message.chat.first_name, dates=datetime.now())
                subscritions_list = []
            elif user_data[1][0][2]:
                subscritions_list = user_data[1][0][2].split(', ')
            else:
                subscritions_list = []
            call_data = callback.data[9:]
            if call_data == 'change':
                if len(subscritions_list) == 0:
                    pass
                else:
                    async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                        content = await file.read()
                        data = json.loads(content)
                    for index_row, row in enumerate(data):
                        if len(keys_list) == len(subscritions_list):
                            break
                        elif str(row["date"])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                            break
                        elif str(row["warehouseID"]) in subscritions_list and row["warehouseName"] not in keys_list:
                            keys_list.append(row["warehouseName"])
                        else:
                            pass
                    subscritions_list = [user_data[1][0][3], [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')]
            else:
                if len(subscritions_list) == 0:
                    pass
                else:
                    async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                        content = await file.read()
                        data = json.loads(content)
                    for index_row, row in enumerate(data):
                        if len(keys_list) == len(subscritions_list):
                            break
                        elif str(row["date"])[0:10] == (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"):
                            break
                        elif row["warehouseID"] in subscritions_list:
                            keys_list.append(row["warehouseName"])
                        else:
                            pass
                if call_data == '2':
                    box_type_list = [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')
                    if len(box_type_list) != 0 and box_type_list[0] == '':
                        box_type_list = box_type_list[1:]
                    if "Короба" in box_type_list:
                        box_type_list.remove('Короба')
                    else:
                        box_type_list.append('Короба')
                    subscritions_list = [user_data[1][0][3], box_type_list]
                    await db.update_users_with_multiple_entries(callback.message.chat.id,
                                                                        'type_of_delivery', box_type_list)
                elif call_data == '5':
                    box_type_list = [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')
                    if len(box_type_list) != 0 and box_type_list[0] == '':
                        box_type_list = box_type_list[1:]
                    if "Монопаллеты" in box_type_list:
                        box_type_list.remove("Монопаллеты")
                    else:
                        box_type_list.append("Монопаллеты")
                    subscritions_list = [user_data[1][0][3], box_type_list]
                    await db.update_users_with_multiple_entries(callback.message.chat.id,
                                                                        'type_of_delivery', box_type_list)
                elif call_data == '6':
                    box_type_list = [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')
                    if len(box_type_list) != 0 and box_type_list[0] == '':
                        box_type_list = box_type_list[1:]
                    if "Суперсейф" in box_type_list:
                        box_type_list.remove("Суперсейф")
                    else:
                        box_type_list.append("Суперсейф")
                    subscritions_list = [user_data[1][0][3], box_type_list]
                    await db.update_users_with_multiple_entries(callback.message.chat.id,
                                                                        'type_of_delivery', box_type_list)
                elif call_data == "отсутствует":
                    box_type_list = [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')
                    if len(box_type_list) != 0 and box_type_list[0] == '':
                        box_type_list = box_type_list[1:]
                    if "QR-поставка с коробами" in box_type_list:
                        box_type_list.remove("QR-поставка с коробами")
                    else:
                        box_type_list.append("QR-поставка с коробами")
                    subscritions_list = [user_data[1][0][3], box_type_list]
                    await db.update_users_with_multiple_entries(callback.message.chat.id,
                                                                        'type_of_delivery', box_type_list)
                elif call_data == "minus":
                    koef = 1 if user_data[1][0][3] is None else int(user_data[1][0][3]) - 1
                    subscritions_list = [str(koef), [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')]
                    await db.update_table_in_users_for_notification(callback.message.chat.id,
                                                                            {'max_koeff': str(koef)})
                elif call_data == "plus":
                    koef = 3 if user_data[1][0][3] is None else int(user_data[1][0][3]) + 1
                    subscritions_list = [str(koef), [] if user_data[1][0][4] is None else user_data[1][0][4].split(', ')]
                    await db.update_table_in_users_for_notification(callback.message.chat.id,
                                                                            {'max_koeff': str(koef)})
            await buttons(bot, callback.message, keyboard_dict=keys_list, back_value='slots',
                          subscritions_list=subscritions_list).setings_buttons()
    else:
        await callback.message.reply(f'Данный раздел в разработке')
