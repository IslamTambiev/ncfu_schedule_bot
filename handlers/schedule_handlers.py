import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

router = Router()


class Form(StatesGroup):
    waiting_for_pattern = State()


@router.message(Command('schedule'))
async def start(message: Message, state: FSMContext) -> None:
    await message.answer("Отправьте мне номер группы:")
    await state.set_state(Form.waiting_for_pattern)


@router.message(Form.waiting_for_pattern)
async def handle_text_message(message: Message, state: FSMContext) -> None:
    pattern = message.text
    # Проверка соответствия строки шаблону
    if is_valid_pattern(pattern):
        await message.reply(f"Ваш шаблон '{pattern}' принят.")
        # Сброс состояния
        await state.clear()
    else:
        await message.reply("Некорректный шаблон.")


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


def is_valid_pattern(pattern: str) -> bool:
    # Паттерн для соответствия формату "aaa-a-a-11-1"
    regex_pattern = r'^[а-яА-Я]{3}-[а-яА-Я]-[а-яА-Я]-\d{2}-\d$'
    # Проверка соответствия строки шаблону
    return bool(re.match(regex_pattern, pattern))
