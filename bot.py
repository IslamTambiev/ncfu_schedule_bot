import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from keyboards.set_menu import set_main_menu
from handlers import schedule_handlers
from handlers.common_handlers import register_handlers_common

from config import config

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция для регистрации всех хэндлеров
def register_all_handlers(dp: Dispatcher) -> None:
    register_handlers_common(dp)


# Функция для регистрации всех роутеров
def register_all_routers(dp) -> None:
    dp.include_router(schedule_handlers.router)


# Функция конфигурирования и запуска бота
async def main():
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s - %(lineno)d - (%(filename)s).%(funcName)s(%("
               "lineno)d)",
    )
    # Выводим информацию о начале запуска бота
    logger.info("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрируем все хэндлеры
    register_all_handlers(dp)

    # Регистрируем все роутеры
    register_all_routers(dp)

    # Установка команд бота
    await set_main_menu(bot)

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.close()


if __name__ == '__main__':
    try:
        # Запускаем функцию main
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Bot stopped!')
