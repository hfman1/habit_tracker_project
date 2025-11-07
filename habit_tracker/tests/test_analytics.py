# tests/test_analytics.py
from analytics import active_habits, average_streak, top_problem_habits

def test_active_and_average():
    sample = [
        {"name": "A", "streak": "2", "progress": "50%"},
        {"name": "B", "streak": "4", "progress": "60%"},
    ]
    assert active_habits(sample) == 2
    assert average_streak(sample) == 3

def test_top_problems():
    sample = [
        {"name": "A", "progress": "10%"},
        {"name": "B", "progress": "80%"},
    ]
    problems = top_problem_habits(sample, threshold=50)
    assert "A" in problems and "B" not in problems
