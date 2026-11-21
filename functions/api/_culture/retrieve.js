/* _culture/retrieve.js — 限定知识源检索：《生生》+《企业文化顶层设计》
 * 唯一知识源 = _culture/kb.js 的 CHUNKS；命中块带 [book:章节] 出处；不引入任何外部知识。
 * 领域无关骨架沿用 manyuan；锚点词表 = 企业文化域（取自两书真实术语）。
 */
import { CHUNKS, TERMS } from "./kb.js";
import { EXAMPLE_ANCHORS } from "./registry.js";

/* 从用户填写内容中提取检索词：术语表优先 + 中文 2-4 字滑窗 */
function extractKeywords(text, limit) {
  const s = String(text || "").replace(/[，。！？、；：""''《》（）()\s,.!?~…＝=×·]/g, " ");
  const words = new Set();
  for (const t of TERMS) if (t && s.indexOf(t) >= 0) words.add(t);
  const STOP = new Set(["什么", "怎么", "为什么", "可以", "这个", "那个", "我们", "你们", "他们",
    "应该", "需要", "必须", "是否", "正确", "符合", "不是", "就是", "这样", "那样", "通过", "进行"]);
  const han = s.match(/[\u4e00-\u9fff]{2,}/g) || [];
  for (const seg of han) {
    for (let L = 4; L >= 2; L--) {
      for (let i = 0; i + L <= seg.length; i++) {
        const w = seg.slice(i, i + L);
        if (!STOP.has(w)) words.add(w);
      }
    }
  }
  return Array.from(words).slice(0, limit || 28);
}

/* 词条锚点统一在 registry.js；锚点只排序、不充当证据。 */

const GENERIC = new Set(["怎么样", "什么样", "为什么", "是什么", "怎么办", "哪些", "如何",
  "正确", "符合", "应该", "需要", "这样", "那样", "通过", "进行", "我们", "他们", "这个"]);
function isEvidenceWord(kw) {
  if (GENERIC.has(kw)) return false;
  if (TERMS.indexOf(kw) >= 0) return true;
  return kw.length >= 3;
}
function scoreChunk(chunk, kws) {
  const text = chunk.text || "", sec = chunk.section || "";
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

/* 证据判定：只看用户填写内容本身的词；锚点词不得充当证据（否则任何内容都有依据） */
function evidenceHit(chunk, kws) {
  const text = chunk.text || "", sec = chunk.section || "";
  let hit = 0;
  for (const kw of kws) {
    const strong = TERMS.indexOf(kw) >= 0 || kw.length >= 4; // 术语或≥4字实词才算证据
    if (!strong || GENERIC.has(kw)) continue;
    if (text.indexOf(kw) >= 0 || sec.indexOf(kw) >= 0) hit++;
  }
  return hit;
}

/* 主检索：question=用户填写内容；exampleId=当前示例（可选）
 * 锚点词只提升排序分；hit（是否有依据）只由用户填写内容决定。 */
export function retrieve(question, exampleId, limit) {
  const qKws = extractKeywords(question, 24);
  const anchors = (exampleId && EXAMPLE_ANCHORS[exampleId]) || [];
  const scoreKws = Array.from(new Set([...anchors, ...qKws, ...qKws]));
  if (!scoreKws.length) return { chunks: [], hit: 0, keywords: [] };

  const scored = [];
  for (const c of CHUNKS) {
    const { score } = scoreChunk(c, scoreKws);
    const ev = evidenceHit(c, qKws);
    const srcBoost = c.source === "生生" ? 2 : 0;
    const final = score + srcBoost;
    if (score > 0) scored.push({ c, score: final, hit: ev });
  }
  scored.sort((a, b) => b.score - a.score || b.hit - a.hit || a.c.i - b.c.i);

  const top = scored.slice(0, limit || 6).map(x => ({
    source: "book", book: x.c.source, section: x.c.section, anchor: x.c.anchor,
    text: x.c.text, score: x.score,
  }));
  return { chunks: top, hit: scored.reduce((a, x) => a + x.hit, 0), keywords: scoreKws.slice(0, 14) };
}

export function hasEvidence(result) {
  return !!(result && result.chunks && result.chunks.length && result.hit >= 2);
}
