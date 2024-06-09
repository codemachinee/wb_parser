from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import math
from salute import *
from FSM import step_message
from callbacks import *
token = lemonade
# token = codemashine_test

bot = Bot(token=token)
dp = Dispatcher()


@dp.message(Command(commands='start'))
async def start(message):
    if message.chat.id in admins_list:
        await bot.send_message(message.chat.id, f'<b>Бот-поддержки продаж инициализирован.</b>\n'
                               f'<b>Режим доступа</b>: Администратор\n'
                               f'/help - справка по боту', message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await database().search_in_table(message.chat.id)
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
                                                 f'/sent_message - cделать рассылку по клиентской базе.\n\n'
                                                 f'<b>Для вызова Давинчи</b> необходимо указать имя в сообщении.\n\n'
                                                 f'<b>Для перевода голосового сообщения</b>(длительность до 1 мин.) '
                                                 f'в текст ответьте на него словом "давинчи" или перешлите голосовое '
                                                 f'сообщение в личку боту.\n\n'),
                               message_thread_id=message.message_thread_id,
                               parse_mode='html')
    else:
        data_from_database = await database().search_in_table(message.chat.id)
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


@dp.callback_query(F.data)
async def check_callback(callback: CallbackQuery):
    data_from_database = await database().search_in_table(callback.message.chat.id)
    if data_from_database is not False and data_from_database[0][4] >= 6:
        pass
    else:
        await callbacks(bot, callback)


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
        data_from_database = await database().search_in_table(message.chat.id)
        if data_from_database is not False:
            if data_from_database[0][4] >= 6:
                pass
            elif data_from_database[0][4] >= 4:
                await bot.send_message(message.chat.id, f'Превышен дневной лимит обращений.')
                await database().update_table(telegram_id=message.chat.id,
                                              update_number_of_requests=data_from_database[0][4] + 1)
            else:
                mes = await bot.send_message(message.chat.id, 'Загрузка..⏳')
                await database().update_table(telegram_id=message.chat.id,
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
                        await bot.send_message(admin_account, f'Исключение вызванное проблемами подключения к '
                                                              f'гугл-таблице: {e}')
                else:
                    await bot.edit_message_text(f'Пожалуйста выберите причину обращения:', message.chat.id,
                                                mes.message_id, reply_markup=kb_choice_reasons)
        else:
            await bot.send_message(message.chat.id, f'Пожалуйста выберите интересующий товар:',
                                   message_thread_id=message.message_thread_id, reply_markup=kb_choice_tovar)


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
                for n in range(0, math.ceil(len(i) / 1020)):
                    if n == (math.ceil(len(i) / 1020) - 1):
                        await bot.send_message(group_id, f'{i[n*1020:]}', message_thread_id=343, parse_mode='HTML')
                    else:
                        await bot.send_message(group_id, f'{i[n * 1020:(n + 1) * 1020]}', message_thread_id=343,
                                               parse_mode='HTML')
    except Exception as e:
        await bot.send_message(admin_id, f'Ошибка в фyкции send_news: {e}')


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(database().delete_all_users, "cron", day_of_week='mon-sun', hour=00)
    scheduler.add_job(send_news, trigger="interval", minutes=25)
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(database().delete_all_users())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')