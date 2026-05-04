import os
import sys
import requests

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

    # 1. 제미나이 API 키 셋팅 (공백 완벽 제거)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("에러: GEMINI_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    prompt = f"""
    다음은 Python 테스트 실패 로그와 소스 코드입니다.
    버그의 원인을 분석하고, 수정된 코드를 제안해주세요.

    [에러 로그]
    {error_log}

    [소스 코드]
    {source_code}
    """

    # 2. 제미나이 REST API 직접 호출 (구버전 패키지 충돌 우회)
    print("Gemini API(REST)로 분석을 요청합니다...")
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    gemini_headers = {'Content-Type': 'application/json'}
    gemini_data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        res = requests.post(gemini_url, headers=gemini_headers, json=gemini_data)
        res.raise_for_status() # 에러 발생 시 바로 예외 처리로 던짐
        response_json = res.json()
        analysis_result = response_json['candidates'][0]['content']['parts'][0]['text']
        print("분석 완료!")
    except Exception as e:
        print(f"Gemini API 호출 중 에러 발생: {e}")
        if 'res' in locals():
            print(f"상세 에러 내용: {res.text}")
        sys.exit(1)

    # 3. GitHub PR에 코멘트 달기
    change_id = os.environ.get("CHANGE_ID")
    repo = os.environ.get("GITHUB_REPO")
    token = os.environ.get("GITHUB_TOKEN", "").strip()

    if not change_id:
        print("CHANGE_ID가 없습니다. (일반 브랜치 빌드이므로 PR 코멘트는 생략합니다)")
        print("\n=== AI 분석 결과 ===\n", analysis_result)
        return

    if not repo or not token:
        print("GITHUB_REPO 또는 GITHUB_TOKEN이 없어서 코멘트를 작성할 수 없습니다.")
        return

    print("GitHub PR에 코멘트를 작성합니다...")
    github_url = f"https://api.github.com/repos/{repo}/issues/{change_id}/comments"
    github_headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    github_data = {
        "body": f"### 🤖 Gemini AI 코드 리뷰\n\n{analysis_result}"
    }

    gh_res = requests.post(github_url, headers=github_headers, json=github_data)
    if gh_res.status_code == 201:
        print("PR 코멘트 작성 성공! GitHub을 확인해보세요.")
    else:
        print(f"코멘트 작성 실패: {gh_res.status_code} - {gh_res.text}")

if __name__ == "__main__":
    main()