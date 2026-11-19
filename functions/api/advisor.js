/* Pages Function：五行人格 AI 顾问
 * POST /api/advisor  {schema:"wxr_advisor_v1", mode:"report|manual", kind, yesIds, mainType, question}
 * 判定由服务端确定性引擎重算；AI 只做表达；不落库任何提问/回答原文。
 */
import { validateInput, buildFacts, qidOf } from "./_advisor/validate.js";
import { buildMessages, validateAnswer, fallbackAnswer, DISCLAIMER } from "./_advisor/prompt.js";
import { checkRate, cacheKey, getCache, setCache, bumpCounter } from "./_advisor/rate.js";
import { META } from "./_advisor/core.generated.js";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json; charset=utf-8", ...CORS } });
}

/* D1 检索：书稿原文优先，词条仅作词级证据（2026-11-20 重写） */
async function retrieve(env, facts, question) {
  if (!env.DB_LEX) return [];
  const out = [], seen = new Set();
  const push = r => { const k = r.source + "|" + r.section; if (!seen.has(k)) { seen.add(k); out.push({ source: r.source, section: r.section, text: r.chunk_text, tag_el: r.tag_el, tag_xiang: r.tag_xiang }); } };

  // 词条证据：按 qid 取原始词（判断层用）——同时这些词是书稿检索的最佳锚点
  if (!facts.manual && facts.evidence.length) {
    const ids = facts.evidence.slice(0, 6).map(e => e.qid);
    for (const qid of ids) {
      try {
        const r = await env.DB_LEX.prepare("SELECT qid,raw_word,element,xiang,layer FROM raw_words WHERE qid=?1").bind(qid).first();
        if (r) { const ev = facts.evidence.find(x => x.qid === qid); if (ev) { ev.word = r.raw_word; ev.element = r.element; ev.layer = r.layer; ev.xiang = r.xiang; } }
      } catch (e) {}
    }
  }

  // 检索锚点：答是词原文（傲慢孤僻/抗上不服）→ 书稿对这些词有专章；手动模式回退主型象维
  const anchors = (facts.evidence || []).map(e => e.word).filter(Boolean).slice(0, 6);
  if (!anchors.length && facts.mainType) {
    const XIANG = { 木:["曲直","生发","独","顶","傲"], 火:["炎上","明亮","发散","急"], 土:["承载","容纳","稳定","忍"], 金:["收敛","坚固","标准","锋利"], 水:["润下","通透","沉潜","藏"] };
    anchors.push(...(XIANG[facts.mainType] || [facts.mainType]));
  }
  const qWords = [];
  for (const x of ["顶","忍","边界","成长","承载","标准","退让","表达","冲突","关系","孤僻","不服","傲"]) if (question && question.includes(x)) qWords.push(x);
  const kws = [...anchors, ...qWords];

  // ① 书稿优先：锚点命中 book 正文
  for (const kw of kws.slice(0, 5)) {
    try {
      const rs = await env.DB_LEX.prepare(
        "SELECT source,section,chunk_text,tag_el,tag_xiang FROM knowledge WHERE source='book' AND chunk_text LIKE ?1 ORDER BY char_len ASC LIMIT 2"
      ).bind("%" + kw + "%").all();
      (rs.results || []).forEach(push);
    } catch (e) {}
  }
  // ② llms-full 补 1-2 块
  for (const kw of [...(facts.evidence || []).map(e => e.xiang).filter(Boolean), facts.mainType].filter(Boolean).slice(0, 2)) {
    try {
      const rs = await env.DB_LEX.prepare(
        "SELECT source,section,chunk_text,tag_el,tag_xiang FROM knowledge WHERE source='llms-full' AND chunk_text LIKE ?1 ORDER BY char_len ASC LIMIT 1"
      ).bind("%" + kw + "%").all();
      (rs.results || []).forEach(push);
    } catch (e) {}
  }
  // ③ 词条兜底：仅 2 条，且书稿不足时才补
  if (out.filter(x => x.source === "book").length < 2) {
    for (const kw of kws.slice(0, 3)) {
      try {
        const rs = await env.DB_LEX.prepare(
          "SELECT source,section,chunk_text,tag_el,tag_xiang FROM knowledge WHERE source='knowledge-js' AND (section LIKE ?1 OR chunk_text LIKE ?1) LIMIT 1"
        ).bind("%" + kw + "%").all();
        (rs.results || []).forEach(push);
      } catch (e) {}
    }
  }
  const rank = { book: 0, "llms-full": 1, "knowledge-js": 2 };
  return out.sort((a, b) => (rank[a.source] ?? 9) - (rank[b.source] ?? 9)).slice(0, 8);
}

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    const body = await request.json();
    const input = validateInput(body);
    if (!input.ok) return json({ ok: false, error: input.error, disclaimer: DISCLAIMER }, 400);

    const ip = request.headers.get("CF-Connecting-IP") || request.headers.get("x-forwarded-for") || "unknown";
    const rate = await checkRate(env, ip);
    if (!rate.ok) return json({ ok: false, error: "rate_limited", retryAfter: rate.retryAfter, disclaimer: DISCLAIMER }, 429);

    let ai = null, aiErr = null; // 提前声明：无AI兜底分支(L91)也要引用
    const facts = buildFacts(input, body.qEl || null);
    const ck = cacheKey(facts, input.question);
    const cached = await getCache(env, ck);
    if (cached && cached.answer) {
      await bumpCounter(env, "cached");
      return json({ ...cached, cached: true, ruleVersion: META.hash.reportText }, 200);
    }

    const knowledge = await retrieve(env, facts, input.question);
    facts.knowledge = knowledge;

    // 无 AI 绑定 → 确定性兜底（不报错）
    if (!env.AI) {
      const answer = fallbackAnswer(facts);
      const res = { ok: true, answer, facts, disclaimer: DISCLAIMER, model: "deterministic-fallback", degraded: true, aiErr, hasAI: !!env.AI, hasDB: !!env.DB_LEX, ruleVersion: META.hash.reportText };
      await bumpCounter(env, "fallback");
      return json(res, 200);
    }

    const model = env.AI_MODEL || "@cf/meta/llama-3.1-8b-instruct-fp8";
    const messages = buildMessages(facts, input.question, input.mode);
    try {
      ai = await env.AI.run(model, { messages, max_tokens: 1100, temperature: 0.35 });
    } catch (e) { ai = null; aiErr = String(e && e.message || e).slice(0, 200); }

    let answer = ai && (ai.response || ai.result || "");
    let check = validateAnswer(answer, facts);
    if (!check.ok) {
      // 纠正重试一次：字数不足则明确要求扩写并多引用书稿片段
      const hint = check.reason === "too_short"
        ? "\n（上一条太短了。请扩写到 300 字以上：多引用上方必读书稿的原文句子，讲透机制、给具体场景，分 3–4 点展开。）"
        : "\n（请严格遵守：只用给定事实与片段，不作诊断，主型不得改写。）";
      try {
        const retry = buildMessages(facts, input.question + hint, input.mode);
        ai = await env.AI.run(model, { messages: retry, max_tokens: 1100, temperature: 0.4 });
        answer = ai && (ai.response || ai.result || "");
        check = validateAnswer(answer, facts);
      } catch (e) { check = { ok: false, reason: "retry_failed" }; }
    }
    if (!check.ok) {
      await bumpCounter(env, "fallback");
      const res = { ok: true, answer: fallbackAnswer(facts), facts, disclaimer: DISCLAIMER,
        model: "deterministic-fallback", degraded: true, reason: check.reason, aiErr, hasAI: !!env.AI, hasDB: !!env.DB_LEX, ruleVersion: META.hash.reportText };
      return json(res, 200);
    }

    const out = { ok: true, answer: String(answer).trim(), facts, disclaimer: DISCLAIMER,
      model, cached: false, degraded: false, ruleVersion: META.hash.reportText };
    await setCache(env, ck, out);
    await bumpCounter(env, "answered");
    return json(out, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error", disclaimer: DISCLAIMER }, 500);
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
