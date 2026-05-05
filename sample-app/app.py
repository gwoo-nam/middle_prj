import math
import re
import requests


# ✅ 성공 예상 케이스들 - 명확한 코드 버그

def calculate_discount(price, discount_rate):
    # BUG: 할인율이 0~1 범위인지 검증 없음
    return price * (1 - discount_rate)


def format_phone_number(phone):
    # BUG: 숫자 외 문자 포함 시 처리 없음
    digits = phone.replace("-", "").replace(" ", "")
    return f"{digits[:3]}-{digits[3:7]}-{digits[7:]}"


def get_user_age(user):
    # BUG: KeyError when "age" key is missing
    return user["age"]


def divide(a, b):
    # BUG: ZeroDivisionError when b is 0
    return a / b


def get_first_initial(name):
    # BUG: IndexError when name is empty string
    return name[0].upper()


# ❌ 실패 예상 케이스들 - 환경/외부 의존성 문제

def read_user_config():
    # BUG: FileNotFoundError - 설정 파일이 배포 환경에 없음
    with open("/etc/myapp/config.json") as f:
        return f.read()


def send_notification(user_email, message):
    # BUG: 외부 메일 서버 연결 실패
    res = requests.post(
        "http://internal-mail-server.local/api/send",
        json={"to": user_email, "body": message}
    )
    return res.status_code == 200


def process_large_dataset(data):
    # BUG: 무한루프 - 인덱스가 줄지 않음
    result = []
    i = len(data)
    while i > 0:
        result.append(data[i - 1])
        i += 1  # BUG: i를 감소시켜야 함
    return result