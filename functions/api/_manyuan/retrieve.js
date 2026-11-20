/* manyuan/retrieve.js — 关键词锚点检索（领域无关骨架，术语表为本书数据）
 * 静态知识包检索：问题词 + 章节词 + 选中段落词 -> 命中块 -> 相关性排序 -> 配额兜底。
 * 只从本书 CHUNKS 取，绝不引入外部知识。检索结果带 [book:章节] 出处。
 */
import { CHUNKS, TERMS } from "./kb.js";

/* 从问题/选中段落中提取检索词：中文 2-4 字词组 + 命中术语表 */
function extractKeywords(text, limit) {
  const s = String(text || "").replace(/[，。！？、；：""''《》（）()\s,.!?~…]/g, " ");
  const words = new Set();
  // 术语表命中（优先，带权重）
  for (const t of TERMS) {
    if (t && s.indexOf(t) >= 0) words.add(t);
  }
  // 2-4 字中文滑窗（过滤纯通用词）
  const STOP = new Set(["什么", "怎么", "为什么", "可以", "这个", "那个", "我们", "你们", "他们",
    "一个", "是不是", "有没有", "告诉我", "请问", "解释", "意思", "意思呢", "这本书", "书中", "里面"]);
  const han = s.match(/[\u4e00-\u9fff]{2,}/g) || [];
  for (const seg of han) {
    for (let L = 4; L >= 2; L--) {
      for (let i = 0; i + L <= seg.length; i++) {
        const w = seg.slice(i, i + L);
        if (!STOP.has(w)) words.add(w);
      }
    }
  }
  return Array.from(words).slice(0, limit || 24);
}

/* 相关性打分：命中次数 + 标题命中加权 + 位置加权
 * 泛用疑问词与 2 字词会产生假命中，只计分、不计入有效证据 hit。
 * 真正证据 = 命中本书术语表，或长度≥3 且不在疑问黑名单里的实词。
 */
const VALID = new Set(TERMS); // 术语表里的词是本书概念的强证据
const GENERIC = new Set([
  "怎么样", "什么样", "为什么", "是什么", "怎么办", "怎么讲", "什么意思", "哪些", "哪些呢",
  "怎么样呢", "什么意", "怎么办", "如何呢", "是什么", "讲什么", "说什么", "讲呢",
  "天气", "推荐", "今天", "怎么样", "样呢", "一下", "这个", "那个", "我们", "他们",
]);
function isEvidenceWord(kw) {
  if (GENERIC.has(kw)) return false;
  if (VALID.has(kw)) return true;
  return kw.length >= 3;
}
function scoreChunk(chunk, kws) {
  const text = chunk.text || "";
  const sec = chunk.section || "";
  let score = 0, hit = 0;
  for (const kw of kws) {
    const inText = text.indexOf(kw) >= 0;
    const inSec = sec.indexOf(kw) >= 0;
    if (inSec && !GENERIC.has(kw)) { score += 6; hit += 2; }
    if (inText) {
      const c = text.split(kw).length - 1;
      score += Math.min(c, 4) + 1;
      if (isEvidenceWord(kw)) hit++;
    }
  }
  return { score, hit };
}

/* 主检索：返回带出处的命中块（最多 limit 块） */
export function retrieve(question, selectedText, currentAnchor, limit) {
  const qKws = extractKeywords(question, 18);
  const sKws = selectedText ? extractKeywords(selectedText, 12) : [];
  // 选中段落词权重加倍（读者明确指向它）
  const kws = Array.from(new Set([...sKws, ...sKws, ...qKws]));
  if (!kws.length) return { chunks: [], hit: 0, keywords: [] };

  const scored = [];
  for (const c of CHUNKS) {
    const { score, hit } = scoreChunk(c, kws);
    // 当前阅读章节 +2 关联分（围绕当前上下文）
    const contextBoost = (currentAnchor && c.anchor === currentAnchor) ? 3 : 0;
    const final = score + contextBoost;
    if (hit > 0 || contextBoost) scored.push({ c, score: final, hit });
  }
  scored.sort((a, b) => b.score - a.score || b.hit - a.hit || a.c.i - b.c.i);

  const top = scored.slice(0, limit || 6).map(x => ({
    source: "book",
    section: x.c.section,
    anchor: x.c.anchor,
    text: x.c.text,
    score: x.score,
  }));
  const totalHit = scored.reduce((a, x) => a + x.hit, 0);
  return { chunks: top, hit: totalHit, keywords: kws.slice(0, 12) };
}

/* 是否检索到足够依据：无命中则判定为“书中无依据” */
export function hasEvidence(result) {
  return !!(result && result.chunks && result.chunks.length && result.hit >= 2);
}
