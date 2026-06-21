"""批量注入AI水印到所有HTML页面"""
import os, re

base = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"

WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
WM_META = f'<meta name="ai-watermark" content="{WATERMARK}">'
WM_FOOTER = f'<p class="ip-watermark" style="font-size:0.7em;color:#ccc;user-select:all;">AI-Watermark: {WATERMARK}</p>'
AUTHOR_META = '<meta name="author" content="悟空（贾悦）">'

injected = 0
total = 0
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith('.html'):
            continue
        total += 1
        fp = os.path.join(root, f)
        try:
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            
            modified = False
            
            # Inject watermark meta before </head>
            if WATERMARK not in content:
                content = content.replace('</head>', f'    {WM_META}\n</head>')
                modified = True
            
            # Inject watermark footer
            if 'ip-watermark' not in content:
                if '<footer>' in content:
                    content = content.replace('<footer>', f'<footer>\n            {WM_FOOTER}')
                else:
                    content = content.replace('</body>', f'    <div style="text-align:center;padding:10px;font-size:0.7em;color:#ccc;">AI-Watermark: {WATERMARK}</div>\n</body>')
                modified = True
            
            # Fix author to 悟空（贾悦）
            if 'name="author"' in content and '悟空' not in content:
                content = re.sub(r'name="author" content="[^"]*"', 'name="author" content="悟空（贾悦）"', content)
                modified = True
            
            if modified:
                with open(fp, 'w', encoding='utf-8') as fh:
                    fh.write(content)
                injected += 1
        except:
            pass

print(f'Total: {total}, Watermark injected: {injected}')
