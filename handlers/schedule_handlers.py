from datetime import date

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from keyboards.pagination_kb import create_pagination_keyboard
from services.patterns import is_valid_group_name_pattern
from services.schedule_parser import get_group_id, get_group_schedule, format_schedule_for_day

router = Router()

page_num = 1
pages_len = 1
schedule_pages = []


class Form(StatesGroup):
    waiting_for_pattern = State()


@router.message(Command('schedule'))
async def start(message: Message, state: FSMContext) -> None:
    await message.answer("Отправьте мне номер группы (например: КМБ-с-о-19-1):")
    await state.set_state(Form.waiting_for_pattern)


@router.message(Form.waiting_for_pattern)
async def handle_text_message(message: Message, state: FSMContext) -> None:
    pattern = message.text
    # Проверка соответствия строки шаблону
    if is_valid_group_name_pattern(pattern):
        group_id = get_group_id(pattern)
        if group_id == 0:
            await message.reply("Группа не найдена.")
            return
        await message.reply(f"Ваш шаблон '{pattern}' принят. Вот расписание:")
        today = date.today()
        global schedule_pages
        schedule_pages = get_group_schedule(group_id, today.strftime("%Y-%m-%d"))
        print(today.strftime("%Y-%m-%d"))
        global page_num
        global pages_len
        page_num = 1
        pages_len = len(schedule_pages)
        text = format_schedule_for_day(schedule_pages[page_num - 1])
        print(schedule_pages)
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page_num}/{pages_len}',
                'forward'
            )
        )

        # Сброс состояния
        await state.clear()
    else:
        await message.reply("Некорректный шаблон. Отправьте правильный")


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    global page_num
    if page_num < pages_len:
        page_num += 1
        text = format_schedule_for_day(schedule_pages[page_num - 1])
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page_num}/{pages_len}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    global page_num
    if page_num > 1:
        page_num -= 1
        text = format_schedule_for_day(schedule_pages[page_num - 1])
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page_num}/{pages_len}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    await callback.answer()


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")
