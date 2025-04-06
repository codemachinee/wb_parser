# Импортируем необходимые классы из aiogram
from aiogram.fsm.state import State, StatesGroup


# Определяем класс для состояния message
class step_message(StatesGroup):
    message = State()  # Состояние для работы с сообщением
