#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传《09第九章 化克为生》深度学习文档到IMA知识库
"""

import os
import json
import urllib.request
import urllib.error

# IMA API配置
CLIENT_ID = "your_client_id"  # 需要从配置文件中读取
API_KEY = "your_api_key"      # 需要从配置文件中读取
KB_ID = "DhG0JMfmIYIkPOxSs3U4gCpnqzCX2JQfBwqUAy887ZY="
FOLDER_ID = "folder_7441985942068358"  # 龙龟神将备份资料文件夹

def read_credential(file_path):
    """读取认证信息"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return None

def upload_to_ima(file_path, title):
    """上传文件到IMA知识库"""
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 准备请求头
    headers = {
        'ima-openapi-clientid': CLIENT_ID,
        'ima-openapi-apikey': API_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    # 1. 创建笔记（import_doc）
    import_url = 'https://ima.qq.com/openapi/note/v1/import_doc'
    import_data = {
        'content_format': 1,  # 1表示Markdown格式
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
        
        if result.get('code') == 0:
            note_id = result['data']['note_id']
            print(f"✅ 笔记创建成功: note_id={note_id}")
            
            # 2. 将笔记添加到知识库
            add_url = 'https://ima.qq.com/openapi/wiki/v1/add_knowledge'
            add_data = {
                'media_type': 11,  # 11表示笔记类型
                'note_info': {
                    'content_id': note_id
                },
                'title': title,
                'knowledge_base_id': KB_ID,
                'folder_id': FOLDER_ID
            }
            
            req2 = urllib.request.Request(
                add_url,
                data=json.dumps(add_data, ensure_ascii=False).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req2) as response2:
                result2 = json.loads(response2.read().decode('utf-8'))
            
            if result2.get('code') == 0:
                print(f"✅ 笔记已添加到知识库: {title}")
                return True
            else:
                print(f"❌ 添加到知识库失败: {result2.get('message')}")
                return False
        else:
            print(f"❌ 创建笔记失败: {result.get('message')}")
            return False
            
    except Exception as e:
        print(f"❌ 上传失败: {str(e)}")
        return False

# 主函数
if __name__ == "__main__":
    # 读取认证信息（需要从实际配置文件中读取）
    # 这里需要先读取存储认证信息的文件
    print("开始上传《09第九章 化克为生》到IMA知识库...")
    
    # 上传深度学习文档
    file1 = r'D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/09第九章 化克为生-深度学习与知识图谱.md'
    title1 = "09第九章 化克为生-深度学习与知识图谱"
    upload_to_ima(file1, title1)
    
    # 上传知识图谱文档
    file2 = r'D:/以观其妙书院知识库/以观其妙书院/01-龙心OS核心系统/09第九章 化克为生-知识图谱.md'
    title2 = "09第九章 化克为生-知识图谱"
    upload_to_ima(file2, title2)
    
    print("上传完成！")
