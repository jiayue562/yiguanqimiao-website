/* Pages Function：企业文化填写内容 · 知识库评估
 * POST /api/culture-check
 *   { schema:"culture_check_v1", exampleId:"01-1-1", text:"用户填写内容" }
 *
 * 硬纪律（对齐用户要求）：
 *  - 唯一知识源 = 《生生》+《企业文化顶层设计》两本书编译的知识包（_culture/kb.js）
 *  - 无依据明确拒答，绝不调用生成模型（杜绝编造书外结论）
 *  - 每条判断带 [book:书名/章节] 出处；模型输出经校验与出处兜底
 *  - 不落库任何填写/评估原文；复用 _advisor/model.js 的多级降级（GLM→Workers AI）
 */
import { validateInput } from "./_culture/validate.js";
import { retrieve, hasEvidence } from "./_culture/retrieve.js";
import { buildMessages, validateAnswer, fallbackAnswer, DISCLAIMER, REFUSAL, PERSONA, EXAMPLE_CRITERIA } from "./_culture/prompt.js";
import { checkRate, cacheKey, getCache, setCache, bumpCounter } from "./_culture/rate.js";
import { generate } from "./_advisor/model.js";
import { META } from "./_culture/kb.js";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(obj, status) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "Cache-Control": "no-store", ...CORS },
  });
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

    // 唯一知识源检索：当前示例锚点 + 用户填写内容
    const result = retrieve(input.text, input.exampleId, 6);
    if (!hasEvidence(result)) {
      await bumpCounter(env, "refused");
      return json({
        ok: true, answer: REFUSAL, refused: true, evidenced: false,
        sources: [], example: (EXAMPLE_CRITERIA[input.exampleId] || {}).name || "",
        disclaimer: DISCLAIMER, kbVersion: META.kb_version,
      }, 200);
    }

    const ck = cacheKey(input);
    const cached = await getCache(env, ck);
    if (cached && cached.answer) {
      await bumpCounter(env, "cached");
      return json({ ...cached, cached: true, kbVersion: META.kb_version }, 200);
    }

    const messages = buildMessages(result, input.text, input.exampleId);
    let gen = await generate(env, messages, { maxTokens: 1100, temperature: 0.3 });
    let answer = gen.text;
    let check = validateAnswer(answer, hasEvidence(result));

    if (!check.ok && check.reason !== "too_short") {
      const hint = "\n（请严格遵守：只用给定书稿原文，无依据就说明无法判断；每条标 [book:书名/章节]，分符合之处／不符合之处及依据／改写建议三部分。）";
      gen = await generate(env, buildMessages({ chunks: result.chunks }, input.text + hint, input.exampleId), { maxTokens: 1100, temperature: 0.35 });
      answer = gen.text;
      check = validateAnswer(answer, hasEvidence(result));
    }
    if (!check.ok || !answer) {
      await bumpCounter(env, "fallback");
      return json({
        ok: true, answer: fallbackAnswer(result), degraded: true, evidenced: true,
        model: "deterministic-fallback", reason: check.reason || "no_output",
        sources: result.chunks.map(c => ({ book: c.book, section: c.section })),
        example: (EXAMPLE_CRITERIA[input.exampleId] || {}).name || "",
        disclaimer: DISCLAIMER, kbVersion: META.kb_version,
      }, 200);
    }

    let finalAnswer = String(answer).trim();
    if (!/\[book:/.test(finalAnswer)) {
      const srcs = result.chunks.slice(0, 3).map(c => `[book:${c.book}/${c.section}]`);
      if (srcs.length) finalAnswer += "\n\n【依据】" + srcs.join("；") + "。";
    }

    const out = {
      ok: true, answer: finalAnswer, refused: false, evidenced: true, cached: false, degraded: false,
      model: gen.model, tier: gen.tier,
      sources: result.chunks.map(c => ({ book: c.book, section: c.section })),
      example: (EXAMPLE_CRITERIA[input.exampleId] || {}).name || "",
      persona: PERSONA, disclaimer: DISCLAIMER, kbVersion: META.kb_version,
    };
    await setCache(env, ck, out);
    await bumpCounter(env, "answered");
    return json(out, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error", detail: String(e && e.message || e).slice(0, 100), disclaimer: DISCLAIMER }, 500);
  }
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
