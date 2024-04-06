from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

BTNS = {'backward': '<<',
        'forward': '>>'}


# Функция, генерирующая клавиатуру для страницы книги
def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Добавляем в билдер ряд с кнопками
    kb_builder.row(*[InlineKeyboardButton(
        text=BTNS[button] if button in BTNS else button,
        callback_data=button) for button in buttons]
                   )
    print(buttons)
    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()
