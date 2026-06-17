#!/usr/bin/env python3
"""
IMA知识库增量同步脚本 - WorkBuddy日常备份
同步今日工作日志到IMA笔记，并添加到知识库
"""
import json
import urllib.request
import urllib.error
import sys
import os
from datetime import datetime

# 凭证
IMA_CLIENT_ID = open(os.path.expanduser("~/.config/ima/client_id")).read().strip()
IMA_API_KEY = open(os.path.expanduser("~/.config/ima/api_key")).read().strip()
BASE_URL = "https://ima.qq.com"

# 知识库ID
KB_ID = "DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY="

def ima_api(path, data):
    """发送IMA API请求"""
    url = f"{BASE_URL}/{path}"
    headers = {
        "ima-openapi-clientid": IMA_CLIENT_ID,
        "ima-openapi-apikey": IMA_API_KEY,
        "Content-Type": "application/json; charset=utf-8"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else str(e)
        return {"retcode": -1, "errmsg": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"retcode": -1, "errmsg": str(e)}

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    memory_path = rf"C:\Users\jia'yue\WorkBuddy\Claw\.workbuddy\memory\{today}.md"

    if not os.path.exists(memory_path):
        print(f"❌ 今日工作日志不存在: {memory_path}")
        sys.exit(1)

    with open(memory_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 验证UTF-8
    try:
        content.encode("utf-8").decode("utf-8")
    except:
        print("❌ 内容不是有效UTF-8")
        sys.exit(1)

    print(f"✅ 读取今日日志: {len(content)} 字节")

    # 1. 创建笔记
    print("📝 创建IMA笔记...")
    note_result = ima_api("openapi/note/v1/import_doc", {
        "content_format": 1,
        "content": content
    })

    if note_result.get("retcode", note_result.get("code", -1)) != 0:
        print(f"❌ 创建笔记失败: {note_result}")
        sys.exit(1)

    doc_id = note_result.get("data", {}).get("note_id") or note_result.get("data", {}).get("doc_id")
    if not doc_id:
        print(f"❌ 未返回doc_id: {note_result}")
        sys.exit(1)

    print(f"✅ 笔记创建成功: doc_id={doc_id}")

    # 2. 添加笔记到知识库
    print("📚 添加到知识库...")
    kb_result = ima_api("openapi/wiki/v1/add_knowledge", {
        "media_type": 11,
        "note_info": {"content_id": doc_id},
        "title": f"{today} WorkBuddy工作日志",
        "knowledge_base_id": KB_ID
    })

    if kb_result.get("retcode", kb_result.get("code", -1)) != 0:
        print(f"❌ 添加到知识库失败: {kb_result}")
        print(f"⚠️  笔记已创建但添加到知识库失败，doc_id={doc_id}")
        sys.exit(1)

    print(f"✅ 已添加到知识库「以观其妙书院」")
    print(f"📋 doc_id={doc_id}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
