# 실험 결과 보고서

## 1. 시스템 개요

Jenkins 빌드 실패 시 Claude API가 에러 로그와 소스코드를 분석하여
GitHub PR에 원인 및 수정 제안 코멘트를 자동으로 작성하는 시스템.

```
[GitHub PR] → [Jenkins 빌드] → pytest 실패
                                    ↓
                          analyzer.py 실행
                                    ↓
                         Claude API 분석 요청
                                    ↓
                       GitHub PR 코멘트 자동 작성
```

---

## 2. 실험 환경

| 항목 | 값 |
|---|---|
| Python | 3.13.3 |
| pytest | 9.0.2 |
| Claude 모델 | claude-sonnet-4-5 |
| CI | Jenkins (Docker) |
| 분석 대상 | sample-app/app.py |

---

## 3. 실험 결과

### 3-1. pytest 실행 결과 (로컬 검증)

```
collected 9 items

test_add                        PASSED
test_calculate_average_normal   PASSED
test_get_user_name_normal       PASSED
test_get_first_normal           PASSED
test_repeat_normal              PASSED
test_calculate_average_empty    FAILED  ← ZeroDivisionError
test_get_user_name_missing_key  FAILED  ← KeyError
test_get_first_empty_list       FAILED  ← IndexError
test_repeat_wrong_type          FAILED  ← TypeError

5 passed, 4 failed
```

### 3-2. 시나리오별 Claude 분석 결과

#### Case 1: ZeroDivisionError

- **입력:** `calculate_average([])`
- **에러:** `ZeroDivisionError: division by zero` at `app.py:3`
- **Claude 진단:** 빈 리스트에서 `len(numbers) == 0`이 되어 나눗셈 오류 발생
- **Claude 수정 제안:**
  ```python
  def calculate_average(numbers):
      if not numbers:
          return 0
      return sum(numbers) / len(numbers)
  ```
- **스크린샷:** `docs/screenshots/case1_pr_comment.png` _(Jenkins 실행 후 촬영)_

---

#### Case 2: KeyError

- **입력:** `get_user_name({"age": 30})`
- **에러:** `KeyError: 'name'` at `app.py:12`
- **Claude 진단:** `user` dict에 `"name"` 키가 없을 경우 처리 누락
- **Claude 수정 제안:**
  ```python
  def get_user_name(user):
      return user.get("name", "unknown")
  ```
- **스크린샷:** `docs/screenshots/case2_pr_comment.png` _(Jenkins 실행 후 촬영)_

---

#### Case 3: IndexError

- **입력:** `get_first([])`
- **에러:** `IndexError: list index out of range` at `app.py:17`
- **Claude 진단:** 빈 리스트에 `items[0]` 접근 시 인덱스 범위 초과
- **Claude 수정 제안:**
  ```python
  def get_first(items):
      return items[0] if items else None
  ```
- **스크린샷:** `docs/screenshots/case3_pr_comment.png` _(Jenkins 실행 후 촬영)_

---

#### Case 4: TypeError

- **입력:** `repeat("hi", "3")`
- **에러:** `TypeError: can't multiply sequence by non-int of type 'str'` at `app.py:22`
- **Claude 진단:** `times` 인자가 `str`로 전달되어 `*` 연산자 타입 불일치 발생
- **Claude 수정 제안:**
  ```python
  def repeat(text, times):
      return text * int(times)
  ```
- **스크린샷:** `docs/screenshots/case4_pr_comment.png` _(Jenkins 실행 후 촬영)_

---

### 3-3. Jenkins 빌드 콘솔 스크린샷

| 단계 | 파일 |
|---|---|
| pytest 실패 로그 | `docs/screenshots/jenkins_console_failure.png` |
| analyzer.py 실행 로그 | `docs/screenshots/jenkins_console_analyzer.png` |
| GitHub PR 코멘트 결과 | `docs/screenshots/github_pr_comment.png` |

> 스크린샷은 Jenkins Docker 환경 구동 후 실제 빌드 실행 시 촬영한다.

---

## 4. Do & Don't 최종 정리

### Do — Claude가 효과적으로 분석하는 케이스

| 조건 | 이유 |
|---|---|
| 명확한 예외 타입 (`ZeroDivisionError`, `KeyError` 등) | 에러 종류만으로 원인 범위가 좁혀짐 |
| 스택 트레이스에 파일명 + 라인 번호 포함 | Claude가 소스코드의 정확한 위치를 참조 가능 |
| 동일 입력으로 100% 재현 가능 | 분석 결과를 검증할 수 있음 |
| 단일 함수 내에서 원인이 완결 | 수정 범위가 명확하여 제안 코드가 정확함 |

### Don't — 분석이 어렵거나 부정확해지는 케이스

| 케이스 | 한계 이유 |
|---|---|
| 레이스 컨디션 | 비결정적 — 로그만으로 재현 불가 |
| 네트워크 타임아웃 | 외부 환경 의존 — 소스코드와 무관 |
| 메모리 부족 (OOM) | 런타임 상태 의존 — 코드로 특정 불가 |
| 무한 루프 | 예외 없이 행(hang) — 스택 트레이스 없음 |
| Silent bug (잘못된 결과 반환) | 예외 없음 — 로그에 단서 없음 |

---

## 5. 결론

- **효과적인 범위:** 스택 트레이스가 명확한 런타임 예외. Claude는 파일/라인을 정확히 지목하고 수정 코드를 제시함.
- **한계:** 환경·타이밍 의존적 장애나 silent bug는 로그와 소스코드만으로 분석 불가.
- **실용적 적용:** 전체 빌드 실패의 상당수는 명확한 예외이므로, PR 코멘트 자동화는 리뷰 초기 진단 비용을 줄이는 데 유효함.
