# tests/test_entry.py
import tempfile
import os
from habit_entry import validate_name, parse_date, validate_category
from datetime import datetime

def test_validate_name_ok():
    assert validate_name("Чтение")
    assert validate_name("Run-5")
    assert validate_name("habit_1")

def test_validate_name_bad():
    assert not validate_name("")
    assert not validate_name(" " * 5)
    assert not validate_name("a"*101)

def test_parse_date_defaults_to_today():
    d = parse_date("")
    assert isinstance(d, datetime)

def test_validate_category():
    assert validate_category("Здоровье")
    assert validate_category(None)
