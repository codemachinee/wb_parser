# Импортируем необходимые классы из aiogram
from aiogram.fsm.state import StatesGroup, State


# Определяем класс для состояния message
class step_message(StatesGroup):
    message = State()  # Состояние для работы с сообщением