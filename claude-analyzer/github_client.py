import os
import requests


def post_comment(pr_number, comment):
    token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPO"]  # e.g. "owner/repo"

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    response = requests.post(url, json={"body": comment}, headers=headers)
    response.raise_for_status()
    return response.json()["html_url"]
