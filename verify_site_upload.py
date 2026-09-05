# -*- coding: utf-8 -*-
"""
网站上传质量保障 · 部署前/后校验器 (verify_site_upload.py)
=================================================================
固化 2026-07-28 真实坏链事故的全部根因，作为每次"上传内容→部署"前的
强制门禁。任何一项 ERROR 都会让脚本以退出码 1 结束，阻止 push/部署。

检查的坑（来自真实事故复盘）：
  [1] 空壳 HTML      : 文件存在但内容过短，打开是空白页
  [2] 缺 <title>     : 浏览器标签/SEO 无标题，体验差
  [3] 未打 AI 水印   : 知识产权印记缺失
  [4] CDATA 包裹     : 正文被 <![CDATA[...]]> 包住，浏览器无法渲染正文
  [5] 无正文结构     : 无 <body>/<h1>，内容可能不可见
  [6] 无扩展名副本   : 与 .html 同名的无扩展名文件 → 路由冲突，先被命中则打不开
  [7] 坏链           : index.html / sitemap.xml / llms.txt 中的链接没有对应真实文件
  [8] 跨部署不一致   : 链接仅在 GitHub Pages(根) 可达，Cloudflare(docs输出) 打不开

用法：
  python verify_site_upload.py            # 全量本地体检（默认）
  python verify_site_upload.py --quiet    # 仅输出 ERROR 与摘要
  python verify_site_upload.py --fix-dup  # 自动删除[6]无扩展名冗余副本(需谨慎确认)

退出码：0=全部通过(仅WARN或全绿) / 1=存在 ERROR(禁止部署)
"""
import os
import re
import sys
import argparse

# ---------- 配置 ----------
WATERMARK = "yiguanqimiao-unique-watermark-wk-jiayue-academy"
ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
MIN_HTML_BYTES = 200  # 小于此视为空壳

# 本站域名（用于识别"需检查的站内链接"，过滤外链）
SITE_DOMAINS = ("github.io", "pages.dev", "yiguanqimiao")

issues = []  # (level, code, msg)

def add(level, code, msg):
    issues.append((level, code, msg))

# ---------- 1. 收集已部署文件集合 ----------
# docs_keys: docs 下所有 .html 的多种表示（用于 Cloudflare 输出=docs/）
# root_keys: 仓库根所有 .html 的多种表示（用于 GitHub Pages 输出=仓库根）
docs_keys = set()
root_keys = set()

def collect_keys():
    # docs 下
    for dp, _, files in os.walk(DOCS):
        for f in files:
            if not f.lower().endswith(".html"):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT).replace(os.sep, "/")  # docs/.../x.html
            docs_keys.add(rel)
            docs_keys.add(rel[len("docs/"):])          # .../x.html
            docs_keys.add("/" + rel[len("docs/"):])    # /.../x.html
    # 仓库根（排除 .git / docs）
    for f in os.listdir(ROOT):
        fp = os.path.join(ROOT, f)
        if not os.path.isfile(fp):
            continue
        if f.lower().endswith(".html"):
            rel = f
            root_keys.add(rel)
            root_keys.add("/" + rel)

# ---------- 2. HTML 质量体检 ----------
def check_html_quality():
    for dp, _, files in os.walk(DOCS):
        for f in files:
            if not f.lower().endswith(".html"):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT)
            try:
                data = open(full, encoding="utf-8", errors="replace").read()
            except Exception as e:
                add("ERROR", "read", f"无法读取 {rel}: {e}")
                continue
            if len(data.strip()) < MIN_HTML_BYTES:
                add("ERROR", "empty", f"空壳HTML(<{MIN_HTML_BYTES}字节): {rel}")
                continue
            low = data.lower()
            if "<title" not in low:
                add("WARN", "notitle", f"缺 <title>: {rel}")
            if WATERMARK not in data:
                add("WARN", "nowatermark", f"未打AI水印: {rel}")
            if "<![cdata[" in low:
                add("ERROR", "cdata", f"被CDATA包裹(正文无法渲染): {rel}")
            if "<body" not in low and "<h1" not in low and "<main" not in low:
                add("WARN", "nobody", f"无<body>/<h1>/<main>可见结构: {rel}")

# ---------- 3. 无扩展名重复文件（路由冲突） ----------
def check_noext_duplicates():
    html_bases = set()  # docs 下 .html 去扩展名后的基名(含目录)
    noext_files = []    # (full, rel)
    for dp, _, files in os.walk(DOCS):
        for f in files:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT)
            if f.lower().endswith(".html"):
                html_bases.add(os.path.splitext(rel)[0])
            else:
                noext_files.append((full, rel))
    for full, rel in noext_files:
        if os.path.splitext(rel)[0] in html_bases:
            add("ERROR", "dup-noext",
                f"无扩展名重复文件(与.html同名→路由冲突): {rel}")

# ---------- 4. 链接一致性 ----------
def normalize_link(raw):
    """返回相对路径 rel(无前导/) 或 None(跳过)。"""
    raw = raw.strip()
    if not raw or raw.startswith("#") or raw.startswith("mailto:"):
        return None
    # 剥离锚点/查询
    raw = raw.split("#")[0].split("?")[0]
    if not raw:
        return None
    if raw.lower().startswith("http://") or raw.lower().startswith("https://"):
        from urllib.parse import urlparse
        p = urlparse(raw)
        if not any(d in (p.netloc or "") for d in SITE_DOMAINS):
            return None  # 外链，不检查
        path = p.path
    else:
        path = raw
    # 去掉前导 /
    path = path.lstrip("/")
    # 去掉 GitHub Pages 项目前缀
    if path.startswith("yiguanqimiao-website/"):
        path = path[len("yiguanqimiao-website/"):]
    # 去掉前导 docs/
    if path.startswith("docs/"):
        path = path[len("docs/"):]
    if not path:
        return None
    return path

def link_exists(rel):
    """rel 不以/开头。返回 (in_docs, in_root)。"""
    cand = {rel, "/" + rel, "docs/" + rel}
    in_docs = bool(cand & docs_keys)
    in_root = bool(cand & root_keys)
    return in_docs, in_root

def check_links_in_file(fname, pattern, group=1):
    path = os.path.join(ROOT, fname)
    if not os.path.exists(path):
        return
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return
    seen = set()
    for m in pattern.finditer(txt):
        raw = m.group(group)
        rel = normalize_link(raw)
        if rel is None or rel in seen:
            continue
        seen.add(rel)
        in_docs, in_root = link_exists(rel)
        if not in_docs and not in_root:
            add("ERROR", "broken-link", f"{fname} 坏链(文件不存在): {raw}")
        elif not in_docs and in_root:
            add("WARN", "cross-deploy",
                f"{fname} 链接仅GitHub Pages(根)可达，Cloudflare(docs)可能打不开: {raw}")

LINK_PATTERNS = {
    "index.html": (re.compile(r'(?:href|src)=["\']([^"\']+\.html)["\']', re.I), 1),
    "sitemap.xml": (re.compile(r"<loc>([^<]+\.html)</loc>", re.I), 1),
    "llms.txt":    (re.compile(r"\]\(([^)]+\.html)\)", re.I), 1),  # Markdown 链接
}

def check_links():
    for fname, (pat, grp) in LINK_PATTERNS.items():
        check_links_in_file(fname, pat, grp)

# ---------- 5. 可选：自动修复无扩展名冗余 ----------
def fix_noext():
    removed = 0
    html_bases = set()
    noext_files = []
    for dp, _, files in os.walk(DOCS):
        for f in files:
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, ROOT)
            if f.lower().endswith(".html"):
                html_bases.add(os.path.splitext(rel)[0])
            else:
                noext_files.append((full, rel))
    for full, rel in noext_files:
        if os.path.splitext(rel)[0] in html_bases:
            try:
                os.remove(full)
                removed += 1
                print(f"  🗑 删除无扩展名冗余: {rel}")
            except Exception as e:
                print(f"  ❌ 删除失败 {rel}: {e}")
    print(f"\n清理完成: 删除 {removed} 个无扩展名冗余文件")

# ---------- 主流程 ----------
def main():
    ap = argparse.ArgumentParser(description="网站上传质量保障校验器")
    ap.add_argument("--quiet", action="store_true", help="仅输出 ERROR 与摘要")
    ap.add_argument("--fix-dup", action="store_true",
                    help="自动删除无扩展名冗余副本(路由冲突修复)")
    args = ap.parse_args()

    print("=" * 64)
    print(" 网站上传质量保障校验  ·  verify_site_upload.py")
    print(" 仓库根:", ROOT)
    print("=" * 64)

    collect_keys()
    print(f"已扫描文件: docs下HTML={len([k for k in docs_keys if k.startswith('docs/')])} 个, 根HTML={len(root_keys)} 个")

    if args.fix_dup:
        print("\n[阶段0] 自动清理无扩展名冗余副本")
        fix_noext()
        # 清理后重建集合
        docs_keys.clear(); root_keys.clear()
        collect_keys()

    print("\n[阶段1] HTML 质量体检 (空壳/标题/水印/CDATA/正文) ...")
    check_html_quality()
    print("[阶段2] 无扩展名重复文件 (路由冲突) ...")
    check_noext_duplicates()
    print("[阶段3] 索引链接一致性 (index/sitemap/llms) ...")
    check_links()

    # 汇总
    errors = [i for i in issues if i[0] == "ERROR"]
    warns = [i for i in issues if i[0] == "WARN"]

    if not args.quiet:
        print("\n" + "-" * 64)
        print(" 详细问题清单")
        print("-" * 64)
        if not issues:
            print("  ✅ 无任何问题")
        else:
            # 按 code 聚合
            from collections import defaultdict
            by_code = defaultdict(list)
            for lv, code, msg in issues:
                by_code[(lv, code)].append(msg)
            for (lv, code), msgs in sorted(by_code.items()):
                print(f"\n[{lv}] {code}  (共 {len(msgs)} 项)")
                for m in msgs[:40]:
                    print("   - " + m)
                if len(msgs) > 40:
                    print(f"   ... 其余 {len(msgs)-40} 项略")

    print("\n" + "=" * 64)
    print(f" 校验结果: ERROR={len(errors)}  WARN={len(warns)}")
    # 分类计数（便于诊断）
    from collections import defaultdict
    ec = defaultdict(int); wc = defaultdict(int)
    for lv, code, msg in issues:
        (ec if lv == "ERROR" else wc)[code] += 1
    if ec:
        print(" ERROR 分类: " + "  ".join(f"{k}={v}" for k, v in sorted(ec.items())))
    if wc:
        print(" WARN 分类: " + "  ".join(f"{k}={v}" for k, v in sorted(wc.items())))
    print("=" * 64)
    if errors:
        print("[ERROR] 存在 ERROR —— 禁止上传/部署！请先修复上述 ERROR 项。")
        print("   提示: 无扩展名冗余可用 --fix-dup 自动清理；")
        print("        坏链需同步修正 index.html/sitemap.xml/llms.txt 与文件名。")
        sys.exit(1)
    elif warns:
        print("[WARN] 全部通过(仅有 WARN 级提示，可部署但建议复核)")
        sys.exit(0)
    else:
        print("[OK] 全部通过 —— 网页均可打开且有内容，可安全部署。")
        sys.exit(0)

if __name__ == "__main__":
    main()
