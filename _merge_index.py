#!/usr/bin/env python3
"""Merge old root index.html (1494 articles) with new docs/index.html (2921 articles)."""
import sys, os, re, html
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT_INDEX = r"C:\dragon-heart-os\yiguanqimiao-website\index.html"
DOCS_INDEX = r"C:\dragon-heart-os\yiguanqimiao-website\docs\index.html"
OUTPUT = r"C:\dragon-heart-os\yiguanqimiao-website\index.html"

# Read old index to extract categorized article links
with open(ROOT_INDEX, "r", encoding="utf-8", errors="replace") as f:
    old_html = f.read()

# Read new index to extract flat article list
with open(DOCS_INDEX, "r", encoding="utf-8", errors="replace") as f:
    new_html = f.read()

# Extract old sections: <h2>Category (N篇)</h2><ul>...<li><a href="...">title</a></li>...</ul>
old_sections = re.findall(
    r'<h2>(.*?)</h2>\s*<ul>(.*?)</ul>',
    old_html,
    re.DOTALL
)

# Extract new article items (all items after the first <ul>)
new_section_match = re.search(
    r'<div class="s"><ul>(.*?)</ul></div>',
    new_html,
    re.DOTALL
)
new_items = new_section_match.group(1).strip() if new_section_match else ""

# Build new sections by replacing relative links in old sections
processed_old = []
for section_title, ul_content in old_sections:
    items = re.findall(r'<li>(.*?)</li>', ul_content, re.DOTALL)
    processed_old.append((section_title, len(items), ul_content))

# Generate new GEO section
new_count = len(re.findall(r'<li>', new_items))
geo_section = f'<h2>📦 GEO知识库转化（{new_count}篇）</h2>\n<ul>\n{new_items}\n</ul>'

# Build total count
total = sum(c for _, c, _ in processed_old) + new_count

# Build merged HTML
# Extract head section from old index
head_match = re.search(
    r'(<!DOCTYPE html>.*?</head>\s*<body>.*?<div class="wrap">.*?<div class="h">.*?</div>)',
    old_html,
    re.DOTALL
)
head_section = head_match.group(1) if head_match else ""

# Replace old count
head_section = re.sub(
    r'总 \d+ 篇文章',
    f'总 {total} 篇文章',
    head_section
)

# Extract footer
footer_match = re.search(r'(<div class="f">.*?</div>\s*</div>\s*</body>\s*</html>)', old_html, re.DOTALL)
footer = footer_match.group(1) if footer_match else '<div class="f">© 以观其妙书院</div></div></body></html>'

# Build sections HTML
all_sections_html = ""
for title, count, content in processed_old:
    all_sections_html += f'<div class="s">\n<h2>{title}</h2>\n<ul>\n{content}\n</ul>\n</div>\n'
all_sections_html += f'<div class="s">\n{geo_section}\n</div>\n'

# Build new index
merged = head_section + '\n' + all_sections_html + '\n' + footer

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(merged)
print(f"Merged index.html: {total} articles ({sum(c for _,c,_ in processed_old)} old + {new_count} new)")
