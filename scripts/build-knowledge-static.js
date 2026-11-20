/* build-knowledge-static.js — 把三源语料编译成随站发布的静态知识包
 * 输出：wuxing/rel/knowledge-pack.js（window.WXKNOW），供 advisor 无 D1 时使用
 * 只取带五行tag的块 + 全量词条，控制体积
 */
const fs = require("fs"), path = require("path");
const REPO = __dirname + "/..";
const BUILD = path.join(__dirname, ".build");
const OUTS = [path.join(REPO, "wuxing/rel/knowledge-pack.js"), path.join(REPO, "docs/wuxing/rel/knowledge-pack.js")];
const sql = fs.readFileSync(path.join(BUILD, "knowledge.sql"), "utf8");

/* 从 SQL 解析 INSERT（构建期一次性，格式由 build-knowledge.js 固定） */
function unesc(s) { return s.replace(/''/g, "'"); }
const re = /INSERT INTO knowledge \(id,source,section,tag_el,tag_xiang,chunk_text,char_len,src_hash\) VALUES \((\d+),'([^']*)','([^']*)',(NULL|'[^']*'),(NULL|'[^']*'),'((?:[^']|'')*)',(\d+),'([^']*)'\);/g;
const items = []; let m;
while ((m = re.exec(sql))) {
  items.push({ id: +m[1], source: m[2], section: unesc(m[3]),
    tag_el: m[4] === "NULL" ? null : unesc(m[4].slice(1, -1)),
    tag_xiang: m[5] === "NULL" ? null : unesc(m[5].slice(1, -1)),
    text: unesc(m[6]) });
}
/* 保留：全部词条 + 带五行tag的块（限每源前600条控体积） */
const keep = items.filter(x => x.source === "knowledge-js" || x.tag_el);
const byEl = {};
keep.forEach(x => { const e = x.tag_el || "通用"; (byEl[e] = byEl[e] || []).push({ s: x.section, t: x.text.slice(0, 500), src: x.source }); });
for (const e of Object.keys(byEl)) byEl[e] = byEl[e].slice(0, 300);

const payload = { meta: { n: keep.length, byEl: Object.fromEntries(Object.entries(byEl).map(([k,v])=>[k,v.length])), note: "构建期编译，随站发布，零D1依赖" }, byEl };
const js = "/* 五行知识包 · 构建期生成勿手改 */\nwindow.WXKNOW = " + JSON.stringify(payload) + ";\n";
OUTS.forEach(p => { fs.writeFileSync(p, js, "utf8"); console.log("WROTE", p, Math.round(js.length/1024) + "KB"); });
