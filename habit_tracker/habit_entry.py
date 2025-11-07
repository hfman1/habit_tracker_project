# habit_entry.py
"""
Ввод и валидация данных для Habit Tracker.

Содержит функции по валидации названия, даты и целого числа.
Все функции документированы в стиле Google.
"""

from datetime import datetime
import re


DATE_FORMAT = "%d-%m-%Y"


def validate_name(name: str) -> bool:
    """
    Проверяет корректность названия привычки.

    Args:
        name (str): Название привычки.

    Returns:
        bool: True если название корректно (не пустое, не длиннее 100, без спецсимволов).
    """
    if not isinstance(name, str):
        raise TypeError("name must be a string")
    name = name.strip()
    if not name:
        return False
    if len(name) > 100:
        return False
    # Разрешаем буквы, цифры, пробелы, дефис и подчёркивание
    return bool(re.match(r"^[\w\s\-]+$", name))


def validate_category(category: str) -> bool:
    """
    Проверка категории (необязательное поле, но если задано — должно быть строкой).
    """
    if category is None:
        return True
    if not isinstance(category, str):
        raise TypeError("category must be a string or None")
    return 0 < len(category.strip()) <= 50


def parse_date(text: str) -> datetime:
    """
    Парсит дату в формате DD-MM-YYYY. Если пусто — возвращает сегодняшнюю дату.

    Args:
        text (str): Текст даты.

    Returns:
        datetime: parsed date

    Raises:
        ValueError: если формат неверный.
    """
    if text is None or not str(text).strip():
        return datetime.now()
    try:
        return datetime.strptime(text.strip(), DATE_FORMAT)
    except ValueError as exc:
        raise ValueError(f"Неверный формат даты: ожидается {DATE_FORMAT}") from exc
