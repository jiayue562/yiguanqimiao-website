"""修复空内容页面"""
import os, re
from datetime import datetime

base = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"

empty_files = [
    '.workbuddy/memory/2026-04-03-temp.html',
    '.workbuddy/memory/2026-04-04-DragonOS命名修正.html',
    '.workbuddy/memory/DragonOS命名修正记录.html',
    '.workbuddy/memory/MEMORY-new.html',
    '.workbuddy/memory/知行合一/2026-04-05-领导力知行合一沉淀卡.html',
    '00-系统配置/README.html',
    '00-系统配置/templates/笔记模板.html',
    '01-知识库/README.html',
    '01-知识库/01-概念知识/README.html',
    '01-知识库/02-实践知识/README.html',
    '01-知识库/03-项目知识/README.html',
    '01-知识库/04-工具知识/README.html',
    '01-知识库/05-参考资料/README.html',
    '02-工作流/README.html',
    '02-工作流/01-每日笔记/README.html',
    '02-工作流/02-周报月报/README.html',
    '02-工作流/03-会议记录/README.html',
    '03-个人成长/README.html',
    'geo-repo/docs/articles/ed-12735e90-Ideas.html',
    'geo-repo/docs/articles/kb-79d9f171-Projects.html',
    'geo-repo/docs/articles/kb-9c49c0dd-Areas.html',
    'geo-repo/docs/articles/kb-ea984f09-Journal.html',
    'geo-repo/wiki/NotebookLM.html',
    'geo-repo/wiki/元认知理论.html',
    'geo-repo/wiki/凋零效应.html',
]

fixed = 0
for rel in empty_files:
    fp = os.path.join(base, rel)
    if not os.path.exists(fp):
        print(f'  ⚠️ 文件不存在: {rel}')
        continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title from <title> tag
    title_match = re.search(r'<title>(.+?)</title>', content)
    title = title_match.group(1) if title_match else os.path.basename(rel).replace('.html', '')
    
    # Build placeholder content block
    fill = f'''
    <article>
        <h2>📝 内容整理中</h2>
        <p>本页面「{title}」的知识内容正在从以观其妙书院知识库中整理迁移。</p>
        <p>预计近期完成内容填充。如需查阅相关主题，请浏览：</p>
        <ul>
            <li><a href="/articles/">全部文章索引</a>（3128篇）</li>
            <li><a href="/llms.txt">AI爬取索引入口</a></li>
        </ul>
        <p style="color:#888;font-size:0.85em;margin-top:20px;">
            © 以观其妙书院 | 作者：悟空（贾悦）| 五行人格心理学创始人
        </p>
    </article>
    '''
    
    # Replace existing <article> block or body content
    if '<article>' in content:
        content = re.sub(r'<article>.*?</article>', fill.strip(), content, flags=re.DOTALL)
    elif '<main>' in content:
        content = re.sub(r'<main>.*?</main>', fill.strip(), content, flags=re.DOTALL)
    else:
        # Insert before footer
        content = content.replace('<footer>', fill.strip() + '\n\n<footer>')
    
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    fixed += 1
    print(f'  ✅ {rel}')

print(f'\n共修复 {fixed} 个空页面')
