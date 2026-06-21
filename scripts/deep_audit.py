"""全面审计所有文章链接，修复空内容页面"""
import os, re

base = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"

empty_pages = []
has_content = []
has_md_source = []

for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.html') and f != 'index.html':
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, base)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                
                # Extract body content (between <article> and </article> or <main> tags)
                body_match = re.search(r'<(?:article|main)[^>]*>(.*?)</(?:article|main)>', content, re.DOTALL)
                if body_match:
                    body_text = re.sub(r'<[^>]+>', ' ', body_match.group(1))
                    body_text = re.sub(r'\s+', ' ', body_text).strip()
                    word_count = len(body_text)
                else:
                    # Fallback: get text after removing all HTML tags
                    text = re.sub(r'<[^>]+>', ' ', content)
                    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
                    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
                    text = re.sub(r'\s+', ' ', text).strip()
                    # Remove navigation, footer, header text
                    word_count = len(text)
                
                # Check for placeholder patterns
                is_placeholder = any(ph in content for ph in [
                    '请阅读正文获取完整内容',
                    '暂无内容',
                    '核心定义',
                    '常见问题',
                ]) and word_count < 500
                
                if word_count < 200 or is_placeholder:
                    empty_pages.append({
                        'file': rel,
                        'chars': word_count,
                        'placeholder': is_placeholder
                    })
                else:
                    has_content.append({'file': rel, 'chars': word_count})
                    
            except Exception as e:
                print(f'Error reading {rel}: {e}')

print(f'审计完成:')
print(f'  有内容文章: {len(has_content)}')
print(f'  空/占位页面: {len(empty_pages)}')
print(f'')

if empty_pages:
    print('=== 空页面列表（前30个）===')
    for p in empty_pages[:30]:
        tag = ' [占位]' if p['placeholder'] else ''
        print(f'  {p["file"]} ({p["chars"]} 字符){tag}')
    
    if len(empty_pages) > 30:
        print(f'  ... 还有 {len(empty_pages) - 30} 个空页面')
