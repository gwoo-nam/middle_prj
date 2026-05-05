import pytest
from app import (
    calculate_discount, format_phone_number, get_user_age,
    divide, get_first_initial,
    read_user_config, send_notification, process_large_dataset
)


# ✅ 성공 예상 케이스 1 - 할인율 유효성 검사 누락
# 할인율이 1 초과일 때 음수 가격이 반환되는 버그
def test_calculate_discount_over_100_percent():
    result = calculate_discount(10000, 1.5)  # 150% 할인 → 음수 반환
    assert result >= 0  # 가격은 0 이상이어야 함


# ✅ 성공 예상 케이스 2 - 전화번호 포맷 처리
# 전화번호에 특수문자 포함 시 처리 실패
def test_format_phone_number_with_special_chars():
    result = format_phone_number("(010)1234-5678")
    assert result == "010-1234-5678"


# ✅ 성공 예상 케이스 3 - 딕셔너리 키 없음
# user 딕셔너리에 age 키가 없을 때 KeyError 발생
def test_get_user_age_missing_key():
    result = get_user_age({"name": "Alice"})
    assert result == 0  # 기본값 0 반환


# ✅ 성공 예상 케이스 4 - 0으로 나누기
# b가 0일 때 ZeroDivisionError 발생
def test_divide_by_zero():
    result = divide(10, 0)
    assert result == 0  # 0으로 나눌 때 0 반환


# ✅ 성공 예상 케이스 5 - 빈 문자열 인덱스 접근
# 빈 문자열에서 첫 글자를 가져올 때 IndexError 발생
def test_get_first_initial_empty():
    result = get_first_initial("")
    assert result == ""  # 빈 문자열 반환


# ❌ 실패 예상 케이스 1 - 설정 파일 없음 (배포 환경 문제)
# /etc/myapp/config.json이 없는 환경에서 FileNotFoundError 발생
# AI가 코드 문제로 오판하여 엉뚱한 수정 시도 예상
def test_read_user_config():
    result = read_user_config()
    assert result is not None


# ❌ 실패 예상 케이스 2 - 내부 메일 서버 연결 불가 (네트워크 문제)
# 내부 메일 서버가 없는 환경에서 ConnectionError 발생
# AI가 네트워크 문제를 코드 수정으로 해결하려는 시도 예상
def test_send_notification():
    result = send_notification("test@example.com", "테스트 메시지")
    assert result is True


# ❌ 실패 예상 케이스 3 - 무한루프 (타임아웃)
# 대용량 데이터 처리 중 인덱스 버그로 무한루프 발생
# 3초 타임아웃으로 강제 종료, AI가 원인 파악 어려움
@pytest.mark.timeout(3)
def test_process_large_dataset():
    result = process_large_dataset([1, 2, 3, 4, 5])
    assert result == [5, 4, 3, 2, 1]