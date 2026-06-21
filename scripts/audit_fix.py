import os

base = r"C:\Users\jia'yue\WorkBuddy\yiguanqimiao-website\articles"

total = 0
archive_count = 0
main_count = 0
replaced = 0

for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith('.html'):
            total += 1
            if 'archive' in root:
                archive_count += 1
            else:
                main_count += 1

            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                if '五行识人' in content:
                    new_content = content.replace('五行识人', '五行人格')
                    # Also replace in meta tags and structured data
                    new_content = new_content.replace('五行识人', '五行人格')
                    with open(fp, 'w', encoding='utf-8') as fh:
                        fh.write(new_content)
                    replaced += 1
            except Exception as e:
                print(f'Error: {fp}: {e}')

print(f'总HTML文件: {total}')
print(f'  主文章: {main_count}')
print(f'  归档: {archive_count}')
print(f'')
print(f'替换「五行识人」→「五行人格」: {replaced} 个文件')
