# main.py
"""
Точка запуска проекта. Поддерживает CLI-параметр --nogui для работы в консоли.
"""

import argparse
import sys

from habit_manager import HabitManager
from notifications import random_motivation
from gui import HabitTrackerApp


def run_cli():
    """Простой CLI: печатает сводку и мотивацию."""
    manager = HabitManager()
    habits = manager.list_habits()
    print("Habit Tracker Pro — CLI режим")
    print(f"Всего привычек: {len(habits)}")
    for h in habits:
        print(f"- {h['name']} | streak: {h.get('streak','0')} | progress: {h.get('progress','0%')}")
    print("\n" + random_motivation())


def main(argv=None):
    parser = argparse.ArgumentParser(description="Habit Tracker Pro")
    parser.add_argument("--nogui", action="store_true", help="Запуск без GUI (CLI summary).")
    args = parser.parse_args(argv)
    if args.nogui:
        run_cli()
    else:
        # Запуск GUI
        app = HabitTrackerApp(manager=HabitManager())
        app.mainloop()


if __name__ == "__main__":
    main()
