# Test Scenarios: Do & Don't

Claude 분석 시스템이 잘 동작하는 케이스와 한계가 있는 케이스를 정리한다.

---

## Do: Claude가 잘 분석하는 케이스

스택 트레이스가 명확하고 재현 가능한 예외들.

| 시나리오 | 함수 | 예외 | 원인 |
|---|---|---|---|
| 빈 리스트 평균 | `calculate_average([])` | `ZeroDivisionError` | `len([]) == 0` |
| 누락된 딕셔너리 키 | `get_user_name({"age": 30})` | `KeyError: 'name'` | 키 존재 여부 미확인 |
| 빈 리스트 인덱스 | `get_first([])` | `IndexError` | 빈 컨테이너 경계 미처리 |
| 잘못된 타입 | `repeat("hi", "3")` | `TypeError` | int 대신 str 전달 |

**공통 특성:**
- 스택 트레이스에 파일명 + 라인 번호가 명시됨
- 동일 입력으로 100% 재현 가능
- 원인과 수정 방법이 코드 한 줄 수준으로 특정됨

---

## Don't: Claude 분석이 어려운 케이스

| 시나리오 | 이유 |
|---|---|
| 레이스 컨디션 | 비결정적 — 로그만으로 재현 불가 |
| 네트워크 타임아웃 | 외부 환경 의존 — 소스코드와 무관 |
| 메모리 부족 (OOM) | 런타임 상태에 의존 — 코드 분석으로 특정 불가 |
| 무한 루프 (행) | 예외 없이 종료 안 됨 — 스택 트레이스 없음 |
| 데이터 오염 (silent bug) | 예외 없이 잘못된 결과 반환 — 로그에 단서 없음 |

**공통 특성:**
- 스택 트레이스가 없거나 무의미함
- 실행 환경 / 타이밍 / 외부 시스템에 의존
- 로그와 소스코드만으로 원인 특정 불가

---

## 실험 결과 요약

```
pytest 결과 (sample-app/test_app.py)

통과 (5): test_add, test_calculate_average_normal,
          test_get_user_name_normal, test_get_first_normal, test_repeat_normal

실패 (4): test_calculate_average_empty   → ZeroDivisionError
          test_get_user_name_missing_key → KeyError
          test_get_first_empty_list      → IndexError
          test_repeat_wrong_type         → TypeError
```

4가지 Do 케이스 모두 스택 트레이스가 명확하여 Claude가 원인 파일/라인을 정확히 지목할 수 있음.
