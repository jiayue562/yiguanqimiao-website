/* Pages Function：《满愿与圆满之道》随书 AI 助理
 * POST /api/manyuan-advisor
 *   { schema:"manyuan_assistant_v1", question, selectedText?, currentAnchor?, historyDigest?[], sid? }
 *
 * 硬纪律：唯一知识源 = 本书正文检索结果；无依据明确拒答；不编造；不存问答原文。
 * 复用工程骨架：_advisor/model.js 的多级降级（GLM→Workers AI），KV 可选静默降级。
 */
import { validateInput } from "./_manyuan/validate.js";
import { retrieve, hasEvidence } from "./_manyuan/retrieve.js";
import { buildMessages, validateAnswer, fallbackAnswer, DISCLAIMER, REFUSAL } from "./_manyuan/prompt.js";
import { checkRate, cacheKey, getCache, setCache, bumpCounter } from "./_manyuan/rate.js";
import { generate } from "./_advisor/model.js";
import { META } from "./_manyuan/kb.js";

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

    // 检索：唯一知识源 = 本书正文
    const result = retrieve(input.question, input.selectedText, input.currentAnchor, 6);
    const evidenced = hasEvidence(result);

    // 【无依据硬门禁】检索不到就明确拒答，绝不调用生成模型（杜绝编造）
    if (!evidenced) {
      await bumpCounter(env, "refused");
      return json({
        ok: true, answer: REFUSAL, refused: true, evidenced: false,
        sources: [], disclaimer: DISCLAIMER, kbVersion: META.kb_version,
      }, 200);
    }

    const ck = cacheKey(input);
    const cached = await getCache(env, ck);
    if (cached && cached.answer) {
      await bumpCounter(env, "cached");
      return json({ ...cached, cached: true, kbVersion: META.kb_version }, 200);
    }

    const messages = buildMessages(result, input.question, input.selectedText, input.historyDigest);
    let gen = await generate(env, messages, { maxTokens: 900, temperature: 0.3 });
    let answer = gen.text;
    let check = validateAnswer(answer, evidenced);

    // 一次扩写/纠偏重试
    if (!check.ok && check.reason !== "diagnostic") {
      const hint = "\n（请严格遵守：只依据必读语料，无依据就说明无法回答；用原句加解释，标 [book:章节]，150-600 字。）";
      gen = await generate(env, buildMessages(result, input.question + hint, input.selectedText, input.historyDigest), { maxTokens: 900, temperature: 0.35 });
      answer = gen.text;
      check = validateAnswer(answer, evidenced);
    }

    // 全链失败 -> 确定性兜底（摘原句/或无依据拒答），顾客永远有回答
    if (!check.ok || !answer) {
      await bumpCounter(env, "fallback");
      return json({
        ok: true, answer: fallbackAnswer(result), degraded: true, evidenced: true,
        model: "deterministic-fallback", reason: check.reason || "no_output",
        sources: result.chunks.map(c => c.section), disclaimer: DISCLAIMER, kbVersion: META.kb_version,
      }, 200);
    }

    let finalAnswer = String(answer).trim();
    // 出处兜底：模型漏标时服务端补真实章节
    if (!/\[book:/.test(finalAnswer)) {
      const secs = result.chunks.slice(0, 3).map(c => c.section);
      if (secs.length) finalAnswer += "\n\n【依据章节】" + secs.join("；") + "。";
    }

    const out = {
      ok: true, answer: finalAnswer, refused: false, evidenced: true,
      model: gen.model, tier: gen.tier, cached: false, degraded: false,
      sources: result.chunks.map(c => c.section),
      disclaimer: DISCLAIMER, kbVersion: META.kb_version,
    };
    await setCache(env, ck, out);
    await bumpCounter(env, "answered");
    return json(out, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error", detail: String(e && e.message || e).slice(0, 100), disclaimer: DISCLAIMER }, 500);
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
