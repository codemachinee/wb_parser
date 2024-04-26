from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from wb_api import *
from keyboards import *
from salute import *

token = lemonade
# token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message):
    await bot.send_message(message.chat.id, '''Бот уже инициализирован.
Новости присылаются ежедневно в 11:00 по московскому времени

/help - справка по боту''', message_thread_id=message.message_thread_id)


@dp.message(Command(commands='help'))
async def help(message):
    await bot.send_message(message.chat.id, (f'Основные команды поддерживаемые ботом:\n'
                                             f'/start - инициализация бота,\n'
                                             f'/help - справка по боту,\n'
                                             f'/func - вызов функциональной клавиатуры бота.\n\n'
                                             f'Для вызова Давинчи необходимо указать имя в сообщении.\n\n'
                                             f'Для перевода голосового сообщения(длительность до 1 мин.) в текст '
                                             f'ответьте на него словом "давинчи" или перешлите голосовое сообщение '
                                             f'в личку боту.\n\n'), message_thread_id=message.message_thread_id)


# @dp.message(Command(commands='test'))
# async def help(message):
#     await bot.send_message(group_id, f'<em>Привет меня зовут Молли</em>', parse_mode='HTML', message_thread_id=2109)


@dp.message(Command(commands='func'))
async def functions(message):
    await bot.send_message(message.chat.id, 'Функции бота..', message_thread_id=message.message_thread_id,
                           reply_markup=kb1,)


@dp.callback_query(F.data)
async def check_callback(callback: CallbackQuery):
    if callback.data == 'wb_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("список складов wb.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'my_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("список моих складов.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'goods_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("список товаров.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_returns':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("Тарифы на возвраты.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_box':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("Тарифы на короб.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_pallet':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("Тарифы на монопалет.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'feedbacks':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("report_feedbacks.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'questions':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("report_questions.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'suplier_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("Отчет о поставках.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)


# @dp.message(F.text)
# async def chek_message(message):
#     print(message)

@dp.message(F.text)
async def chek_message(message):
    if 'Давинчи' in message.text:
        try:
            if message.reply_to_message.voice.file_id:
                await save_audio(bot, message.reply_to_message)
        except AttributeError:
            b = str(message.text).replace('Давинчи ', '', 1).replace('Давинчи, ', '', 1).replace('Давинчи,', '',
                                                                                             1).replace(
                ' Давинчи', '', 1)
            await Artur(bot, message, b)
    elif 'давинчи' in message.text:
        try:
            if message.reply_to_message.voice.file_id:
                await save_audio(bot, message.reply_to_message)
        except AttributeError:
            b = str(message.text).replace('давинчи ', '', 1).replace('давинчи, ', '',
                                                                     1).replace('давинчи,', '',
                                                                                1).replace(' давинчи', '', 1)
            await Artur(bot, message, b)


@dp.message(F.voice, F.chat.type == 'private')
async def chek_message(v):
    await save_audio(bot, v)


async def send_news():
    try:
        message = await parse_date().get_news()
        if message is None:
            pass
        else:
            for i in message:
                if len(i) < 1023:
                    await bot.send_message(group_id, f'{i}', message_thread_id=343, parse_mode='HTML')
                else:
                    with open('news.txt', 'r') as file:
                        file_id = file.read()
                    index_end = i.find(f'{str(int(file_id[:4]) - 2)}')
                    await bot.send_message(group_id, f'{i[:index_end]}', message_thread_id=343, parse_mode='HTML')
                    await bot.send_message(group_id, f'{i[index_end:]}', message_thread_id=343, parse_mode='HTML')
    except Exception as e:
        await bot.send_message(admin_id, f'Ошибка в фyкции send_news: {e}')


async def main():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(pidr, "cron", day_of_week='mon-sun', hour=11)
    scheduler.add_job(send_news, trigger="interval", hours=3)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')