/* model.js — 多级模型适配器：任何一个模型挂了，顾客都不会看到"不可用"
 * 降级链（按序）：GLM-4.7-Flash → GLM-4-Flash-250414 → GLM-Z1-Flash → Workers AI → 确定性兜底
 * 设计：
 *  1. 免费模型优先（GLM），失败即自动降级，不暴露错误给顾客
 *  2. KV 记录"冷静期"：某模型失败后隔 10 分钟再试，避免每次请求都白等超时
 *  3. 成功即缓存"当前可用模型"，下次直达；全链失败仍有确定性兜底
 *  4. API key 走 env.GLM_API_KEY（Cloudflare secret），绝不写入代码
 */

const GLM_ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/chat/completions";
const FREE_MODELS = [
  "glm-4.7-flash",        // 免费·200K·延续 4.7 基座（首选）
  "glm-4-flash-250414",   // 免费·128K·高速
  "glm-4.5-flash",        // 免费·128K·备胎
];
const COOLDOWN_MS = 10 * 60 * 1000;
const HF_MODEL = "@cf/meta/llama-3.1-8b-instruct-fp8";

/* 读 KV 熔断记录：返回被临时拉黑的模型集合 */
async function cooldowns(env) {
  if (!env.ADVISOR_KV) return new Set();
  try { return new Set(await env.ADVISOR_KV.get("advisor:model:down", "json") || []); }
  catch (e) { return new Set(); }
}
async function markDown(env, model) {
  if (!env.ADVISOR_KV) return;
  try {
    const list = await env.ADVISOR_KV.get("advisor:model:down", "json") || [];
    if (!list.find(x => x.m === model)) list.push({ m: model, t: Date.now() });
    await env.ADVISOR_KV.put("advisor:model:down", JSON.stringify(list.filter(x => Date.now() - x.t < COOLDOWN_MS)), { expirationTtl: 700 });
  } catch (e) {}
}
async function getPreferred(env) {
  if (!env.ADVISOR_KV) return null;
  try { return await env.ADVISOR_KV.get("advisor:model:preferred"); } catch (e) { return null; }
}
async function setPreferred(env, model) {
  if (!env.ADVISOR_KV) return;
  try { await env.ADVISOR_KV.put("advisor:model:preferred", model, { expirationTtl: 3600 }); } catch (e) {}
}

/* 单次调用 GLM（OpenAI 兼容协议） */
async function callGLM(env, model, messages, maxTokens, temperature) {
  const key = env.GLM_API_KEY;
  if (!key) throw new Error("no_glm_key");
  const ctl = new AbortController();
  const timer = setTimeout(() => ctl.abort(), 25000); // 25 秒超时，绝不让顾客等太久
  try {
    const resp = await fetch(GLM_ENDPOINT, {
      method: "POST", signal: ctl.signal,
      headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({ model, messages, max_tokens: maxTokens, temperature, stream: false }),
    });
    if (!resp.ok) {
      const txt = (await resp.text()).slice(0, 120);
      throw new Error("glm_http_" + resp.status + ":" + txt);
    }
    const j = await resp.json();
    const content = j && j.choices && j.choices[0] && j.choices[0].message && j.choices[0].message.content;
    if (!content) throw new Error("glm_empty");
    return { text: content, model };
  } finally { clearTimeout(timer); }
}

/* 单次调用 Workers AI（保底，永远在） */
async function callWorkersAI(env, messages, maxTokens, temperature) {
  if (!env.AI) throw new Error("no_ai_binding");
  const model = env.AI_MODEL || HF_MODEL;
  const r = await env.AI.run(model, { messages, max_tokens: maxTokens, temperature });
  const text = r && (r.response || r.result || "");
  if (!text) throw new Error("ai_empty");
  return { text, model };
}

/* 主入口：按降级链依次尝试，返回 {text, model, tier, tried[]}
 * tier: "glm" | "workers-ai" | "fallback"（由调用方用确定性兜底）
 */
export async function generate(env, messages, opts) {
  const maxTokens = (opts && opts.maxTokens) || 1100;
  const temperature = (opts && opts.temperature != null) ? opts.temperature : 0.35;
  const tried = [];
  const down = await cooldowns(env);
  const pref = await getPreferred(env);

  // 有 key 才排 GLM；上次成功的模型置顶，其它保持优先级
  const glmList = env.GLM_API_KEY
    ? [...FREE_MODELS].sort((a, b) => (a === pref ? -1 : b === pref ? 1 : 0))
    : [];

  for (const model of glmList) {
    if (down.has(model)) { tried.push(model + ":cooldown"); continue; }
    try {
      const r = await callGLM(env, model, messages, maxTokens, temperature);
      await setPreferred(env, model);
      return { ...r, tier: "glm", tried };
    } catch (e) {
      tried.push(model + ":" + String(e.message || e).slice(0, 60));
      await markDown(env, model); // 失败即冷静 10 分钟，下次请求不重复踩坑
    }
  }

  // GLM 全线失败/未配置 → Workers AI 保底
  try {
    const r = await callWorkersAI(env, messages, maxTokens, temperature);
    return { ...r, tier: "workers-ai", tried };
  } catch (e) {
    tried.push("workers-ai:" + String(e.message || e).slice(0, 60));
  }

  // 全链失败 → 交给调用方确定性兜底（永远有回答）
  return { text: null, model: null, tier: "fallback", tried };
}

/* 供管理端查看当前模型状态（不暴露 key） */
export async function modelStatus(env) {
  const down = [...(await cooldowns(env))];
  return {
    glmConfigured: !!env.GLM_API_KEY,
    workersAIConfigured: !!env.AI,
    preferred: await getPreferred(env),
    cooldown: down,
    chain: [...FREE_MODELS, "workers-ai", "deterministic-fallback"],
  };
}
