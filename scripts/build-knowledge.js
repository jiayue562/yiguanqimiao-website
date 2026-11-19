/* build-knowledge.js — P2 构建期编译三源语料→D1 knowledge 表 SQL
 * 源：llms-full.txt（LLM全量）/ wuxing/rel/knowledge.js（225词条）/ scripts/.build/book.md（书稿）
 * 输出：scripts/.build/knowledge.sql + stats
 * 切块：按标题/段落，每块 400-800 字，重叠 50 字；tag_el/tag_xiang 自动标注
 * 纯 Node，不依赖 WorkBuddy
 */
const fs = require("fs"), path = require("path"), crypto = require("crypto"), vm = require("vm");
const REPO = __dirname + "/..";
const BUILD = path.join(__dirname, ".build");
const OUT = path.join(BUILD, "knowledge.sql");
function hash(b) { return crypto.createHash("sha256").update(b).digest("hex").slice(0, 16); }
function esc(s) { return "'" + String(s).replace(/'/g, "''") + "'"; }

const ELS = ["木", "火", "土", "金", "水"];
const XIANGS = {
  木: ["曲直","生发","舒畅腾上","调达柔和","内在成长"],
  火: ["炎上","明亮","炽烈","发散","迅疾"],
  土: ["承载","适应","容纳","运化","稳定"],
  金: ["坚固","收敛","锋利","光洁","变革"],
  水: ["润下","通透","沉潜","静藏","养物"]
};
function detectTags(text) {
  const found = { el: null, xiang: null };
  for (const [e, xs] of Object.entries(XIANGS)) {
    for (const x of xs) {
      if (text.includes(x)) { if (!found.el) { found.el = e; found.xiang = x; } return found; }
    }
  }
  for (const e of ELS) if (text.includes(e + "行") || text.includes(e + "曰")) { found.el = e; break; }
  return found;
}
function chunk(text, section, source, srcHash, minLen = 400, maxLen = 800, overlap = 50) {
  const paras = text.split(/\n{2,}/).map(s => s.trim()).filter(Boolean);
  const out = []; let cur = "", sec = section;
  for (const para of paras) {
    const hm = para.match(/^(#{1,4})\s+(.+)$/);
    if (hm) { sec = (section ? section + " > " : "") + hm[2]; continue; }
    if ((cur + para).length > maxLen && cur.length >= minLen) {
      out.push({ section: sec, text: cur.slice(0, maxLen) });
      cur = cur.slice(-overlap) + "\n" + para;
    } else {
      cur += (cur ? "\n" : "") + para;
    }
  }
  if (cur.length >= 40) out.push({ section: sec, text: cur.slice(0, maxLen) });
  return out;
}

const rows = [];
let id = 0;
const sources = [];
/* 1) llms-full.txt — HTML 标签流，按 <h1/h2> 分篇、去标签后切块 */
const fullPath = path.join(REPO, "llms-full.txt");
if (fs.existsSync(fullPath)) {
  const buf = fs.readFileSync(fullPath);
  let raw = buf.toString("utf8")
    .replace(/<(script|style|code)[\s\S]*?<\/\1>/gi, " ")
    .replace(/<\/?(h[1-6]|p|div|li|blockquote|tr|section|article|br)[^>]*>/gi, "\n") // 块级标签→换行
    .replace(/<[^>]+>/g, " ")            // 去其余 HTML 标签
    .replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/[ \t]+/g, " ");
  const h = hash(buf);
  // 该语料标题在清洗后丢失 markdown # 标记；用固定窗口滑切（检索用，section 记偏移）
  const clean = raw.replace(/\n{2,}/g, "\n").trim();
  const chunks = [];
  const WIN = 700, STEP = 650;
  for (let pos = 0; pos < clean.length; pos += STEP) {
    const piece = clean.slice(pos, pos + WIN).trim();
    if (piece.length >= 40) chunks.push({ section: `offset:${pos}`, text: piece });
  }
  chunks.forEach(c => { const t = detectTags(c.text); rows.push({ id: ++id, source: "llms-full", section: c.section.slice(0, 120), tag_el: t.el, tag_xiang: t.xiang, text: c.text }); });
  sources.push(`llms-full: ${chunks.length} chunks`);
}
/* 2) knowledge.js 225词条 */
const kjPath = path.join(REPO, "wuxing/rel/knowledge.js");
if (fs.existsSync(kjPath)) {
  const buf = fs.readFileSync(kjPath); const h = hash(buf);
  const kctx = { window: {} }; vm.createContext(kctx);
  vm.runInContext(buf.toString("utf8"), kctx);
  const words = (kctx.window.WXKB && kctx.window.WXKB.words) || {};
  let n = 0;
  for (const [word, val] of Object.entries(words)) {
    const d = val.d || "", f = val.f || "";
    if (!d && !f) continue;
    const text = `【${word}】${d}${f ? "｜辨析：" + f : ""}`;
    const t = detectTags(word + d);
    rows.push({ id: ++id, source: "knowledge-js", section: word, tag_el: t.el, tag_xiang: t.xiang, text });
    n++;
  }
  sources.push(`knowledge.js: ${n} 词条`);
}
/* 3) book.md */
const bookPath = path.join(BUILD, "book.md");
if (fs.existsSync(bookPath)) {
  const buf = fs.readFileSync(bookPath); const h = hash(buf);
  const text = buf.toString("utf8");
  const chunks = chunk(text, "", "book", h);
  chunks.forEach(c => { const t = detectTags(c.text); rows.push({ id: ++id, source: "book", section: c.section.slice(0, 120), tag_el: t.el, tag_xiang: t.xiang, text: c.text }); });
  sources.push(`book: ${chunks.length} chunks`);
}

const lines = ["-- knowledge 表由 build-knowledge.js 自动生成，勿手改",
  "CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, source TEXT NOT NULL, section TEXT, tag_el TEXT, tag_xiang TEXT, chunk_text TEXT NOT NULL, char_len INTEGER NOT NULL, src_hash TEXT NOT NULL);",
  "DELETE FROM knowledge;"];
rows.forEach(r => lines.push(`INSERT INTO knowledge (id,source,section,tag_el,tag_xiang,chunk_text,char_len,src_hash) VALUES (${r.id},${esc(r.source)},${esc(r.section)},${r.tag_el ? esc(r.tag_el) : "NULL"},${r.tag_xiang ? esc(r.tag_xiang) : "NULL"},${esc(r.text)},${r.text.length},${esc(sourceHash(r.source))});`));
function sourceHash(s) {
  const p = s === "llms-full" ? fullPath : s === "knowledge-js" ? kjPath : bookPath;
  return fs.existsSync(p) ? hash(fs.readFileSync(p)) : "NA";
}
fs.writeFileSync(OUT, lines.join("\n") + "\n", "utf8");
const sized = rows.filter(r => r.text.length >= 40 && r.text.length <= 850).length;
console.log("KNOWLEDGE BUILT:", rows.length, "rows, sized OK:", sized, "->", OUT);
console.log(sources.join(" | "));
