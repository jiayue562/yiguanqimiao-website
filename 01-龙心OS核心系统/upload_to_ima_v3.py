#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传《第一期工作坊+5次俱乐部》到IMA知识库
作者：龙龟神将
日期：2026-05-25
"""

import os
import sys
import json
import urllib.request
import urllib.error

# IMA认证信息（从环境变量读取）
IMA_CLIENT_ID = os.environ.get('IMA_OPENAPI_CLIENTID', '')
IMA_API_KEY = os.environ.get('IMA_OPENAPI_APIKEY', '')

# 知识库配置
KB_ID = "DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY="  # 以观其妙书院
FOLDER_ID = "folder_7441985942068358"  # 龙龟神将备份资料

def read_credential(credential_path):
    """读取认证信息"""
    try:
        with open(credential_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return None

def upload_markdown_as_note(file_path, kb_id, folder_id=None):
    """上传Markdown文件到IMA知识库（使用import_doc方法）"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取文件名作为标题
    title = os.path.basename(file_path).replace('.md', '')
    
    # 构建请求头
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Accept': 'application/json'
    }
    
    # 如果有认证信息，添加到请求头
    if IMA_CLIENT_ID and IMA_API_KEY:
        headers['ima-openapi-clientid'] = IMA_CLIENT_ID
        headers['ima-openapi-apikey'] = IMA_API_KEY
    else:
        # 尝试从配置文件读取
        client_id = read_credential(os.path.expanduser('~/.config/ima/client_id'))
        api_key = read_credential(os.path.expanduser('~/.config/ima/api_key'))
        if client_id and api_key:
            headers['ima-openapi-clientid'] = client_id
            headers['ima-openapi-apikey'] = api_key
        else:
            raise Exception("❌ IMA认证信息未配置，请设置环境变量或配置文件")
    
    # 1. 创建笔记（import_doc）
    import_url = 'https://ima.qq.com/openapi/note/v1/import_doc'
    import_data = {
        'content_format': 1,  # 1=Markdown
        'content': content
    }
    
    try:
        req = urllib.request.Request(
            import_url,
            data=json.dumps(import_data, ensure_ascii=False).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode('utf-8')
            print(f"   🔍 API响应: {response_data[:200]}")  # 打印前200个字符
            result = json.loads(response_data)
            print(f"   🔍 完整响应: {json.dumps(result, ensure_ascii=False)}")
            
            # 检查响应格式
            if result.get('ret') == 0 or result.get('code') == 0 or 'note_id' in str(result):
                # 尝试多种可能的响应格式
                note_id = None
                if 'data' in result and 'note_id' in result['data']:
                    note_id = result['data']['note_id']
                elif 'note_id' in result:
                    note_id = result['note_id']
                elif 'data' in result and isinstance(result['data'], str):
                    note_id = result['data']
                
                if note_id:
                    print(f"✅ 笔记创建成功: {title}")
                    print(f"   Note ID: {note_id}")
                else:
                    raise Exception(f"创建笔记失败: 无法获取note_id from {result}")
            else:
                # 获取错误信息
                error_msg = result.get('msg', result.get('message', json.dumps(result, ensure_ascii=False)))
                raise Exception(f"创建笔记失败: {error_msg}")
    except Exception as e:
        raise Exception(f"❌ 创建笔记失败: {str(e)}")
    
    # 2. 将笔记添加到知识库
    add_url = 'https://ima.qq.com/openapi/wiki/v1/add_knowledge'
    add_data = {
        'media_type': 11,  # 11=笔记
        'note_info': {
            'content_id': str(note_id)
        },
        'title': title,
        'knowledge_base_id': kb_id
    }
    
    if folder_id:
        add_data['folder_id'] = folder_id
    
    try:
        req = urllib.request.Request(
            add_url,
            data=json.dumps(add_data, ensure_ascii=False).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            if result.get('ret') == 0:
                print(f"✅ 笔记已添加到知识库: {title}")
                print(f"   知识库ID: {kb_id}")
                if folder_id:
                    print(f"   文件夹ID: {folder_id}")
            else:
                raise Exception(f"添加到知识库失败: {result.get('msg')}")
    except Exception as e:
        raise Exception(f"❌ 添加到知识库失败: {str(e)}")
    
    return note_id

def main():
    """主函数"""
    print("📤 开始上传《第一期工作坊+5次俱乐部》到IMA知识库...")
    print(f"   知识库: 以观其妙书院 (kb_id: {KB_ID})")
    print(f"   文件夹: 龙龟神将备份资料 (folder_id: {FOLDER_ID})")
    print()
    
    # 上传文件1：深度学习文档
    file1 = r"D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/第一期工作坊+5次俱乐部-深度学习与知识图谱.md"
    print(f"📄 上传文件1: {os.path.basename(file1)}")
    try:
        note_id_1 = upload_markdown_as_note(file1, KB_ID, FOLDER_ID)
        print(f"   ✅ 上传成功! Note ID: {note_id_1}")
    except Exception as e:
        print(f"   ❌ 上传失败: {str(e)}")
        return
    
    print()
    
    # 上传文件2：知识图谱文件
    file2 = r"D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/第一期工作坊+5次俱乐部-知识图谱.md"
    print(f"📄 上传文件2: {os.path.basename(file2)}")
    try:
        note_id_2 = upload_markdown_as_note(file2, KB_ID, FOLDER_ID)
        print(f"   ✅ 上传成功! Note ID: {note_id_2}")
    except Exception as e:
        print(f"   ❌ 上传失败: {str(e)}")
        return
    
    print()
    print("🎉 所有文件上传完成!")
    print(f"   文件1 Note ID: {note_id_1}")
    print(f"   文件2 Note ID: {note_id_2}")

if __name__ == '__main__':
    main()
