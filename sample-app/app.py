def calculate_average(numbers):
    # BUG: ZeroDivisionError when numbers is empty
    if not numbers:  # numbers 리스트가 비어 있는지 확인
        return 0     # 비어 있으면 평균을 0으로 반환 (또는 ValueError를 발생시킬 수도 있음)
    return sum(numbers) / len(numbers)


def add(a, b):
    return a + b

def get_user_name(user):
    # BUG: KeyError when "name" key is missing
    # .get() 메서드를 사용하여 키가 없을 때 None을 반환하도록 수정
    return user.get("name", "unknown")


def get_first(items):
    # BUG: IndexError when items is empty
    if not items:  # items 리스트가 비어 있는지 확인
        return None  # 비어 있으면 None을 반환
    return items[0]

#dd
def repeat(text, times):
    # BUG: TypeError when times is not an int
    try:
        # times를 정수로 변환 시도.
        actual_times = int(times)
    except (ValueError, TypeError):
        # 정수나 정수 형태의 문자열이 아닌 경우 TypeError를 발생시킨다.
        raise TypeError("times must be an integer or a string convertible to an integer")
    return text * actual_times
