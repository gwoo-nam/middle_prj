import pytest
from app import add, calculate_average, get_first, get_user_name, repeat


# --- 통과 케이스 ---

def test_add():
    assert add(2, 3) == 5


def test_calculate_average_normal():
    assert calculate_average([10, 20, 30]) == 20.0


def test_get_user_name_normal():
    assert get_user_name({"name": "Alice"}) == "Alice"


def test_get_first_normal():
    assert get_first([1, 2, 3]) == 1


def test_repeat_normal():
    assert repeat("hi", 3) == "hihihi"


# --- 실패 케이스 (Do: Claude가 잘 분석하는 명확한 예외) ---

def test_calculate_average_empty():
    # FAILS: ZeroDivisionError - empty list
    result = calculate_average([])
    assert result == 0


def test_get_user_name_missing_key():
    # FAILS: KeyError - "name" key absent
    result = get_user_name({"age": 30})
    assert result == "unknown"


def test_get_first_empty_list():
    # FAILS: IndexError - empty list
    result = get_first([])
    assert result is None


def test_repeat_wrong_type():
    # FAILS: TypeError - times must be int, not str
    result = repeat("hi", "3")
    assert result == "hihihi"
