# tests/test_manager.py
import tempfile
import os
import csv
from habit_manager import HabitManager, HabitError

def make_temp_manager(tmp_path):
    f = tmp_path / "habits.csv"
    return HabitManager(file_path=str(f))

def test_add_and_find(tmp_path):
    mgr = make_temp_manager(tmp_path)
    mgr.add_habit("TestHabit", category="Test", target=5)
    found = mgr.find_habit("TestHabit")
    assert found["name"] == "TestHabit"
    assert found["category"] == "Test"

def test_remove(tmp_path):
    mgr = make_temp_manager(tmp_path)
    mgr.add_habit("ToRemove", category="X", target=3)
    mgr.remove_habit("ToRemove")
    try:
        mgr.find_habit("ToRemove")
        assert False, "Should have raised HabitError"
    except HabitError:
        assert True

def test_mark_done_progress(tmp_path):
    mgr = make_temp_manager(tmp_path)
    mgr.add_habit("P", category="C", target=2)
    mgr.mark_done("P")
    h = mgr.find_habit("P")
    assert h["streak"] in ("1", "1.0") or int(float(h["streak"])) >= 1
    assert "%" in h["progress"]
