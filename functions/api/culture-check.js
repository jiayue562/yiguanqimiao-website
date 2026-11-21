/* Pages Function：企业文化填写内容 · 知识库评估
 * POST /api/culture-check
 *   { schema:"culture_check_v1", exampleId:"01-1-1", text:"用户填写内容" }
 *
 * 该接口只做入口治理（校验 / 限流 / 缓存 / 计数 / 响应包装）；
 * 所有问答逻辑交给 _culture/agent.js 后台智能体统一编排：
 *   词条定义 → 限定知识库检索 → GLM 优先 → 质量门禁 → 网站既有兜底链 → 结果归一
 *
 * 硬纪律（对齐用户要求）：
 *  - 唯一知识源 = 《生生》+《企业文化顶层设计》两本书编译的知识包（_culture/kb.js）
 *  - 无依据明确拒答，绝不调用生成模型（杜绝编造书外结论）
 *  - 回答带 [book:书名/章节] 出处；模型输出经质量门禁与服务端补依据
 *  - 不落库任何填写/评估原文；缓存只存哈希 key 与脱敏结果
 */
import { validateInput } from "./_culture/validate.js";
import { runCultureAgent, resolveTerm } from "./_culture/agent.js";
import { DISCLAIMER } from "./_culture/prompt.js";
import { checkRate, cacheKey, getCache, setCache, bumpCounter } from "./_culture/rate.js";
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

    // 缓存键纳入词条定义，注册表升级后旧答案不会串味
    const term = resolveTerm(input.exampleId);
    const ck = cacheKey({ ...input, definition: term ? term.definition : "" });
    const cached = await getCache(env, ck);
    if (cached && cached.answer) {
      await bumpCounter(env, "cached");
      return json({ ...cached, cached: true, kbVersion: META.kb_version }, 200);
    }

    const out = await runCultureAgent(input, env);
    if (!out.ok) return json(out, 400);

    const final = { ...out, cached: false };
    await setCache(env, ck, final);
    await bumpCounter(env, out.refused ? "refused" : out.switched ? "switched" : "answered");
    return json(final, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error", detail: String(e && e.message || e).slice(0, 100), disclaimer: DISCLAIMER }, 500);
  }
}

export function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
