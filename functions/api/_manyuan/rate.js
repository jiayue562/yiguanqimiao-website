/* manyuan/rate.js — 限流 + 缓存 + 计数（KV 可选，缺失静默降级）
 * 遵循 MD 6.4：不存任何提问/回答原文；只存计数与哈希 key。
 */
const WINDOW_MS = 3600 * 1000;
const LIMIT = 12;          // 12 次/小时/IP
const CACHE_TTL = 86400;   // 24h

async function safeGet(env, k) {
  try { return env.ADVISOR_KV ? await env.ADVISOR_KV.get(k, "json") : null; } catch (e) { return null; }
}
async function safePut(env, k, v, ttl) {
  try { if (env.ADVISOR_KV) await env.ADVISOR_KV.put(k, JSON.stringify(v), { expirationTtl: ttl }); } catch (e) {}
}

export async function checkRate(env, ip) {
  const k = "manyuan:rate:" + ip;
  const rec = await safeGet(env, k) || { t: [] };
  const now = Date.now();
  rec.t = (rec.t || []).filter(x => now - x < WINDOW_MS);
  if (rec.t.length >= LIMIT) return { ok: false, retryAfter: Math.ceil((rec.t[0] + WINDOW_MS - now) / 1000) };
  rec.t.push(now);
  await safePut(env, k, rec, 3600);
  return { ok: true };
}

export function cacheKey(input) {
  const base = [
    input.question.trim().toLowerCase().replace(/\s+/g, ""),
    input.currentAnchor || "",
    (input.selectedText || "").slice(0, 80),
  ].join("|");
  let h = 0;
  for (let i = 0; i < base.length; i++) { h = ((h << 5) - h + base.charCodeAt(i)) | 0; }
  return "manyuan:cache:" + (h >>> 0).toString(36);
}
export async function getCache(env, k) { return safeGet(env, k); }
export async function setCache(env, k, v) { return safePut(env, k, v, CACHE_TTL); }
export async function bumpCounter(env, field) {
  const k = "manyuan:stat:" + new Date().toISOString().slice(0, 10);
  const s = await safeGet(env, k) || {};
  s[field] = (s[field] || 0) + 1;
  await safePut(env, k, s, 86400 * 7);
}
