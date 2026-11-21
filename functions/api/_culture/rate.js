/* _culture/rate.js — 限流 + 缓存 + 计数（KV 可选，缺失静默降级）
 * 不存任何填写/评估原文；只存计数与哈希 key。
 */
const WINDOW_MS = 3600 * 1000;
const LIMIT = 12;
const CACHE_TTL = 86400;

async function safeGet(env, k) {
  try { return env.ADVISOR_KV ? await env.ADVISOR_KV.get(k, "json") : null; } catch (e) { return null; }
}
async function safePut(env, k, v, ttl) {
  try { if (env.ADVISOR_KV) await env.ADVISOR_KV.put(k, JSON.stringify(v), { expirationTtl: ttl }); } catch (e) {}
}

export async function checkRate(env, ip) {
  const k = "culture:rate:" + ip;
  const rec = await safeGet(env, k) || { t: [] };
  const now = Date.now();
  rec.t = (rec.t || []).filter(x => now - x < WINDOW_MS);
  if (rec.t.length >= LIMIT) return { ok: false, retryAfter: Math.ceil((rec.t[0] + WINDOW_MS - now) / 1000) };
  rec.t.push(now);
  await safePut(env, k, rec, 3600);
  return { ok: true };
}
export function cacheKey(input) {
  const base = [String(input.text || "").trim().toLowerCase().replace(/\s+/g, ""), input.exampleId || ""].join("|");
  let h = 0;
  for (let i = 0; i < base.length; i++) { h = ((h << 5) - h + base.charCodeAt(i)) | 0; }
  return "culture:cache:" + (h >>> 0).toString(36);
}
export async function getCache(env, k) { return safeGet(env, k); }
export async function setCache(env, k, v) { return safePut(env, k, v, CACHE_TTL); }
export async function bumpCounter(env, field) {
  const k = "culture:stat:" + new Date().toISOString().slice(0, 10);
  const s = await safeGet(env, k) || {};
  s[field] = (s[field] || 0) + 1;
  await safePut(env, k, s, 86400 * 7);
}
