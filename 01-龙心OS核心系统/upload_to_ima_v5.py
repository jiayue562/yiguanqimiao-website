#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMA上传脚本 v5 - 上传《亲密关系工作坊讲师手册》到IMA知识库
"""

import os
import sys
import json
import urllib.request
import urllib.error

# IMA认证信息（从环境变量读取）
def read_credential(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return None

# 尝试从环境变量获取
client_id = os.environ.get('IMA_OPENAPI_CLIENTID')
api_key = os.environ.get('IMA_OPENAPI_APIKEY')

# 如果环境变量不存在，尝试从文件读取
if not client_id:
    client_id = read_credential(os.path.expanduser('~/.config/ima/client_id'))
if not api_key:
    api_key = read_credential(os.path.expanduser('~/.config/ima/api_key'))

if not client_id or not api_key:
    print("[错误] 未找到IMA认证信息，请设置环境变量或配置文件")
    sys.exit(1)

# IMA API配置
BASE_URL = 'https://ima.qq.com'
KB_ID = 'DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY='  # 以观其妙书院知识库
FOLDER_ID = 'folder_7441985942068358'  # 龙龟神将备份资料文件夹

# 要上传的文件列表
files_to_upload = [
    {
        'path': r"D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/亲密关系工作坊讲师手册-深度学习与知识图谱.md",
        'title': '亲密关系工作坊讲师手册-深度学习与知识图谱',
        'type': 'markdown'
    },
    {
        'path': r"D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/亲密关系工作坊-知识图谱.md",
        'title': '亲密关系工作坊-知识图谱',
        'type': 'markdown'
    }
]

def upload_markdown_as_note(file_path, kb_id, folder_id=None):
    """使用import_doc方法上传Markdown文件到IMA"""
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    headers = {
        'ima-openapi-clientid': client_id,
        'ima-openapi-apikey': api_key,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 1. 创建笔记（import_doc）
    import_url = f'{BASE_URL}/openapi/note/v1/import_doc'
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
            result = json.loads(response.read().decode('utf-8'))
            # 检查响应格式（IMA API使用code而不是ret）
            response_code = result.get('code', result.get('ret', -1))
            if response_code == 0:
                # 尝试多种可能的响应格式
                note_id = None
                if 'data' in result and isinstance(result['data'], dict) and 'note_id' in result['data']:
                    note_id = result['data']['note_id']
                elif 'data' in result and isinstance(result['data'], str):
                    note_id = result['data']
                elif 'note_id' in result:
                    note_id = result['note_id']
                
                if note_id:
                    print(f"[OK] 笔记创建成功: {os.path.basename(file_path)}")
                    print(f"    Note ID: {note_id}")
                    return note_id
                else:
                    raise Exception(f"创建笔记失败: 无法获取note_id from {result}")
            else:
                error_msg = result.get('msg', result.get('message', json.dumps(result, ensure_ascii=False)))
                raise Exception(f"创建笔记失败: {error_msg}")
    except Exception as e:
        print(f"[错误] 创建笔记失败: {str(e)}")
        return None

def add_note_to_knowledge(note_id, kb_id, folder_id=None, title=''):
    """将笔记添加到知识库"""
    
    headers = {
        'ima-openapi-clientid': client_id,
        'ima-openapi-apikey': api_key,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 2. 将笔记添加到知识库
    add_url = f'{BASE_URL}/openapi/wiki/v1/add_knowledge'
    add_data = {
        'media_type': 11,  # 11=笔记类型
        'note_info': {
            'content_id': str(note_id)
        },
        'title': title,
        'knowledge_base_id': kb_id
    }
    
    # 如果指定了文件夹，添加到文件夹
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
            # 检查响应格式
            response_code = result.get('code', result.get('ret', -1))
            if response_code == 0:
                print(f"[OK] 笔记已添加到知识库: {title}")
                return True
            else:
                error_msg = result.get('msg', result.get('message', json.dumps(result, ensure_ascii=False)))
                raise Exception(f"添加笔记到知识库失败: {error_msg}")
    except Exception as e:
        print(f"[错误] 添加笔记到知识库失败: {str(e)}")
        return False

# 主程序
if __name__ == '__main__':
    print(f"[信息] 开始上传{len(files_to_upload)}个文件到IMA知识库...")
    print(f"    知识库: 以观其妙书院")
    print(f"    文件夹: 龙龟神将备份资料")
    print()
    
    success_count = 0
    
    for file_info in files_to_upload:
        file_path = file_info['path']
        title = file_info['title']
        
        print(f"[处理] {title}...")
        
        # 上传文件
        note_id = upload_markdown_as_note(file_path, KB_ID, FOLDER_ID)
        
        if note_id:
            # 添加到知识库
            if add_note_to_knowledge(note_id, KB_ID, FOLDER_ID, title):
                success_count += 1
        
        print()
    
    print(f"[完成] 上传完成: {success_count}/{len(files_to_upload)} 个文件成功")
