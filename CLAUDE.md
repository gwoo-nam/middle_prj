# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

# 프로젝트: Jenkins-Claude 자동 분석 시스템

## 목적
Jenkins 빌드 실패 시 Claude API가 에러 로그와 소스코드를 분석하여
GitHub PR에 원인 및 수정 제안 코멘트를 자동으로 작성한다.

## 기술 스택
- CI/CD: Jenkins (Pipeline)
- 언어: Python 3.11
- AI: Claude API (claude-sonnet-4-20250514)
- 저장소: GitHub
- 환경: Docker (Jenkins 컨테이너)

## 디렉토리 구조
jenkins-claude/
├── CLAUDE.md              ← 이 파일
├── sample-app/            ← 빌드 대상 샘플 프로젝트
│   ├── app.py
│   └── test_app.py
├── claude-analyzer/       ← Claude 분석 스크립트
│   ├── analyzer.py
│   ├── github_client.py
│   └── requirements.txt
├── jenkins/
│   ├── Jenkinsfile
│   └── Dockerfile
└── docs/
    ├── 01_setup.md
    ├── 02_test_scenarios.md  ← Do & Don't 케이스
    └── 03_results.md

## 작업 규칙 (Claude에게 지시할 때)
- 한 번에 하나의 파일/기능만 요청한다
- 각 단계 완료 후 동작 확인 후 다음으로 넘어간다
- 실패 케이스도 의도적으로 테스트한다
- 코드 변경 시 이유를 반드시 설명하도록 요청한다

## 현재 진행 단계
- [x] Step 1: 샘플 앱 + 실패 테스트 작성
- [x] Step 2: Jenkins Docker 환경 구성
- [x] Step 3: Jenkinsfile 작성
- [x] Step 4: Claude 분석 스크립트 작성
- [x] Step 5: GitHub PR 코멘트 연동
- [x] Step 6: 실패 케이스 실험 (Do & Don't)
- [x] Step 7: 발표 자료 정리