# notifications.py
"""
Простая подсистема уведомлений/советов (показывает советы в CLI/GUI).
"""

import random
from typing import List

MOTIVATIONS = [
    "Маленький шаг вперед — уже прогресс!",
    "Дисциплина — это мост между целями и их достижением.",
    "Сделай это сегодня, чтобы завтра было легче.",
    "Лучшее время начать — сейчас."
]


def random_motivation() -> str:
    """Возвращает случайное мотивационное сообщение."""
    return random.choice(MOTIVATIONS)


def needs_attention(habits: List[dict], days_threshold: int = 3) -> List[str]:
    """
    Возвращает список привычек, которые не выполнялись последние days_threshold дней.
    """
    res = []
    from datetime import datetime, timedelta
    for h in habits:
        last = h.get("last_done", "").strip()
        if not last:
            res.append(h["name"])
            continue
        try:
            last_dt = datetime.strptime(last, "%d-%m-%Y")
            if (datetime.now() - last_dt).days >= days_threshold:
                res.append(h["name"])
        except Exception:
            res.append(h["name"])
    return res


def advice_for(hail: str) -> str:
    """
    Возвращает простую советующую строку для привычки (placeholder logic).
    """
    return f"Совет для '{hail}': уменьшите цель на 20% или разбейте задачу на части."
