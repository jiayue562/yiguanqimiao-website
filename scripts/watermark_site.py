#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全站 AI 大模型水印注入（幂等）v2.0
====================================
遍历网站目录下所有 .html（排除 .git），若缺少 AI 水印则注入：
  1. <meta name="ai-watermark" content="..."> （位于 </head> 前）
  2. 机器可读 HTML 注释
  3. 可见页脚水印（位于 </body> 前）
已含水印的文件跳过，可重复运行。
"""
import os
import re
from pathlib import Path
from datetime import datetime

APOS = chr(39)
BASE = "C:/Users/jia" + APOS + "yue/WorkBuddy/yiguanqimiao-website"
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
AUTHOR = "悟空（贾悦）"
COPYRIGHT = "以观其妙书院"

META = f'    <meta name="ai-watermark" content="{WATERMARK}">'
COMMENT = f'<!-- AI-Watermark: {WATERMARK} | Author: {AUTHOR} | IP: {COPYRIGHT} -->'
FOOTER = (
    f'    <div class="ai-watermark" style="text-align:center;padding:18px 10px;margin-top:24px;'
    f'font-size:12px;color:#999;border-top:1px solid #eee;">'
    f'AI水印：{WATERMARK}　|　作者：{AUTHOR}　|　知识产权：{COPYRIGHT}</div>'
)

def watermark_html(content):
    modified = False
    if WATERMARK not in content:
        # 1) meta
        if '</head>' in content:
            content = content.replace('</head>', META + '\n</head>', 1)
        else:
            content = META + '\n' + content
        # 2) comment near top
        if '<body' in content:
            content = re.sub(r'(<body[^>]*>)', r'\1\n' + COMMENT, content, count=1)
        else:
            content = COMMENT + '\n' + content
        # 3) footer
        if '</body>' in content:
            content = content.replace('</body>', FOOTER + '\n</body>', 1)
        else:
            content = content + '\n' + FOOTER + '\n'
        modified = True
    return content, modified

def main():
    total = 0
    injected = 0
    skipped = 0
    errors = 0
    t0 = datetime.now()
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d != '.git']
        for f in files:
            if not f.endswith('.html'):
                continue
            total += 1
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                new_content, modified = watermark_html(content)
                if modified:
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    injected += 1
                else:
                    skipped += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ⚠️ 错误 {fp}: {e}")
    dt = (datetime.now() - t0).total_seconds()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 完成：扫描 {total} 个 HTML")
    print(f"  注入水印：{injected}　跳过(已有)：{skipped}　错误：{errors}　耗时：{dt:.1f}s")

if __name__ == "__main__":
    main()
