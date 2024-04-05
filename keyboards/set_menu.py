from aiogram import Bot
from aiogram.types import BotCommand


# Регистрация команд, отображаемых в интерфейсе Telegram
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/stop", description="Завершить состояние"),
        BotCommand(command="/help", description="Справка"),
        BotCommand(command="/schedule", description="Расписание группы")
    ]
    await bot.set_my_commands(main_menu_commands)
