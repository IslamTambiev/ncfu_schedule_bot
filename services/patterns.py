import re


def is_valid_group_name_pattern(pattern: str) -> bool:
    # Паттерн для соответствия формату "aaa-a-a-11-1"
    regex_pattern = r'^[а-яА-Я]{3}-[а-яА-Я]-[а-яА-Я]-\d{2}-\d$'
    # Проверка соответствия строки шаблону
    return bool(re.match(regex_pattern, pattern))
