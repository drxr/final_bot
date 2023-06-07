from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from functions.common import get_dates_from_data


# Основная клавиатура для внесения операций
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


# Клавиатура выбора месяца отчета



# Клавиатура выбора года отчета

