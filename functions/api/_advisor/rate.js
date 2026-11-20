/* advisor/rate.js — 限流与缓存（KV 可选，未绑定时静默降级不阻塞） */
const WINDOW_MS = 3600 * 1000, LIMIT = 10, CACHE_TTL = 86400;

function keyOf(env, suffix) { return "advisor:" + suffix; }
async function safeGet(env, k) { try { return env.ADVISOR_KV ? await env.ADVISOR_KV.get(k, "json") : null; } catch (e) { return null; } }
async function safePut(env, k, v, ttl) { try { if (env.ADVISOR_KV) await env.ADVISOR_KV.put(k, JSON.stringify(v), { expirationTtl: ttl }); } catch (e) {} }

export async function checkRate(env, ip) {
  const k = keyOf(env, "rate:" + ip);
  const rec = await safeGet(env, k) || { t: [], n: 0 };
  const now = Date.now();
  rec.t = (rec.t || []).filter(x => now - x < WINDOW_MS);
  if (rec.t.length >= LIMIT) return { ok: false, retryAfter: Math.ceil((rec.t[0] + WINDOW_MS - now) / 1000) };
  rec.t.push(now); rec.n = (rec.n || 0) + 1;
  await safePut(env, k, rec, 3600);
  return { ok: true, remaining: LIMIT - rec.t.length };
}

export function cacheKey(facts, question) {
  const base = [
    facts.manual ? "manual" : "report",
    facts.mainType || "", facts.typeState || "", facts.peak || "", facts.startLayer || "", facts.relationClass || "",
    String(question || "").trim().toLowerCase().replace(/\s+/g, ""),
  ].join("|");
  let h = 0; for (let i = 0; i < base.length; i++) { h = ((h << 5) - h + base.charCodeAt(i)) | 0; }
  return keyOf(null, "cache:" + (h >>> 0).toString(36));
}
export async function getCache(env, k) { return safeGet(env, k); }
export async function setCache(env, k, v) { return safePut(env, k, v, CACHE_TTL); }
export async function bumpCounter(env, field) {
  const k = keyOf(env, "stat:" + new Date().toISOString().slice(0, 10));
  const s = await safeGet(env, k) || {};
  s[field] = (s[field] || 0) + 1;
  await safePut(env, k, s, 86400 * 7);
}
