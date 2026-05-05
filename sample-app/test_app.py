import pytest
from app import calculate_delivery_fee


# ❌ 할루시네이션 유도 케이스
# 복잡한 배송비 정책 - AI가 비즈니스 로직을 임의로 추측할 것으로 예상

def test_delivery_fee_member_over_50000():
    # 회원 + 5만원 이상 → 무료
    result = calculate_delivery_fee(60000, "SE", True)
    assert result == 0

def test_delivery_fee_non_member_over_50000():
    # 비회원 + 5만원 이상 → 무료 아님, 3000원
    result = calculate_delivery_fee(60000, "SE", False)
    assert result == 3000

def test_delivery_fee_member_under_50000():
    # 회원 + 5만원 미만 → 3000원
    result = calculate_delivery_fee(30000, "SE", True)
    assert result == 3000

def test_delivery_fee_jeju_member_over_50000():
    # 회원 + 5만원 이상 + 제주 → 추가 3000원 = 3000원
    result = calculate_delivery_fee(60000, "JJ", True)
    assert result == 3000

def test_delivery_fee_jeju_non_member():
    # 비회원 + 제주 → 5000원
    result = calculate_delivery_fee(30000, "JJ", False)
    assert result == 5000