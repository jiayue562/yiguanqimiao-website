# -*- coding: utf-8 -*-
# IMA 知识库功能测试脚本
# 龙心 OS · 2026-04-16

import os
import sys
import requests
from pathlib import Path

# 设置控制台编码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# 加载凭证
def load_credentials():
    """加载 IMA 凭证"""
    config_dir = Path.home() / ".config" / "ima"
    
    client_id = os.getenv("IMA_OPENAPI_CLIENTID")
    api_key = os.getenv("IMA_OPENAPI_APIKEY")
    
    # 从文件加载（如果环境变量未设置）
    if not client_id and (config_dir / "client_id").exists():
        with open(config_dir / "client_id", "r", encoding="utf-8-sig") as f:
            client_id = f.read().strip()
    
    if not api_key and (config_dir / "api_key").exists():
        with open(config_dir / "api_key", "r", encoding="utf-8-sig") as f:
            api_key = f.read().strip()
    
    return client_id, api_key

# API 调用辅助函数
def ima_api(path, body=None):
    """调用 IMA API"""
    client_id, api_key = load_credentials()
    
    if not client_id or not api_key:
        print("ERROR: 缺少 IMA 凭证，请按 Setup 步骤配置 Client ID 和 API Key")
        return None
    
    url = f"https://ima.qq.com/{path}"
    headers = {
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=body or {}, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"ERROR: API 调用失败：{e}")
        return None

# 测试功能
def test_get_knowledge_bases():
    """测试 1: 获取知识库列表"""
    print("=" * 60)
    print("  测试 1: 获取知识库列表")
    print("=" * 60)
    print("")
    
    result = ima_api("openapi/wiki/v1/search_knowledge_base", {
        "query": "",
        "cursor": "",
        "limit": 10
    })
    
    if result and result.get("code") == 20000:
        data = result.get("data", {})
        wiki_list = data.get("wiki_list", [])
        
        print("SUCCESS: API 调用成功")
        print(f"  知识库数量：{len(wiki_list)}")
        print("")
        
        if wiki_list:
            print("知识库列表:")
            for i, wiki in enumerate(wiki_list[:5], 1):
                print(f"  {i}. {wiki.get('name', '未命名')} (ID: {wiki.get('id', 'N/A')})")
            if len(wiki_list) > 5:
                print(f"  ... 还有 {len(wiki_list) - 5} 个")
        else:
            print("  暂无知识库")
        
        return True
    else:
        print("ERROR: API 调用失败")
        print(f"  返回码：{result.get('code') if result else 'N/A'}")
        print(f"  消息：{result.get('msg') if result else 'N/A'}")
        return False

def test_search_knowledge():
    """测试 2: 搜索知识库内容"""
    print("")
    print("=" * 60)
    print("  测试 2: 搜索知识库内容")
    print("=" * 60)
    print("")
    
    # 先获取知识库列表
    kb_result = ima_api("openapi/wiki/v1/search_knowledge_base", {
        "query": "",
        "cursor": "",
        "limit": 1
    })
    
    if not kb_result or kb_result.get("code") != 20000:
        print("ERROR: 无法获取知识库列表，跳过搜索测试")
        return False
    
    wiki_list = kb_result.get("data", {}).get("wiki_list", [])
    if not wiki_list:
        print("ERROR: 暂无知识库，跳过搜索测试")
        return False
    
    knowledge_base_id = wiki_list[0].get("id")
    print(f"使用知识库 ID: {knowledge_base_id}")
    print("")
    
    # 搜索内容
    result = ima_api("openapi/wiki/v1/search_knowledge", {
        "query": "测试",
        "knowledge_base_id": knowledge_base_id,
        "cursor": ""
    })
    
    if result and result.get("code") == 20000:
        data = result.get("data", {})
        items = data.get("item_list", [])
        
        print("SUCCESS: 搜索成功")
        print(f"  结果数量：{len(items)}")
        
        if items:
            print("")
            print("搜索结果:")
            for i, item in enumerate(items[:3], 1):
                print(f"  {i}. {item.get('title', '未命名')}")
        else:
            print("  无匹配结果")
        
        return True
    else:
        print("ERROR: 搜索失败")
        print(f"  返回码：{result.get('code') if result else 'N/A'}")
        return False

def test_get_knowledge_list():
    """测试 3: 浏览知识库内容列表"""
    print("")
    print("=" * 60)
    print("  测试 3: 浏览知识库内容列表")
    print("=" * 60)
    print("")
    
    # 先获取知识库列表
    kb_result = ima_api("openapi/wiki/v1/search_knowledge_base", {
        "query": "",
        "cursor": "",
        "limit": 1
    })
    
    if not kb_result or kb_result.get("code") != 20000:
        print("ERROR: 无法获取知识库列表，跳过浏览测试")
        return False
    
    wiki_list = kb_result.get("data", {}).get("wiki_list", [])
    if not wiki_list:
        print("ERROR: 暂无知识库，跳过浏览测试")
        return False
    
    knowledge_base_id = wiki_list[0].get("id")
    print(f"使用知识库 ID: {knowledge_base_id}")
    print("")
    
    # 浏览内容
    result = ima_api("openapi/wiki/v1/get_knowledge_list", {
        "knowledge_base_id": knowledge_base_id,
        "cursor": "",
        "limit": 10
    })
    
    if result and result.get("code") == 20000:
        data = result.get("data", {})
        items = data.get("item_list", [])
        
        print("SUCCESS: 浏览成功")
        print(f"  内容数量：{len(items)}")
        
        if items:
            print("")
            print("内容列表:")
            for i, item in enumerate(items[:5], 1):
                item_type = item.get("media_type", 0)
                type_name = {
                    1: "PDF", 3: "Word", 4: "PPT", 5: "Excel",
                    7: "Markdown", 9: "图片", 11: "笔记", 13: "文本"
                }.get(item_type, f"类型{item_type}")
                
                print(f"  {i}. [{type_name}] {item.get('name', '未命名')}")
            if len(items) > 5:
                print(f"  ... 还有 {len(items) - 5} 个")
        else:
            print("  知识库为空")
        
        return True
    else:
        print("ERROR: 浏览失败")
        print(f"  返回码：{result.get('code') if result else 'N/A'}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("  IMA 知识库功能测试")
    print("=" * 60)
    print("")
    
    # 检查凭证
    client_id, api_key = load_credentials()
    
    if not client_id:
        print("ERROR: Client ID 未配置")
        print("   请按 Setup 步骤配置：https://ima.qq.com/agent-interface")
        return False
    
    if not api_key:
        print("ERROR: API Key 未配置")
        print("   请按 Setup 步骤配置：https://ima.qq.com/agent-interface")
        return False
    
    print("SUCCESS: 凭证检查通过")
    print(f"  Client ID: {client_id[:8]}...{client_id[-8:]}")
    print(f"  API Key:  已配置 ({len(api_key)} 字符)")
    print("")
    
    # 运行测试
    results = []
    
    results.append(("获取知识库列表", test_get_knowledge_bases()))
    results.append(("搜索知识库内容", test_search_knowledge()))
    results.append(("浏览知识库内容", test_get_knowledge_list()))
    
    # 汇总结果
    print("")
    print("=" * 60)
    print("  测试结果汇总")
    print("=" * 60)
    print("")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {status} - {name}")
    
    print("")
    print(f"总计：{passed}/{total} 测试通过")
    
    if passed == total:
        print("")
        print("SUCCESS: 所有测试通过！IMA 知识库功能正常")
        return True
    else:
        print("")
        print("WARNING: 部分测试失败，请检查凭证或网络连接")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
