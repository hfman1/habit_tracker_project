# gui.py
"""
GUI приложение Habit Tracker на CustomTkinter.
Весь GUI изолирован в классе HabitTrackerApp.
"""

import os
import threading
import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from habit_manager import HabitManager, HabitError
from visualizer import plot_progress_single, plot_category_distribution
from notifications import random_motivation, needs_attention


ctk.set_appearance_mode("System")  # "Dark" / "Light" / "System"
ctk.set_default_color_theme("blue")


class HabitTrackerApp(ctk.CTk):
    """Главный GUI-класс приложения."""

    def __init__(self, manager: HabitManager = None):
        super().__init__()
        self.title("Habit Tracker Pro")
        self.geometry("900x650")
        self.manager = manager or HabitManager()
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        """Создаёт виджеты."""
        # Заголовок
        header = ctk.CTkLabel(self, text="Habit Tracker Pro", font=ctk.CTkFont(size=24, weight="bold"))
        header.pack(pady=(12, 6))

        # Верхняя рамка — ввод
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=12, pady=6)

        self.name_entry = ctk.CTkEntry(top_frame, placeholder_text="Название привычки")
        self.name_entry.grid(row=0, column=0, padx=6, pady=6)
        self.category_entry = ctk.CTkEntry(top_frame, placeholder_text="Категория (Здоровье/Работа/Другое)")
        self.category_entry.grid(row=0, column=1, padx=6, pady=6)
        self.target_entry = ctk.CTkEntry(top_frame, placeholder_text="Цель в днях (например, 30)")
        self.target_entry.grid(row=0, column=2, padx=6, pady=6)

        add_btn = ctk.CTkButton(top_frame, text="Добавить", command=self._on_add)
        add_btn.grid(row=0, column=3, padx=6)

        remove_btn = ctk.CTkButton(top_frame, text="Удалить", fg_color="tomato", hover_color="#ff7b7b", command=self._on_remove)
        remove_btn.grid(row=0, column=4, padx=6)

        # Слева — список привычек, справа — график/инфо
        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=12, pady=6)

        left = ctk.CTkFrame(body, width=300)
        left.pack(side="left", fill="y", padx=(0, 6), pady=6)

        self.habit_list = ctk.CTkTextbox(left, width=300, height=400, state="disabled")
        self.habit_list.pack(padx=6, pady=6)

        mark_btn = ctk.CTkButton(left, text="Отметить выполнено", command=self._on_mark_done)
        mark_btn.pack(pady=6)

        stats_btn = ctk.CTkButton(left, text="Показать категорийный график", command=self._show_category_chart)
        stats_btn.pack(pady=6)

        right = ctk.CTkFrame(body)
        right.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)

        self.canvas_container = ctk.CTkFrame(right)
        self.canvas_container.pack(fill="both", expand=True, padx=6, pady=6)

        # Нижняя строка — мотивация
        bottom = ctk.CTkFrame(self)
        bottom.pack(fill="x", padx=12, pady=(6, 12))

        self.motivation_label = ctk.CTkLabel(bottom, text=random_motivation())
        self.motivation_label.pack(side="left", padx=6)

        refresh_btn = ctk.CTkButton(bottom, text="Обновить", command=self._refresh_list)
        refresh_btn.pack(side="right", padx=6)

        check_btn = ctk.CTkButton(bottom, text="Проверить пропуски", command=self._show_attention)
        check_btn.pack(side="right", padx=6)

    def _on_add(self):
        """Обработчик добавления привычки."""
        name = self.name_entry.get().strip()
        cat = self.category_entry.get().strip() or "Общее"
        target_text = self.target_entry.get().strip() or "30"
        try:
            target = int(target_text)
        except Exception:
            messagebox.showerror("Ошибка", "Цель должна быть целым числом.")
            return
        try:
            self.manager.add_habit(name=name, category=cat, target=target)
            messagebox.showinfo("OK", f"Привычка '{name}' добавлена.")
            self._refresh_list()
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_remove(self):
        """Удалить выбранную привычку (берём из name_entry)."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите имя привычки для удаления.")
            return
        try:
            self.manager.remove_habit(name)
            messagebox.showinfo("OK", f"Привычка '{name}' удалена.")
            self._refresh_list()
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _on_mark_done(self):
        """Отметить выбранную привычку выполненной."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите имя привычки для отметки.")
            return
        try:
            self.manager.mark_done(name)
            messagebox.showinfo("OK", f"Привычка '{name}' отмечена выполненной.")
            self._refresh_list()
            # показ графика в отдельном потоке, чтобы GUI не блокировался
            threading.Thread(target=self._show_single_chart, args=(name,), daemon=True).start()
        except Exception as exc:
            messagebox.showerror("Ошибка", str(exc))

    def _refresh_list(self):
        """Обновляет текстовое поле со списком привычек."""
        habits = self.manager.list_habits()
        text = ""
        for h in habits:
            text += f"{h['name']} [{h.get('category','')}] — streak: {h.get('streak','0')} — progress: {h.get('progress','0%')}\n"
        self.habit_list.configure(state="normal")
        self.habit_list.delete("0.0", "end")
        self.habit_list.insert("0.0", text or "Нет привычек. Добавьте первую!")
        self.habit_list.configure(state="disabled")

    def _clear_canvas(self):
        """Удаляет все вложенные виджеты в контейнере canvas."""
        for w in self.canvas_container.winfo_children():
            w.destroy()

    def _show_single_chart(self, habit_name: str):
        """Показывает график для одной привычки."""
        try:
            habit = self.manager.find_habit(habit_name)
            fig = plot_progress_single(habit)
            self._clear_canvas()
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Невозможно отобразить график: {exc}")

    def _show_category_chart(self):
        """Показывает круговую диаграмму категорий."""
        try:
            fig = plot_category_distribution(self.manager.list_habits())
            self._clear_canvas()
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
        except Exception as exc:
            messagebox.showerror("Ошибка", f"Невозможно отобразить график: {exc}")

    def _show_attention(self):
        """Показывает список привычек, требующих внимания."""
        problems = needs_attention(self.manager.list_habits(), days_threshold=3)
        if not problems:
            messagebox.showinfo("Всё в порядке", "Нет привычек, требующих внимания.")
        else:
            messagebox.showwarning("Внимание", "Не выполнялись: " + ", ".join(problems))
