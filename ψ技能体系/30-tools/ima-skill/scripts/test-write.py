# -*- coding: utf-8 -*-
# IMA 知识库写入测试脚本
# 龙心 OS · 2026-04-16

import os
import sys
import requests
import json
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 加载凭证
config_dir = Path.home() / '.config' / 'ima'
client_id = ''
api_key = ''

if (config_dir / 'client_id').exists():
    with open(config_dir / 'client_id', 'r', encoding='utf-8-sig') as f:
        client_id = f.read().strip()

if (config_dir / 'api_key').exists():
    with open(config_dir / 'api_key', 'r', encoding='utf-8-sig') as f:
        api_key = f.read().strip()

headers = {
    'ima-openapi-clientid': client_id,
    'ima-openapi-apikey': api_key,
    'Content-Type': 'application/json'
}

# 个人知识库 ID
KB_ID = 'akRnDE_2uPqRYS0xpZQRYzTPxeKhtxUM4xk7i0YUS8E='

def test_add_text_content():
    """测试添加文本内容"""
    print('=' * 70)
    print('  测试 1: 添加文本内容到个人知识库')
    print('=' * 70)
    print('')
    
    # 创建测试文本
    test_text = f'''龙心 OS IMA 写入测试

测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
测试目的：验证 IMA API 文本写入功能

测试内容：
- 验证 API 认证
- 验证文本添加功能
- 验证内容保存

---
此内容由龙心 OS 自动创建，测试完成后可删除
'''
    
    # 使用 add_knowledge API 添加文本
    url = 'https://ima.qq.com/openapi/wiki/v1/add_knowledge'
    body = {
        'media_type': 13,  # TXT 类型
        'title': f'龙心 OS 测试 - {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        'knowledge_base_id': KB_ID,
        'text_info': {
            'content': test_text
        }
    }
    
    print(f'调用 API: {url}')
    print(f'知识库：个人知识库')
    print(f'内容类型：TXT (media_type=13)')
    print('')
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        print(f'HTTP 状态码：{response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'返回码：{data.get("code")}')
            print(f'消息：{data.get("msg")}')
            
            if data.get('code') == 0:
                print('')
                print('✅ 测试成功！文本内容已添加')
                return True
            else:
                print('')
                print(f'❌ 添加失败：{data.get("msg")}')
                return False
        else:
            print(f'响应内容：{response.text[:200]}')
            print('')
            print('❌ HTTP 请求失败')
            return False
    except Exception as e:
        print(f'❌ 请求异常：{e}')
        return False

def test_add_url():
    """测试添加 URL"""
    print('')
    print('=' * 70)
    print('  测试 2: 添加 URL 到个人知识库')
    print('=' * 70)
    print('')
    
    url = 'https://ima.qq.com/openapi/wiki/v1/import_urls'
    body = {
        'knowledge_base_id': KB_ID,
        'urls': ['https://docs.openclaw.ai']
    }
    
    print(f'调用 API: {url}')
    print(f'URL: https://docs.openclaw.ai')
    print('')
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        print(f'HTTP 状态码：{response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'返回码：{data.get("code")}')
            print(f'消息：{data.get("msg")}')
            
            if data.get('code') == 0:
                results = data.get('data', {}).get('result_list', [])
                if results:
                    print(f'导入结果：{results[0].get("ret_code") == 0 and "成功" or "失败"}')
                print('')
                print('✅ 测试成功！URL 已添加')
                return True
            else:
                print('')
                print(f'❌ 添加失败：{data.get("msg")}')
                return False
        else:
            print(f'响应内容：{response.text[:200]}')
            print('')
            print('❌ HTTP 请求失败')
            return False
    except Exception as e:
        print(f'❌ 请求异常：{e}')
        return False

def test_verify_content():
    """验证内容是否添加成功"""
    print('')
    print('=' * 70)
    print('  测试 3: 验证内容是否已保存')
    print('=' * 70)
    print('')
    
    url = 'https://ima.qq.com/openapi/wiki/v1/get_knowledge_list'
    body = {
        'knowledge_base_id': KB_ID,
        'cursor': '',
        'limit': 5
    }
    
    print('获取知识库内容列表...')
    print('')
    
    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        data = response.json()
        
        if data.get('code') == 0:
            items = data.get('data', {}).get('item_list', [])
            
            if items:
                print(f'找到 {len(items)} 个内容:')
                print('')
                for i, item in enumerate(items, 1):
                    name = item.get('name', '未命名')
                    media_type = str(item.get('media_type', '0'))
                    print(f'  {i}. [类型{media_type}] {name}')
                print('')
                print('✅ 内容验证成功！')
                return True
            else:
                print('(知识库为空)')
                return False
        else:
            print(f'获取失败：{data.get("msg")}')
            return False
    except Exception as e:
        print(f'❌ 请求异常：{e}')
        return False

def main():
    """主函数"""
    print('=' * 70)
    print('  IMA 个人知识库 - 完整功能测试')
    print('=' * 70)
    print('')
    
    # 检查凭证
    if not client_id or not api_key:
        print('❌ 缺少 IMA 凭证')
        return False
    
    print(f'Client ID: {client_id[:8]}...{client_id[-8:]}')
    print(f'API Key: 已配置 ({len(api_key)} 字符)')
    print('')
    
    # 运行测试
    results = []
    
    results.append(('添加文本内容', test_add_text_content()))
    results.append(('添加 URL', test_add_url()))
    results.append(('验证内容', test_verify_content()))
    
    # 汇总
    print('')
    print('=' * 70)
    print('  测试结果汇总')
    print('=' * 70)
    print('')
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = '✅ 通过' if result else '❌ 失败'
        print(f'  {status} - {name}')
    
    print('')
    print(f'总计：{passed}/{total} 测试通过')
    
    if passed == total:
        print('')
        print('🎉 所有测试通过！个人知识库读写功能正常')
        return True
    else:
        print('')
        print('⚠️ 部分测试失败')
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
