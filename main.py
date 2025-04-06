import asyncio
import json
import math
from datetime import datetime, timedelta, timezone

import aiofiles
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from callbacks import callbacks
from database import db
from FSM import step_message
from functions import sheduler_block_value
from google_sheets import clients_base
from keyboards import kb1, kb_choice_reasons, kb_choice_tovar
from passwords import admin_id, admins_list, group_id, lemonade, loggs_acc
from salute import Artur, save_audio
from wb_api import parse_date

# Удаляем стандартный обработчик
logger.remove()
# Настраиваем логирование в файл с ограничением количества файлов
logger.add(
    "loggs.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="5 MB",  # Ротация файла каждые 10 MB
    retention="10 days",  # Хранить только 5 последних логов
    compression="zip",  # Сжимать старые логи в архив
    backtrace=True,     # Сохранение трассировки ошибок
    diagnose=True       # Подробный вывод
)


token = lemonade
# token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message):
    if message.chat.id in admins_list:
        # await send_news()
        await bot.send_message(message.chat.id, '<b>Бот-поддержки продаж инициализирован.</b>\n'
                               '<b>Режим доступа</b>: Администратор\n'
                               '/help - справка по боту', message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await db.search_in_table(message.chat.id)
        if data_from_database is not False and data_from_database[1][0][4] >= 6:
            pass
        else:
            await bot.send_message(message.chat.id, f'<b>Здравствуйте {message.from_user.first_name}!</b>\n\n'
                                   f'<b>Бот-поддержки клиентов</b> инициализирован.\n'
                                   f'/help - справка по боту', message_thread_id=message.message_thread_id,
                                   parse_mode='html')
            await bot.send_message(message.chat.id, 'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


@dp.message(Command(commands='help'))
async def help(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, ('<b>Основные команды поддерживаемые ботом:</b>\n'
                                                 '/start - инициализация бота,\n'
                                                 '/help - справка по боту,\n'
                                                 '/func - вызов функциональной клавиатуры бота.\n'
                                                 '/sent_message - cделать рассылку по клиентской базе.\n'
                                                 '/reset_cash - cбросить кэш базы данных.\n\n'
                                                 '<b>Для вызова Давинчи</b> необходимо указать имя в сообщении.\n\n'
                                                 '<b>Для перевода голосового сообщения</b>(длительность до 1 мин.) '
                                                 'в текст ответьте на него словом "давинчи" или перешлите голосовое '
                                                 'сообщение в личку боту.\n\n'),
                               message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await db.search_in_table(message.chat.id)
        if data_from_database is not False and data_from_database[1][0][4] >= 6:
            pass
        else:
            await bot.send_message(message.chat.id, '<b>Бот</b> служит для автоматизации процессса обработки клиентских '
                                   'обращений по проблемным и иным вопросам.\n\n'
                                   '<b>Список команд:</b>\n'
                                   '/start - инициализация бота,\n'
                                   '/help - справка по боту.\n\n'
                                   'Разработка ботов любой сложности @hlapps', message_thread_id=message.message_thread_id,
                                   parse_mode='html')


@dp.message(Command(commands='func'))
async def functions(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, 'Выберите функцию:',
                               message_thread_id=message.message_thread_id, reply_markup=kb1)
    else:
        await bot.send_message(message.chat.id, 'Недостаточно прав',
                               message_thread_id=message.message_thread_id)


@dp.message(Command(commands='reset_cash'))
async def reset_cash(message):
    if message.chat.id in admins_list:
        await db.delete_all_users()
        await bot.send_message(message.chat.id, 'Кэш очищен',
                               message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id, 'Недостаточно прав',
                               message_thread_id=message.message_thread_id)


@dp.message(Command(commands='sent_message'))
async def sent_message(message, state: FSMContext):
    if message.chat.id == admin_id:
        await bot.send_message(message.chat.id, 'Введите текст сообщения',
                               message_thread_id=message.message_thread_id)
        await state.set_state(step_message.message)

    else:
        await bot.send_message(message.chat.id, 'Недостаточно прав', message_thread_id=message.message_thread_id)


@dp.message(step_message.message)
async def perehvat(message, state: FSMContext):
    await clients_base(bot, message).rasylka_v_bazu()
    await state.clear()


dp.callback_query.register(callbacks, F.data)


@dp.message(F.text, F.chat.type == 'private')
async def chek_message(message):
    if 'Давинчи' in message.md_text:
        try:
            if message.reply_to_message.voice.file_id:
                await save_audio(bot, message.reply_to_message)
        except AttributeError:
            b = str(message.text).replace('Давинчи ', '', 1).replace('Давинчи, ', '', 1).replace('Давинчи,', '',
                                                                                             1).replace(
                ' Давинчи', '', 1)
            await Artur(bot, message, b)
    elif 'давинчи' in message.md_text:
        try:
            if message.reply_to_message.voice.file_id:
                await save_audio(bot, message.reply_to_message)
        except AttributeError:
            b = str(message.text).replace('давинчи ', '', 1).replace('давинчи, ', '',
                                                                     1).replace('давинчи,', '',
                                                                                1).replace(' давинчи', '', 1)
            await Artur(bot, message, b)
    elif message.chat.id not in admins_list:
        data_from_database = await db.search_in_table(message.chat.id)
        if data_from_database is not False:
            if data_from_database[1][0][4] >= 6:
                pass
            elif data_from_database[1][0][4] >= 4:
                await bot.send_message(message.chat.id, 'Превышен дневной лимит обращений.')
                await db.update_table(telegram_id=message.chat.id,
                                              update_number_of_requests=data_from_database[1][0][4] + 1)
            else:
                mes = await bot.send_message(message.chat.id, 'Загрузка..⏳')
                await db.update_table(telegram_id=message.chat.id,
                                              update_number_of_requests=data_from_database[1][0][4] + 1)
                if data_from_database[1][0][2]:
                    try:
                        await clients_base(bot, message, data_from_database[1][0][1]).record_in_base(data_from_database[1][0][2],
                                                                                                  message.md_text)             # применяем message.md_text, потоому что при отправке текста с картинкой message.text = None
                        await bot.send_message(group_id, f'🚨!!!СРОЧНО!!!🚨\n'
                                                         f'Поступило  ОБРАЩЕНИЕ от:\n'
                                                         f'Ссылка: @{message.from_user.username}\n'
                                                         f'id чата: {message.chat.id}\n'
                                                         f'Товар: {data_from_database[1][0][1]}\n'
                                                         f'Причина: {data_from_database[1][0][2]}\n'
                                                         f'Ссылка на базу: https://docs.google.com/spreadsheets/d/1gPsql3jmemm'
                                                         f'NbUbN0SQ16NTlYF8omWO4dsbRllJBElw/edit#gid=0\n', message_thread_id=343)

                        await bot.copy_message(group_id, message.chat.id, message.message_id, message_thread_id=343)
                        await bot.edit_message_text(text='Спасибо за обращение, с Вами скоро свяжутся.', chat_id=message.chat.id,
                                                    message_id=mes.message_id)
                    except Exception as e:
                        logger.exception('Исключение вызванное проблемами подключения к гугл-таблице', e)
                        await bot.send_message(loggs_acc, f'Исключение вызванное проблемами подключения к '
                                                               f'гугл-таблице: {e}')
                else:
                    await bot.edit_message_text(text='Пожалуйста выберите причину обращения:', chat_id=message.chat.id,
                                                message_id=mes.message_id, reply_markup=kb_choice_reasons)
        else:
            await bot.send_message(message.chat.id, 'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


@dp.message(F.voice, F.chat.type == 'private')
async def chek_voice_message(v):
    try:
        await save_audio(bot, v)
    except Exception as e:
        logger.exception('Ошибка в main/chek_voice_message', e)
        await bot.send_message(loggs_acc, f'Ошибка в main/chek_voice_message: {e}')


async def send_news():
    if sheduler_block_value.news is True:
        try:
            message = await parse_date().get_news()
            if message is None:
                pass
            else:
                for i in message:
                    for n in range(0, math.ceil(len(i) / 1020)):
                        if n == (math.ceil(len(i) / 1020) - 1):
                            await asyncio.sleep(0.1)
                            await bot.send_message(group_id, f'{i[n*1020:]}', message_thread_id=343, parse_mode='HTML')
                        else:
                            await asyncio.sleep(0.1)
                            await bot.send_message(group_id, f'{i[n * 1020:(n + 1) * 1020]}', message_thread_id=343,
                                                   parse_mode='HTML')
        except Exception as e:
            logger.exception('Ошибка в main/send_news', e)
            await bot.send_message(loggs_acc, f'Ошибка в фyкции send_news: {e}')

    else:
        pass


async def search_warehouses():
    if sheduler_block_value.warehouses is True:
        try:
            base_data_users = await db.return_base_data()
            input_date_obj = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
            input_date_obj = datetime.strptime(input_date_obj, "%Y-%m-%dT%H:%M:%SZ")
            await db.delete_old_messages()
            if base_data_users is False:
                pass
            else:
                try:
                    await parse_date().get_coeffs_warehouses()
                except Exception as e:
                    logger.exception('Ошибка в подключения к api(parse_date().get_coeffs_warehouses())', e)
                    await bot.send_message(loggs_acc, f'Ошибка в подключения к api(parse_date().get_coeffs_warehouses()) {e}')
                async with aiofiles.open('coeffs_from_api.json', 'r', encoding='utf-8') as file:
                    content = await file.read()
                    data = json.loads(content)
                for i in base_data_users:
                    mess_counter = 0
                    if i[1] is not None and i[3] is not None:
                        warehouses_list = i[1].split(', ')
                        mess_max = len(warehouses_list) * 7 * len(i[3].split(', '))
                        for row in data:
                            if datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%SZ") > datetime.now() + timedelta(days=7):
                                break
                            elif datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%SZ") < input_date_obj:
                                pass
                            else:
                                if str(row["warehouseID"]) in warehouses_list:
                                    if row["boxTypeName"] in i[3]:
                                        mess_counter += 1
                                        # if int(row[1].value) <= int(i[2]):
                                        if str(row["coefficient"]) != '-1' and int(row["coefficient"]) <= int(i[2]):
                                            messages_base = await db.return_base_messages(str(i[0]), str(row["warehouseID"]),
                                                                                  row["boxTypeName"], row["date"])
                                            if messages_base is False:
                                                await db.add_message(str(i[0]), str(row["warehouseID"]),
                                                                             row["coefficient"], row["boxTypeName"],
                                                                             row["date"])
                                                await asyncio.sleep(0.033)
                                                await bot.send_message(int(i[0]), f'*Появился слот на приемку товара!*\n\n'
                                                                                  f'*склад:* {row["warehouseName"]}\n'
                                                                                  f'*тип поставки:* {row["boxTypeName"]}\n'
                                                                                  f'*коэффициент приемки:* {row["coefficient"]}\n'
                                                                                  f'*дата:* {row["date"][:10]}\n\n'
                                                                                  f'[создать поставку](https://seller.wildberries.ru'
                                                                                  f'/supplies-management/new-supply/goods?draftID='
                                                                                  f'de3416a0-28de-4ae1-9e6e-0e2f18d63ce9)',
                                                                       parse_mode="Markdown")
                                            elif int(messages_base[0][2]) > int(row["coefficient"]):
                                                await db.update_messages_koeff(str(i[0]), str(row["warehouseID"]),
                                                                             row["coefficient"], row["boxTypeName"],
                                                                             row["date"])
                                                await asyncio.sleep(0.033)
                                                await bot.send_message(int(i[0]), f'*СНИЖЕНИЕ коэффициента приемки товара!*\n\n'
                                                                                  f'*склад:* {row["warehouseName"]}\n'
                                                                                  f'*тип поставки:* {row["boxTypeName"]}\n'
                                                                                  f'*коэффициент приемки:* {row["coefficient"]}\n'
                                                                                  f'*дата:* {row["date"][:10]}\n\n'
                                                                                  f'[создать поставку](https://seller.wildberries.ru'
                                                                                  f'/supplies-management/new-supply/goods?draftID='
                                                                                  f'de3416a0-28de-4ae1-9e6e-0e2f18d63ce9)',
                                                                       parse_mode="Markdown")
                                            else:
                                                pass
                                            if mess_counter >= mess_max:
                                                break
                                        else:
                                            if mess_counter >= mess_max:
                                                break
                                    else:
                                        pass
                                else:
                                    pass

                    else:
                        pass
        except Exception as e:
            logger.exception('Ошибка в main/search_warehouses', e)
            await bot.send_message(loggs_acc, f'Ошибка в main/search_warehouses: {e}')
    else:
        pass


async def main():
    await db.chek_tables()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(db.delete_all_users, "cron", day_of_week='mon-sun', hour=00)
    # scheduler.add_job(db.delete_all_users, trigger="interval", seconds=15)
    scheduler.add_job(send_news, trigger="interval", minutes=10, misfire_grace_time=60, coalesce=True)
    scheduler.add_job(search_warehouses, trigger="interval", minutes=4, misfire_grace_time=60, coalesce=True)
    # scheduler.add_job(send_news, "cron", day_of_week='mon-sun', hour=14, minute=33, misfire_grace_time=60, coalesce=True)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        logger.info('включение бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        asyncio.run(db.close())
        logger.exception('выключение бота')
