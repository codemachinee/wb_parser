import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # нужно для норм видимости коневой папки

import gspread
import pytest


# @pytest.mark.skip(reason="Этот тест запускается только вручную")
@pytest.mark.asyncio
async def test_connect_to_google():
    try:
        gc = gspread.service_account(filename='pidor-of-the-day-5880592e7067.json')
        # Пытаемся открыть таблицу "clients_base_WB"
        sh = gc.open('clients_base_WB')

        # Пытаемся получить первый лист (base)
        worksheet = sh.worksheet('base')
        assert worksheet is not None
        print("Подключение к таблице успешно!")

    except gspread.SpreadsheetNotFound:
        pytest.fail("Таблица 'общая база клиентов' не найдена.")
    except Exception as e:
        pytest.fail(f"Ошибка при подключении к таблице: {str(e)}")
