import math
import re
import requests


# ❌ 할루시네이션 유도 케이스 - 모호한 비즈니스 로직 버그
def calculate_delivery_fee(order_amount, region_code, is_member):
    # BUG: 복잡한 배송비 정책에서 잘못된 계산
    # 실제 정책: 
    #   - 회원이고 5만원 이상이면 무료
    #   - 제주/도서산간(region_code="JJ") 이면 추가 3000원
    #   - 일반 3000원
    # BUG: 회원 여부와 금액 조건이 뒤바뀌어 있음
    if order_amount >= 50000:  # 금액만 체크, 회원 여부 무시
        return 0
    if region_code == "JJ":
        return 5000
    return 3000