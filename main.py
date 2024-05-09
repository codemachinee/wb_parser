from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from wb_api import *
from keyboards import *
from salute import *
from FSM import step_message
from google_sheets import *
# token = lemonade
token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, f'Бот-поддержки продаж инициализирован.\n'
                               f'Режим доступа: Администратор\n'
                               f'/help - справка по боту', message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.first_name}!\n'
                               f'Бот-поддержки клиентов инициализирован.\n'
                               f'/help - справка по боту', message_thread_id=message.message_thread_id)
        await bot.send_message(message.chat.id, f'Пожалуйста выберите интересующий товар:',
                               message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


@dp.message(Command(commands='help'))
async def help(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, (f'Основные команды поддерживаемые ботом:\n'
                                                 f'/start - инициализация бота,\n'
                                                 f'/help - справка по боту,\n'
                                                 f'/func - вызов функциональной клавиатуры бота.\n'
                                                 f'/sent_message - cделать рассылку по клиентской базе.\n'
                                                 f'Для вызова Давинчи необходимо указать имя в сообщении.\n\n'
                                                 f'Для перевода голосового сообщения(длительность до 1 мин.) в текст '
                                                 f'ответьте на него словом "давинчи" или перешлите голосовое сообщение '
                                                 f'в личку боту.\n\n'), message_thread_id=message.message_thread_id)
    else:
        await bot.send_message(message.chat.id, f'Бот служит для автоматизации процессса обработки клиентских '
                               f'обращений по проблемным и иным вопросам.\n'
                               f'Список команд:\n'
                               f'/start - инициализация бота,\n'
                               f'/help - справка по боту.\n\n'
                               f'Разработка ботов любой сложности @hlapps', message_thread_id=message.message_thread_id)


# @dp.message(Command(commands='test'))
# async def help(message):
#     await bot.send_message(group_id, f'<em>Привет меня зовут Молли</em>', parse_mode='HTML', message_thread_id=2109)


@dp.message(Command(commands='func'))
async def functions(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, 'Выберите функцию:',
                               message_thread_id=message.message_thread_id, reply_markup=kb1)
    else:
        await bot.send_message(message.chat.id, 'Недостаточно прав',
                               message_thread_id=message.message_thread_id)


@dp.message(Command(commands='sent_message'))  # команда для переброски клиента из базы потенциальных клиентов в
async def sent_message(message, state: FSMContext):  # базу старых клиентов
    if message.chat.id == admin_id:
        await bot.send_message(message.chat.id, 'Введите текст сообщения',
                               message_thread_id=message.message_thread_id,)
        await state.set_state(step_message.message)

    else:
        await bot.send_message(message.chat.id, 'Недостаточно прав')


@dp.message(step_message.message)
async def perehvat(message, state: FSMContext):
    await clients_base(bot, message).rasylka_v_bazu()
    await Message.answer(message, text='Рассылка осуществлена', show_allert=True)
    await state.clear()


@dp.callback_query(F.data)
async def check_callback(callback: CallbackQuery):
    if callback.data == 'wb_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список складов wb.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'my_warehouses':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список моих складов.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'goods_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/список товаров.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_returns':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на возвраты.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_box':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на короб.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'tariffs_pallet':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Тарифы на монопалет.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'feedbacks':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/report_feedbacks.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'questions':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/report_questions.xlsx")
            await bot.send_document(callback.message.chat.id, file_path,
                                    message_thread_id=callback.message.message_thread_id)
        else:
            await bot.send_message(callback.message.chat.id, f'Исключение:{data}',
                                   message_thread_id=callback.message.message_thread_id)
    if callback.data == 'suplier_list':
        data = await parse_date().get_wb_warehouses()
        if data is None:
            file_path = FSInputFile("tables/Отчет о поставках.xlsx")
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