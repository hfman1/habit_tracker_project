# habit_manager.py
"""
Класс HabitManager — CRUD и работа с CSV.
Документация Google-style для методов.
"""

import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict

from habit_entry import parse_date, validate_name, validate_category, DATE_FORMAT

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DEFAULT_FILE = os.path.join(DATA_DIR, "habits.csv")


class HabitError(Exception):
    """Базовое исключение для менеджера привычек."""
    pass


class HabitManager:
    """Менеджер привычек: загрузка, сохранение, добавление, отметка, поиск."""

    FIELDNAMES = ["name", "category", "frequency", "start_date",
                  "last_done", "streak", "target", "progress"]

    def __init__(self, file_path: str = DEFAULT_FILE):
        """Инициализация менеджера — загружает данные или создаёт файл."""
        self.file_path = file_path
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            # создаём CSV с заголовком
            with open(self.file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
        self.habits = self._load_habits()

    def _load_habits(self) -> List[Dict[str, str]]:
        """Загружает все привычки из CSV в список словарей."""
        try:
            with open(self.file_path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as exc:
            raise HabitError(f"Ошибка загрузки данных: {exc}") from exc

    def _save_habits(self) -> None:
        """Сохраняет self.habits в CSV."""
        try:
            with open(self.file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.FIELDNAMES)
                writer.writeheader()
                writer.writerows(self.habits)
        except Exception as exc:
            raise HabitError(f"Ошибка сохранения данных: {exc}") from exc

    def add_habit(self, name: str, category: str = "Общее", frequency: str = "daily", target: int = 30) -> None:
        """
        Добавляет новую привычку.

        Raises:
            HabitError: если имя некорректно или привычка уже существует.
        """
        if not validate_name(name):
            raise HabitError("Неверное имя привычки.")
        if not validate_category(category):
            raise HabitError("Неверная категория.")
        if any(h["name"].strip().lower() == name.strip().lower() for h in self.habits):
            raise HabitError("Привычка с таким именем уже существует.")
        now = datetime.now().strftime(DATE_FORMAT)
        entry = {
            "name": name.strip(),
            "category": category.strip(),
            "frequency": frequency,
            "start_date": now,
            "last_done": "",
            "streak": "0",
            "target": str(int(target)),
            "progress": "0%"
        }
        self.habits.append(entry)
        self._save_habits()

    def remove_habit(self, name: str) -> None:
        """Удаляет привычку по имени. Если нет — бросает исключение."""
        before = len(self.habits)
        self.habits = [h for h in self.habits if h["name"].strip().lower() != name.strip().lower()]
        if len(self.habits) == before:
            raise HabitError("Привычка не найдена.")
        self._save_habits()

    def list_habits(self) -> List[Dict[str, str]]:
        """Возвращает список всех привычек."""
        return self.habits

    def find_habit(self, name: str) -> Dict[str, str]:
        """Ищет привычку по имени, возвращает словарь или бросает HabitError."""
        for h in self.habits:
            if h["name"].strip().lower() == name.strip().lower():
                return h
        raise HabitError("Привычка не найдена.")

    def mark_done(self, name: str, date_text: str = "") -> None:
        """
        Отметить выполнение привычки на дату date_text (если пусто — сегодня).
        Обновляет last_done, streak и progress.
        """
        d = parse_date(date_text).strftime(DATE_FORMAT)
        habit = self.find_habit(name)
        last_done = habit.get("last_done", "").strip()
        if last_done:
            try:
                last_dt = datetime.strptime(last_done, DATE_FORMAT)
                curr_dt = datetime.strptime(d, DATE_FORMAT)
                delta = (curr_dt - last_dt).days
                if delta == 0:
                    # Уже отмечено за этот день — ничего не делаем
                    return
                elif delta == 1:
                    habit["streak"] = str(int(habit.get("streak", "0")) + 1)
                elif delta > 1:
                    habit["streak"] = "1"
                else:
                    # дата раньше — игнорируем или считаем как отдельная отметка
                    habit["streak"] = str(int(habit.get("streak", "0")) + 1)
            except ValueError:
                habit["streak"] = "1"
        else:
            habit["streak"] = "1"
        habit["last_done"] = d
        try:
            progress = int(habit["streak"]) / max(1, int(habit.get("target", "30"))) * 100
        except Exception:
            progress = 0.0
        habit["progress"] = f"{progress:.1f}%"
        self._save_habits()
