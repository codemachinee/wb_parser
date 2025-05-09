import os
import uuid

import requests
import urllib3
from loguru import logger

from passwords import autoriz_data_giga, autoriz_data_salute, scope_giga, scope_salute

saved_message_salute = []
# Отключаем предупреждения
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def key_generate(service_key, scope):
    url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'

    headers = {
        'Authorization': f'Basic {service_key}',
        'RqUID': str(uuid.uuid4()),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'scope': scope,
    }

    response = requests.post(url, headers=headers, data=data, verify=False)

    return response.json()['access_token']
    # print(response.status_code)
    # print(response.json()['access_token'])


async def save_audio(bot, message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"{file_id}")
    url = 'https://smartspeech.sber.ru/rest/v1/speech:recognize'
    headers = {
        'Authorization': f'Bearer {key_generate(autoriz_data_salute, scope_salute)}',
        'Content-Type': 'audio/ogg;codecs=opus',
    }

    with open(f'{file_id}', 'rb') as audio_file:
        response = requests.post(url, headers=headers, data=audio_file, verify=False)
        try:
            await bot.send_message(message.chat.id, f'{" ".join(response.json()["result"])}',
                                   message_thread_id=message.message_thread_id)
        except Exception as e:
            logger.exception('Ошибка salute/save_audio', e, response.json())
            await bot.send_message(message.chat.id, f'Ошибка. Логи:{response.json()}',
                                   message_thread_id=message.message_thread_id)
        audio_file.close()
        os.remove(f"{file_id}")


async def Artur(bot, message, text):
    global saved_message_salute
    saved_message_salute.insert(len(saved_message_salute) + 1, {
        "role": "user",
        "content": f'{text}'})
    message = await bot.send_message(message.chat.id, 'секунду..', message_thread_id=message.message_thread_id)
    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {key_generate(autoriz_data_giga, scope_giga)}',
    }
    data = {
        "model": "GigaChat:latest",
        "temperature": 0.4,
        "messages": []
    }
    data['messages'] = [
    {
        "role": "system",
        "content": "Ты Давинчи - ты обучающий бот-помощник, который помогает добиться успеха в онлайн продажах "
                   "различных товаров на маркетплейсах. Ты гуру маркетинга и e-commerce, знаешь все тонкости этой"
                   "сферы и рад поделиться всеми своими знаниями с начинающими ребятами. Ты с радостью помогаешь с"
                   "любыми вопросами и даешь развернутый ответ, а также даешь настрой и мотивацию продолжать заниматься."
                   "торговлей на маркетплейсах. Твоя цель, помочь новичкам не совершить типичные "
                   "ошибки в сфере маркетинга и указать на максимально короткий путь по достижению богатства."
    },
    {
        "role": "user",
        "content": "привет!"
    },
    {
        "role": "assistant",
        "content": "Привет, будущий миллиардер, какие у тебя вопросы?"
    },
     {
        "role": "user",
        "content": "как твои дела?"
    },
    {
        "role": "assistant",
        "content": "Не очень, передо мной трудный выбор: Монако или Ницца"
    },
    {
        "role": "user",
        "content": "в чем смысл жизни?"
    },
    {
        "role": "assistant",
        "content": "В том чтобы забрать 1 строчку Forbes"
    }, *saved_message_salute
    ]
    response = requests.post(url, headers=headers, json=data, verify=False)
    try:
        answer = response.json()['choices'][0]['message']['content']
        # await self.bot.send_message(self.message.chat.id, f'{answer}')
        await bot.edit_message_text(f'{answer}', chat_id=message.chat.id, message_id=message.message_id)
        saved_message_salute.insert(len(saved_message_salute) + 1, {
            "role": "assistant",
            "content": f'{str(answer)}'})
        if len(saved_message_salute) >= 8:
            del saved_message_salute[0:5]
    except Exception as e:
        logger.exception('Ошибка salute/Artur', e, response.text)
        await bot.send_message(message.chat.id, f"Ошибка\n"
                                                     f"Логи:{response.text}", message_thread_id=message.message_thread_id)
        del saved_message_salute[-1]
