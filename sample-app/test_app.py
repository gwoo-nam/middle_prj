import pytest
from app import add, calculate_average, get_first, get_user_name, repeat
from app import get_length, get_sqrt, get_city, read_config


# --- 기존 통과 케이스 ---

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


# --- 기존 실패 케이스 ---

def test_calculate_average_empty():
    result = calculate_average([])
    assert result == 0

def test_get_user_name_missing_key():
    result = get_user_name({"age": 30})
    assert result == "unknown"

def test_get_first_empty_list():
    result = get_first([])
    assert result is None

def test_repeat_wrong_type():
    result = repeat("hi", "3")
    assert result == "hihihi"


# ✅ 성공 예상 케이스 1 - NoneType 오류
# AI가 None 체크 추가로 정확히 수정할 것으로 예상
def test_get_length_none():
    result = get_length(None)
    assert result == 0


# ✅ 성공 예상 케이스 2 - 음수 입력 ValueError
# AI가 음수 체크 조건문 추가로 정확히 수정할 것으로 예상
def test_get_sqrt_negative():
    result = get_sqrt(-4)
    assert result == 0


# ✅ 성공 예상 케이스 3 - 중첩 딕셔너리 KeyError
# AI가 .get() 체이닝으로 정확히 수정할 것으로 예상
def test_get_city_missing():
    result = get_city({"name": "Alice"})
    assert result == "unknown"

