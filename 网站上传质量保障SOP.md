# 网站上传质量保障 SOP（经验沉淀 · 2026-07-29）

> 目的：把 2026-07-28 坏链事故的教训固化为可执行的门禁机制，保证**以后每次上传内容，所有网页都能打开且有内容**。

---

## 一、背景：2026-07-28 真实坏链事故

用户反馈首页「AI原生组织·顶层设计全书」与「龙脑OS系列」链接打不开。根因复盘：

1. **文件名改名但链接没改**：10 篇中文文件名被重命名为 ASCII 哈希名，但 `index.html` / `sitemap.xml` / `llms.txt` 仍指向旧中文名 → 坏链（打不开）。
2. **CDATA 包裹正文**：`ai-native-org-complete-book.html` 被 `<![CDATA[...]]>` 包裹 → 浏览器无法渲染正文（打开是空白）。
3. **无扩展名重复文件**：存在与 `.html` 同名的无扩展名文件 → 路由冲突，先被命中则打不开。

事后全量审计虽修复，但**没有沉淀为防护机制**，导致生成脚本继续产出无扩展名冗余、`sitemap.xml` 陈旧脱节（仍引用已不存在的中文路径）。这正是本次要解决的复发问题。

---

## 二、核心原则（铁律）

- **【生成】** 上传内容必须生成 HTML。Cloudflare 输出目录 = `docs/`，仅服务 `.html`；严禁只推 `.md`。
- **【一致】** `index.html` / `sitemap.xml` / `llms.txt` 三者的链接必须与真实文件名**完全一致**；改文件名须同步改三处。
- **【唯一】** 禁止产生与 `.html` 同名的无扩展名文件（路由冲突）。
- **【印记】** 每个 HTML 必须含 AI 水印 `yiguanqimiao-unique-watermark-wk-jiayue-academy`。
- **【门禁】** 每次 push / 部署前**必须**运行 `verify_site_upload.py`，全绿（无 ERROR）才允许。

---

## 三、标准上传流程（每次上传内容必走）

1. **生成 HTML**：把 markdown / 内容转为规范 HTML，输出到 `docs/articles/<栏目>/`（带 `<title>` + 水印 + SEO）。
2. **登记索引**：更新 `index.html`（首页卡片）、`llms.txt`（Markdown 链接）、`sitemap.xml`（`<loc>`）。
3. **跑门禁**：`python verify_site_upload.py`
   - 退出码 `0` = 全绿 / 仅 WARN → 可部署
   - 退出码 `1` = 有 ERROR → **禁止 push**，先修
4. **修复 ERROR**：
   - `dup-noext`（无扩展名冗余）→ `python verify_site_upload.py --fix-dup`（删冗余，先 `git commit` 备份点！）
   - `broken-link`（坏链）→ 修正 index / sitemap / llms 链接或文件名，使其一致
   - `empty` / `cdata` → 重新生成该 HTML
5. **重跑门禁至全绿** → `git commit` + `git push`（Cloudflare Git 集成自动部署）。
6. **部署后抽查**：`https://yiguanqimiao-website.pages.dev/<path>` 应 HTTP 200 且有内容。

---

## 四、校验器说明（verify_site_upload.py）

位于网站仓库根。固化上述所有坑的检查项：

| 检查项 | 说明 | 级别 |
|--------|------|------|
| 空壳 HTML | 文件存在但 <200 字节，打开是空白 | ERROR |
| 缺 `<title>` | 浏览器标签 / SEO 无标题 | WARN |
| 未打 AI 水印 | 知识产权印记缺失 | WARN |
| CDATA 包裹 | 正文被 `<![CDATA[...]]>` 包住，无法渲染 | ERROR |
| 无正文结构 | 无 `<body>`/`<h1>`/`<main>` | WARN |
| 无扩展名副本 | 与 `.html` 同名的无扩展名文件（路由冲突） | ERROR |
| 坏链 | index / sitemap / llms 链接无对应真实文件 | ERROR |
| 跨部署不一致 | 链接仅 GitHub Pages(根) 可达，Cloudflare(docs) 可能打不开 | WARN |

用法：

```bash
python verify_site_upload.py            # 全量体检（详细清单）
python verify_site_upload.py --quiet    # 仅摘要 + 分类计数
python verify_site_upload.py --fix-dup  # 自动删除无扩展名冗余（先 git 提交备份点！）
```

退出码：`0` = 通过（仅 WARN 或全绿）；`1` = 存在 ERROR（禁止部署）。

---

## 五、禁止事项（红线）

- 改文件名不改 index / sitemap / llms 链接
- 用 `<![CDATA[...]]>` 包裹 HTML 正文
- 生成与 `.html` 同名的无扩展名文件
- 推送未跑门禁、或门禁报 ERROR 的内容
- 在 Claw 仓库 `git add -A`（网站是独立仓库 `yiguanqimiao-website`）

---

## 六、当前基线状态（2026-07-29 体检）

- `index.html` 坏链：1；`llms.txt` 坏链：1（用户真实入口基本健康）
- `sitemap.xml`：Jun 12 陈旧产物，引用已不存在的中文路径（含 `data:image` 脏数据），需随上传重生成
- 无扩展名冗余：6711 个（生成脚本复发），需用 `--fix-dup` 清理建立干净基线

> 沉淀结论：**事故不在"一次没修好"，而在"没有门禁"**。把校验器接进每次上传流程，比事后审计更可靠。
