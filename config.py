from dataclasses import dataclass
from environs import Env


@dataclass
class TgBotConfig:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Config:
    tg_bot: TgBotConfig


def load_config() -> Config:
    """
    Load the configuration settings from the environment variables and create a Config object.

    Returns:
        Config: The configuration object containing the loaded settings.
    """
    # Создаем экземпляр класса Env
    env: Env = Env()
    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env()

    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    return Config(tg_bot=TgBotConfig(token=env('BOT_TOKEN')))


config: Config = load_config()
