import os
import sys
import requests
import google.generativeai as genai

def main():
    if len(sys.argv) < 3:
        print("Usage: python analyzer.py <pytest_log> <source_file>")
        sys.exit(1)

    pytest_log_path = sys.argv[1]
    source_file_path = sys.argv[2]

    with open(pytest_log_path, "r", encoding="utf-8") as f:
        error_log = f.read()

    with open(source_file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # 1. 제미나이 API 키 및 모델 셋팅
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("에러: GEMINI_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    다음은 Python 테스트 실패 로그와 소스 코드입니다.
    버그의 원인을 분석하고, 수정된 코드를 제안해주세요.

    [에러 로그]
    {error_log}

    [소스 코드]
    {source_code}
    """

    # 2. 제미나이 분석 요청
    try:
        print("Gemini API로 분석을 요청합니다...")
        response = model.generate_content(prompt)
        analysis_result = response.text
        print("분석 완료!")
    except Exception as e:
        print(f"Gemini API 호출 중 에러 발생: {e}")
        sys.exit(1)

    # 3. GitHub PR에 코멘트 달기
    change_id = os.environ.get("CHANGE_ID")
    repo = os.environ.get("GITHUB_REPO")
    token = os.environ.get("GITHUB_TOKEN")

    if not change_id:
        print("CHANGE_ID가 없습니다. (일반 브랜치 빌드이므로 PR 코멘트는 생략합니다)")
        print("\n=== AI 분석 결과 ===\n", analysis_result)
        return

    if not repo or not token:
        print("GITHUB_REPO 또는 GITHUB_TOKEN이 없어서 코멘트를 작성할 수 없습니다.")
        return

    print("GitHub PR에 코멘트를 작성합니다...")
    url = f"https://api.github.com/repos/{repo}/issues/{change_id}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "body": f"### 🤖 Gemini AI 코드 리뷰\n\n{analysis_result}"
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 201:
        print("PR 코멘트 작성 성공!")
    else:
        print(f"코멘트 작성 실패: {res.status_code} - {res.text}")

if __name__ == "__main__":
    main()