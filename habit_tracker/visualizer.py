# visualizer.py
"""
Визуализация привычек с помощью matplotlib.
Содержит функции для построения графиков, возвращающих объект Figure.
"""

import os
from typing import List, Dict
from datetime import datetime, timedelta

import matplotlib
# Не навязываем GUI backend — он выберется автоматически при встраивании
from matplotlib.figure import Figure

from habit_manager import HabitManager, DATE_FORMAT


def plot_progress_single(habit: Dict[str, str]) -> Figure:
    """
    Возвращает matplotlib Figure с простым графиком прогресса в % (по streak/target).
    Для упрощения используем текущий прогресс как точку.
    """
    fig = Figure(figsize=(5, 3), dpi=100)
    ax = fig.add_subplot(111)
    try:
        progress = float(habit.get("progress", "0%").strip().strip("%"))
    except Exception:
        progress = 0.0
    ax.bar([habit["name"]], [progress])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Progress (%)")
    ax.set_title(f"Progress: {habit['name']}")
    return fig


def plot_category_distribution(habits: List[Dict[str, str]]) -> Figure:
    """Круговая диаграмма распределения привычек по категориям."""
    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot(111)
    categories = {}
    for h in habits:
        cat = h.get("category", "Общее") or "Общее"
        categories[cat] = categories.get(cat, 0) + 1
    if not categories:
        ax.text(0.5, 0.5, "Нет данных", ha="center")
        return fig
    labels = list(categories.keys())
    sizes = list(categories.values())
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Categories distribution")
    return fig


def save_figure(fig: Figure, filename: str) -> str:
    """Сохраняет Figure в файл PNG и возвращает путь."""
    out_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)
    fig.savefig(out_path)
    return out_path
