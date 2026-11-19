/* Pages Function：顾问管理端（口令保护，只看计数不看文本）
 * GET /api/advisor-admin?key=<WX_ADMIN_KEY>
 */
import { META } from "./_advisor/core.generated.js";
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, OPTIONS" };
function json(o, s) { return new Response(JSON.stringify(o), { status: s, headers: { "content-type": "application/json; charset=utf-8", ...CORS } }); }

export async function onRequestGet(context) {
  const { request, env } = context;
  const configured = env && env.WX_ADMIN_KEY;
  if (!configured) return json({ ok: false, error: "view_not_configured" }, 503);
  const key = new URL(request.url).searchParams.get("key") || "";
  if (key.length !== configured.length || key !== configured) return json({ ok: false, error: "unauthorized" }, 401);
  const days = [];
  for (let i = 0; i < 7; i++) {
    const d = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
    let s = {};
    try { if (env.ADVISOR_KV) s = await env.ADVISOR_KV.get("advisor:stat:" + d, "json") || {}; } catch (e) {}
    days.push({ date: d, answered: s.answered || 0, cached: s.cached || 0, fallback: s.fallback || 0 });
  }
  return json({ ok: true, ruleVersion: META.hash.reportText, builtAt: META.builtAt, days,
    note: "仅统计计数，不存储任何提问或回答原文" }, 200);
}
export async function onRequestOptions() { return new Response(null, { status: 204, headers: CORS }); }
