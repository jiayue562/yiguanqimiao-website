"""
全面深度审计：逐页检查内容 + 五行识人替换 + 统计报告
"""
import os, re, sys

BASE = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"

results = {
    'total': 0,
    'good': 0,        # 有实际正文
    'light': 0,       # 内容偏少 (<300字)
    'empty': 0,       # 几乎无内容 (<50字)
    'replaced': 0,    # 替换了五行识人
}

empty_details = []
light_details = []

for root, dirs, files in os.walk(BASE):
    for f in files:
        if not f.endswith('.html') or f == 'index.html':
            continue
        
        fp = os.path.join(root, f)
        rel = os.path.relpath(fp, BASE)
        results['total'] += 1
        
        try:
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            empty_details.append((rel, 'READ_ERROR'))
            results['empty'] += 1
            continue
        
        # 替换五行识人
        if '五行识人' in content:
            content = content.replace('五行识人', '五行人格')
            with open(fp, 'w', encoding='utf-8') as fh:
                fh.write(content)
            results['replaced'] += 1
        
        # 提取正文文字（移除HTML标签）
        text = content
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL)
        text = re.sub(r'<head[^>]*>.*?</head>', '', text, flags=re.DOTALL)
        
        # Extract article/main content specifically
        article = re.search(r'<(?:article|main)[^>]*>(.*?)</(?:article|main)>', text, re.DOTALL)
        if article:
            body = article.group(1)
        else:
            # Fallback: all remaining text
            body = text
        
        # Strip all HTML tags
        body = re.sub(r'<[^>]+>', ' ', body)
        body = re.sub(r'&[a-z]+;', ' ', body)
        body = re.sub(r'\s+', ' ', body).strip()
        char_count = len(body)
        
        # Classify
        if char_count >= 300:
            results['good'] += 1
        elif char_count >= 50:
            results['light'] += 1
            if char_count < 150:
                light_details.append((rel, char_count))
        else:
            results['empty'] += 1
            empty_details.append((rel, char_count))

# Report
print("=" * 60)
print("以观其妙书院 — 全站深度审计报告")
print("=" * 60)
print(f"")
print(f"📊 总页面数: {results['total']}")
print(f"   ✅ 内容完整 (>300字): {results['good']} ({100*results['good']//max(results['total'],1)}%)")
print(f"   ⚠️  内容偏少 (50-300字): {results['light']} ({100*results['light']//max(results['total'],1)}%)")
print(f"   ❌ 几乎无内容 (<50字): {results['empty']} ({100*results['empty']//max(results['total'],1)}%)")
print(f"")
print(f"🔄 「五行识人」→「五行人格」: {results['replaced']} 个文件")
print(f"")

if empty_details:
    print(f"=== ❌ 空内容页面 ({len(empty_details)}) ===")
    for rel, cc in empty_details:
        print(f"  [{cc}] {rel}")

if light_details:
    print(f"")
    print(f"=== ⚠️ 内容偏少页面 ({len(light_details)}) ===")
    for rel, cc in light_details:
        print(f"  [{cc}字] {rel}")

print(f"")
print(f"=== 结论 ===")
health = results['good'] / max(results['total'], 1) * 100
if health > 95:
    print(f"✅ 网站健康度: {health:.1f}% — 优秀")
elif health > 80:
    print(f"⚠️ 网站健康度: {health:.1f}% — 良好，建议补齐空页面")
else:
    print(f"❌ 网站健康度: {health:.1f}% — 需要修复")
