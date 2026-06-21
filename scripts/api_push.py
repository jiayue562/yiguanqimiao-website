import requests, base64

TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Read local file
file_path = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\.github\workflows\deploy.yml"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Get SHA
resp = requests.get(
    "https://api.github.com/repos/jiayue562/yiguanqimiao-website/contents/.github/workflows/deploy.yml?ref=master",
    headers=HEADERS
)
sha = resp.json()["sha"]
print(f"SHA: {sha}")

# Base64 encode
encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")

# Update file
data = {
    "message": "修复：优化首页展示为文章列表页",
    "content": encoded,
    "sha": sha,
    "branch": "master"
}
resp = requests.put(
    "https://api.github.com/repos/jiayue562/yiguanqimiao-website/contents/.github/workflows/deploy.yml",
    headers=HEADERS,
    json=data
)
print(f"Status: {resp.status_code}")
print(resp.json().get("commit", {}).get("sha", resp.text[:200]))
