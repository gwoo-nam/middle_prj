import argparse
import os
import anthropic
from github_client import post_comment


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def analyze(log_path, source_path):
    log = load_file(log_path)
    source = load_file(source_path)

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY from env

    prompt = f"""다음은 CI 빌드에서 발생한 pytest 실패 로그와 소스코드입니다.
버그의 원인을 분석하고 수정 방법을 제안해주세요.

## pytest 실패 로그
```
{log}
```

## 소스코드 ({source_path})
```python
{source}
```

다음 형식으로 작성해주세요:
1. 버그 원인
2. 수정 제안 (코드 포함)
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    analysis = message.content[0].text
    print(analysis)

    pr_number = os.environ.get("CHANGE_ID")
    if pr_number:
        url = post_comment(pr_number, analysis)
        print(f"PR 코멘트 작성 완료: {url}")
    else:
        print("[CHANGE_ID 없음] GitHub 코멘트 생략 (로컬 실행)")


def main():
    parser = argparse.ArgumentParser(description="Claude로 빌드 실패 로그 분석")
    parser.add_argument("log", help="pytest 에러 로그 파일 경로")
    parser.add_argument("source", help="분석할 소스코드 파일 경로")
    args = parser.parse_args()

    analyze(args.log, args.source)


if __name__ == "__main__":
    main()
