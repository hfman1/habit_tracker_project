# analytics.py
"""
Функции для аналитики привычек: вычисление средних, выявление проблем и советы.
"""

from typing import List, Dict
from statistics import mean

from habit_manager import HabitManager


def active_habits(habits: List[Dict[str, str]]) -> int:
    """Количество активных привычек."""
    return len(habits)


def average_streak(habits: List[Dict[str, str]]) -> float:
    """Средняя длина streak по всем привычкам."""
    streaks = []
    for h in habits:
        try:
            streaks.append(int(h.get("streak", "0")))
        except Exception:
            continue
    return mean(streaks) if streaks else 0.0


def top_problem_habits(habits: List[Dict[str, str]], threshold: float = 50.0) -> List[str]:
    """
    Возвращает список привычек, у которых прогресс ниже threshold процентов.
    """
    problems = []
    for h in habits:
        try:
            p = float(h.get("progress", "0%").strip().strip("%"))
            if p < threshold:
                problems.append(h["name"])
        except Exception:
            continue
    return problems


def summary(manager: HabitManager) -> Dict[str, object]:
    """
    Возвращает словарь с основными метриками (число привычек, avg streak, проблемные).
    """
    habits = manager.list_habits()
    return {
        "total": active_habits(habits),
        "avg_streak": average_streak(habits),
        "problems": top_problem_habits(habits)
    }
