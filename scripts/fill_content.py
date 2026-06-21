"""从原始 .md 文件补充薄页面内容"""
import os, re

BASE = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"
CLAW = r"C:\Users\jia'yue\WorkBuddy\Claw"

# Map thin pages to their .md source files
sources = {
    # geo-repo wiki pages
    'geo-repo\\wiki\\NotebookLM.html': r'geo-repo\wiki\NotebookLM.md',
    'geo-repo\\wiki\\元认知理论.html': r'geo-repo\wiki\元认知理论.md',
    'geo-repo\\wiki\\凋零效应.html': r'geo-repo\wiki\凋零效应.md',
    # geo-repo docs  
    'geo-repo\\docs\\articles\\ed-12735e90-Ideas.html': r'geo-repo\docs\articles\ed-12735e90-Ideas.md',
    'geo-repo\\docs\\articles\\kb-79d9f171-Projects.html': r'geo-repo\docs\articles\kb-79d9f171-Projects.md',
    'geo-repo\\docs\\articles\\kb-9c49c0dd-Areas.html': r'geo-repo\docs\articles\kb-9c49c0dd-Areas.md',
    'geo-repo\\docs\\articles\\kb-ea984f09-Journal.html': r'geo-repo\docs\articles\kb-ea984f09-Journal.md',
}

def md_to_html_simple(md_text):
    """Simple markdown to HTML paragraph conversion"""
    # Remove frontmatter
    if md_text.startswith('---'):
        parts = md_text.split('---', 2)
        md_text = parts[2] if len(parts) >= 3 else md_text
    
    # Headers
    md_text = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    
    # Bold
    md_text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md_text)
    
    # Links
    md_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md_text)
    
    # Lists
    md_text = re.sub(r'^- (.+)$', r'<li>\1</li>', md_text, flags=re.MULTILINE)
    
    # Blockquote
    md_text = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', md_text, flags=re.MULTILINE)
    
    # Code
    md_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', md_text)
    
    # Wrap non-tag paragraphs
    blocks = md_text.split('\n\n')
    result = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if b.startswith('<'):
            result.append(b)
        else:
            result.append(f'<p>{b}</p>')
    
    return '\n'.join(result)

fixed = 0
for rel_html, rel_md in sources.items():
    html_path = os.path.join(BASE, rel_html)
    md_path = os.path.join(CLAW, rel_md)
    
    if not os.path.exists(html_path):
        print(f'  ⚠️ HTML not found: {rel_html}')
        continue
    
    if not os.path.exists(md_path):
        print(f'  ⚠️ MD not found: {rel_md}')
        # Try alternative paths
        alt = os.path.join(CLAW, os.path.basename(rel_md))
        if os.path.exists(alt):
            md_path = alt
        else:
            continue
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    body_html = md_to_html_simple(md_content)
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace <article> block
    if '<article>' in html:
        html = re.sub(r'<article>.*?</article>', f'<article>\n{body_html}\n</article>', html, flags=re.DOTALL)
    else:
        # Insert before footer
        html = html.replace('<footer>', f'<article>\n{body_html}\n</article>\n\n<footer>')
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    fixed += 1
    title_match = re.search(r'<title>(.+?)</title>', html)
    title = title_match.group(1) if title_match else rel_html
    print(f'  ✅ {title[:50]}')

print(f'\n共补充 {fixed} 个页面内容')
