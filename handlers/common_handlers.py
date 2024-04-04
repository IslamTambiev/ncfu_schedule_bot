from aiogram import Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hbold


# Этот хэндлер срабатывает на команду /start
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}! Отправь мне номер своей группы чтобы получить "
                         f"расписание", reply_markup=types.ReplyKeyboardRemove())


# Этот хэндлер срабатывает на команду /help
async def process_help_command(message: Message) -> None:
    await message.answer(text='/help')


# Этот хэндлер срабатывает на команду /cancel
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Состояние сброшено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher) -> None:
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(process_help_command, Command(commands='help'))
    dp.message.register(cmd_cancel, Command(commands='stop'))
    dp.message.register(cmd_cancel, F.text.lower() == "стоп")
