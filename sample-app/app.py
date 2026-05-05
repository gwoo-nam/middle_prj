def calculate_average(numbers):
    # BUG: ZeroDivisionError when numbers is empty
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
 
 
def add(a, b):
    return a + b
 
 
def get_user_name(user):
    # BUG: KeyError when "name" key is missing
    return user.get("name", None)
 
 
def get_first(items):
    # BUG: IndexError when items is empty
    if not items:
        return None
    return items[0]
 
 
def repeat(text, times):
    # BUG: TypeError when times is not an int
    try:
        actual_times = int(times)
    except (ValueError, TypeError):
        raise TypeError("times must be an integer or a string convertible to an integer")
    return text * actual_times
 
 
# ✅ 성공 예상 케이스 1 - NoneType 오류
def get_length(text):
    # BUG: TypeError when text is None
    return len(text)
 
 
# ✅ 성공 예상 케이스 2 - 음수 입력 처리 누락
import math
def get_sqrt(n):
    # BUG: ValueError when n is negative
    return math.sqrt(n)
 
 
# ✅ 성공 예상 케이스 3 - 딕셔너리 중첩 KeyError
def get_city(data):
    # BUG: KeyError when "address" or "city" key is missing
    return data["address"]["city"]