from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import math
from salute import *
from FSM import step_message
from callbacks import *
from loguru import logger

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

logger.add(
    "errors.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="ERROR",
    rotation="5 MB",
    retention="10 days",
    compression="zip",
    backtrace=True,     # Сохранение трассировки ошибок
    diagnose=True       # Подробный вывод
)

# token = lemonade
token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message):
    if message.chat.id in admins_list:
        # await send_news()
        await bot.send_message(message.chat.id, f'<b>Бот-поддержки продаж инициализирован.</b>\n'
                               f'<b>Режим доступа</b>: Администратор\n'
                               f'/help - справка по боту', message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await Database().search_in_table(message.chat.id)
        if data_from_database is not False and data_from_database[0][4] >= 6:
            pass
        else:
            await bot.send_message(message.chat.id, f'<b>Здравствуйте {message.from_user.first_name}!</b>\n\n'
                                   f'<b>Бот-поддержки клиентов</b> инициализирован.\n'
                                   f'/help - справка по боту', message_thread_id=message.message_thread_id,
                                   parse_mode='html')
            await bot.send_message(message.chat.id, f'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


@dp.message(Command(commands='help'))
async def help(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, (f'<b>Основные команды поддерживаемые ботом:</b>\n'
                                                 f'/start - инициализация бота,\n'
                                                 f'/help - справка по боту,\n'
                                                 f'/func - вызов функциональной клавиатуры бота.\n'
                                                 f'/sent_message - cделать рассылку по клиентской базе.\n'
                                                 f'/reset_cash - cбросить кэш базы данных.\n\n'
                                                 f'<b>Для вызова Давинчи</b> необходимо указать имя в сообщении.\n\n'
                                                 f'<b>Для перевода голосового сообщения</b>(длительность до 1 мин.) '
                                                 f'в текст ответьте на него словом "давинчи" или перешлите голосовое '
                                                 f'сообщение в личку боту.\n\n'),
                               message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await Database().search_in_table(message.chat.id)
        if data_from_database is not False and data_from_database[0][4] >= 6:
            pass
        else:
            await bot.send_message(message.chat.id, f'<b>Бот</b> служит для автоматизации процессса обработки клиентских '
                                   f'обращений по проблемным и иным вопросам.\n\n'
                                   f'<b>Список команд:</b>\n'
                                   f'/start - инициализация бота,\n'
                                   f'/help - справка по боту.\n\n'
                                   f'Разработка ботов любой сложности @hlapps', message_thread_id=message.message_thread_id,
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
async def functions(message):
    if message.chat.id in admins_list:
        await Database().delete_all_users()
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


@dp.message(F.text)
@dp.message(F.chat.type == 'private')
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
        data_from_database = await Database().search_in_table(message.chat.id)
        if data_from_database is not False:
            if data_from_database[0][4] >= 6:
                pass
            elif data_from_database[0][4] >= 4:
                await bot.send_message(message.chat.id, f'Превышен дневной лимит обращений.')
                await Database().update_table(telegram_id=message.chat.id,
                                              update_number_of_requests=data_from_database[0][4] + 1)
            else:
                mes = await bot.send_message(message.chat.id, 'Загрузка..⏳')
                await Database().update_table(telegram_id=message.chat.id,
                                              update_number_of_requests=data_from_database[0][4] + 1)
                if data_from_database[0][2]:
                    try:
                        await clients_base(bot, message, data_from_database[0][1]).record_in_base(data_from_database[0][2],
                                                                                                  message.md_text)             # применяем message.md_text, потоому что при отправке текста с картинкой message.text = None
                        await bot.send_message(group_id, f'🚨!!!СРОЧНО!!!🚨\n'
                                                         f'Поступило  ОБРАЩЕНИЕ от:\n'
                                                         f'Ссылка: @{message.from_user.username}\n'
                                                         f'id чата: {message.chat.id}\n'
                                                         f'Товар: {data_from_database[0][1]}\n'
                                                         f'Причина: {data_from_database[0][2]}\n'
                                                         f'Ссылка на базу: https://docs.google.com/spreadsheets/d/1gPsql3jmemm'
                                                         f'NbUbN0SQ16NTlYF8omWO4dsbRllJBElw/edit#gid=0\n', message_thread_id=343)

                        await bot.copy_message(group_id, message.chat.id, message.message_id, message_thread_id=343)
                        await bot.edit_message_text(f'Спасибо за обращение, с Вами скоро свяжутся.', message.chat.id,
                                                    mes.message_id)
                    except Exception as e:
                        logger.exception('Исключение вызванное проблемами подключения к гугл-таблице', e)
                        await bot.send_message(loggs_acc, f'Исключение вызванное проблемами подключения к '
                                                               f'гугл-таблице: {e}')
                else:
                    await bot.edit_message_text(f'Пожалуйста выберите причину обращения:', message.chat.id,
                                                mes.message_id, reply_markup=kb_choice_reasons)
        else:
            await bot.send_message(message.chat.id, f'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


@dp.message(F.voice, F.chat.type == 'private')
async def chek_message(v):
    try:
        await save_audio(bot, v)
    except Exception as e:
        logger.exception('Ошибка в main/save_audio', e)
        await bot.send_message(loggs_acc, f'Ошибка в main/save_audio: {e}')


async def send_news():
    try:
        message = await parse_date().get_news()
        if message is None:
            pass
        else:
            for i in message:
                for n in range(0, math.ceil(len(i) / 1020)):
                    if n == (math.ceil(len(i) / 1020) - 1):
                        await bot.send_message(group_id, f'{i[n*1020:]}', message_thread_id=343, parse_mode='HTML')
                    else:
                        await bot.send_message(group_id, f'{i[n * 1020:(n + 1) * 1020]}', message_thread_id=343,
                                               parse_mode='HTML')
    except Exception as e:
        logger.exception('Ошибка в main/send_news', e)
        await bot.send_message(loggs_acc, f'Ошибка в фyкции send_news: {e}')


async def search_warehouses():
    try:
        base_data = await Database().return_base_data()
        if base_data is False:
            pass
        else:
            for i in base_data:
                mess_counter = 0
                if len(i[1]) is not None and len(i[3]) is not None:
                    warehouses_list = i[1].split(', ')
                    mess_max = len(warehouses_list) * 7 * len(i[3].split(', '))
                    await parse_date().get_coeffs_warehouses()
                    wb = openpyxl.load_workbook("tables/Коэффициенты складов.xlsx")
                    sheet = wb.active  # Берем активный лист (или можно указать по имени, если нужно)
                    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=6):
                        if str(row[2].value) in warehouses_list:
                            if str(row[4].value) in i[3]:
                                mess_counter += 1
                                # if int(row[1].value) <= int(i[2]):
                                if str(row[1].value) != '-1' and int(row[1].value) <= int(i[2]):
                                    await bot.send_message(int(i[0]), f'*Появился слот на приемку товара!*\n\n'
                                                                      f'*склад:* {row[3].value}\n'
                                                                      f'*тип поставки:* {row[4].value}\n'
                                                                      f'*коэффициент приемки:* {row[1].value}\n'
                                                                      f'*дата:* {row[0].value}\n\n'
                                                                      f'[создать поставку](https://seller.wildberries.ru'
                                                                      f'/supplies-management/new-supply/goods?draftID='
                                                                      f'de3416a0-28de-4ae1-9e6e-0e2f18d63ce9)',
                                                           parse_mode="Markdown")
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


async def main():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(send_news, trigger="interval", minutes=10)
    scheduler.add_job(search_warehouses, trigger="interval", seconds=15)
    Database().schedule_task()
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(Database().delete_all_users())
    except Exception as e:
        logger.exception('Ошибка в main/asyncio.run(Database().delete_all_users())', e)
        asyncio.run(bot.send_message(loggs_acc, f'Ошибка в main/search_warehouses: {e}'))
    try:
        logger.info('включение бота')
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.exception('выключение бота')