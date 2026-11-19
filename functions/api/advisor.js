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

/* D1 检索：按主型/象维取知识片段（确定性键，不做运行时 RAG） */
async function retrieve(env, facts, question) {
  if (!env.DB_LEX) return [];
  const els = [];
  if (facts.mainType) els.push(facts.mainType);
  // 从问题里识别其它五行字（最多补一个）
  for (const e of ["木","火","土","金","水"]) {
    if (question.includes(e) && !els.includes(e)) els.push(e);
  }
  const out = [];
  for (const el of els.slice(0, 2)) {
    try {
      const rs = await env.DB_LEX.prepare(
        "SELECT source,section,chunk_text,tag_el,tag_xiang FROM knowledge WHERE tag_el=?1 ORDER BY source='knowledge-js' DESC, id LIMIT 4"
      ).bind(el).all();
      (rs.results || []).forEach(r => out.push({ source: r.source, section: r.section, text: r.chunk_text, tag_el: r.tag_el, tag_xiang: r.tag_xiang }));
    } catch (e) {}
  }
  // 兜底：带标签命中不足时，从问题里抽五行/象维关键词，按正文匹配补书稿/llms-full
  if (out.filter(x => x.source !== "knowledge-js").length < 2) {
    const kws = [];
    for (const e of ["木","火","土","金","水"]) if (question.includes(e)) kws.push(e);
    for (const x of ["顶","忍","边界","成长","承载","标准","退让","表达","冲突","关系"]) if (question.includes(x)) kws.push(x);
    for (const src of ["book", "llms-full"]) {
      for (const kw of kws.slice(0, 3)) {
        try {
          const rs = await env.DB_LEX.prepare(
            "SELECT source,section,chunk_text,tag_el,tag_xiang FROM knowledge WHERE source=?1 AND chunk_text LIKE ?2 ORDER BY char_len DESC LIMIT 2"
          ).bind(src, "%" + kw + "%").all();
          (rs.results || []).forEach(r => { if (!out.some(x => x.source === r.source && x.section === r.section)) out.push({ source: r.source, section: r.section, text: r.chunk_text, tag_el: r.tag_el, tag_xiang: r.tag_xiang }); });
        } catch (e) {}
      }
    }
  }
  // 词条证据：按 qid 精确取原始词（判断层用）
  if (!facts.manual && facts.evidence.length) {
    const ids = facts.evidence.slice(0, 6).map(e => e.qid);
    for (const qid of ids) {
      try {
        const r = await env.DB_LEX.prepare("SELECT qid,raw_word,element,xiang,layer FROM raw_words WHERE qid=?1").bind(qid).first();
        if (r) { const ev = facts.evidence.find(x => x.qid === qid); if (ev) { ev.word = r.raw_word; ev.element = r.element; ev.layer = r.layer; ev.xiang = r.xiang; } }
      } catch (e) {}
    }
  }
  return out.slice(0, 8);
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
    let ai = null, aiErr = null;
    try {
      ai = await env.AI.run(model, { messages, max_tokens: 800, temperature: 0.3 });
    } catch (e) { ai = null; aiErr = String(e && e.message || e).slice(0, 200); }

    let answer = ai && (ai.response || ai.result || "");
    let check = validateAnswer(answer, facts);
    if (!check.ok) {
      // 纠正重试一次：强制纪律段重述
      try {
        const retry = buildMessages(facts, input.question + "\n（请严格遵守：只用给定事实与片段，不作诊断，主型不得改写）", input.mode);
        ai = await env.AI.run(model, { messages: retry, max_tokens: 700, temperature: 0.1 });
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
