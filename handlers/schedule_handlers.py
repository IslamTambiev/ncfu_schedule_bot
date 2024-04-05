import re
from datetime import date

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.schedule_parser import get_group_id, get_group_schedule, format_schedule_for_day

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
        group_id = get_group_id(pattern)
        if group_id == 0:
            await message.reply("Группа не найдена.")
            return
        await message.reply(f"Ваш шаблон '{pattern}' принят. Вот расписание:")
        today = date.today()
        group_schedule = get_group_schedule(group_id, today.strftime("%Y-%m-%d"))
        print(today.strftime("%Y-%m-%d"))
        formated_group_schedule = format_schedule_for_day(group_schedule[0])
        await message.answer(formated_group_schedule)

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
