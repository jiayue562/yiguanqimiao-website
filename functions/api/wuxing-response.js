// Pages Function：测评作答匿名上传接口
// POST /api/wuxing-response  { kind, schema, ans, ts, uid, mainType? }
// 设计：匿名无 PII；严格校验；upload_id 幂等去重；DB 未绑定时返回 503 不影响前端
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...CORS } });
}
function bad(msg) { return json({ ok: false, error: msg }, 400); }

export async function onRequestPost(context) {
  const { request, env } = context;
  try {
    if (!env || !env.DB) return json({ ok: false, error: "db_not_bound" }, 503);
    const body = await request.json();
    const kind = body.kind === "other" ? "other" : "self";
    const schema = body.schema === "wxq_v1" ? "wxq_v1" : "wxr_v1";
    const ans = body.ans;
    if (!ans || typeof ans !== "object" || Array.isArray(ans)) return bad("ans_required");
    const keys = Object.keys(ans);
    if (keys.length === 0 || keys.length > 300) return bad("ans_size");
    for (const k of keys) {
      const n = Number(k);
      if (!Number.isInteger(n) || n < 0 || n > 299) return bad("ans_index");
      if (ans[k] !== true && ans[k] !== false) return bad("ans_value");
    }
    const yesCount = Object.values(ans).filter((v) => v === true).length;
    const ts = Number.isFinite(Number(body.ts)) ? Math.floor(Number(body.ts)) : Date.now();
    const uid = typeof body.uid === "string" && /^[a-f0-9-]{8,64}$/i.test(body.uid) ? body.uid : null;
    if (!uid) return bad("uid_required");
    const mainType = typeof body.mainType === "string" && /^[木火土金水]$/.test(body.mainType) ? body.mainType : null;
    await env.DB.prepare(
      "INSERT INTO responses (kind, schema_version, ans, yes_count, main_type, ts, upload_id) VALUES (?1,?2,?3,?4,?5,?6,?7) ON CONFLICT(upload_id) DO NOTHING"
    ).bind(kind, schema, JSON.stringify(ans), yesCount, mainType, ts, uid).run();
    return json({ ok: true }, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error" }, 500);
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
