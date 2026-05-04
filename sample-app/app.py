def calculate_average(numbers):
    # BUG: ZeroDivisionError when numbers is empty
    return sum(numbers) / len(numbers)


def add(a, b):
    return a + b


def get_user_name(user):
    # BUG: KeyError when "name" key is missing
    return user["name"]


def get_first(items):
    # BUG: IndexError when items is empty
    return items[0]


def repeat(text, times):
    # BUG: TypeError when times is not an int
    return text * times
