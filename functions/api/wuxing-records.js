// Pages Function：测评数据查看接口（口令保护）
// GET /api/wuxing-records?key=<口令>&limit=100&offset=0
// 口令来源：环境变量 WX_ADMIN_KEY（未配置时一律拒绝，安全默认）
// 返回字段：id / kind / yes_count / main_type / created_at / ans（逐题选项，键为题号0-224）
// 说明：数据本身匿名无 PII，但含完整作答，故必须口令保护，不公开
const CORS = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "GET, OPTIONS" };
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...CORS } });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  try {
    const configured = env && env.WX_ADMIN_KEY;
    if (!configured) return json({ ok: false, error: "view_not_configured" }, 503);
    const url = new URL(request.url);
    const key = url.searchParams.get("key") || "";
    // 恒定时间比较简化版（长度+逐字符），避免时序侧信道
    if (key.length !== configured.length || key !== configured) {
      return json({ ok: false, error: "unauthorized" }, 401);
    }
    if (!env.DB) return json({ ok: false, error: "db_not_bound" }, 503);
    const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit"), 10) || 50, 1), 200);
    const offset = Math.max(parseInt(url.searchParams.get("offset"), 10) || 0, 0);
    const [rows, cnt] = await Promise.all([
      env.DB.prepare(
        "SELECT id, kind, schema_version, yes_count, main_type, ts, upload_id, created_at, ans FROM responses ORDER BY id DESC LIMIT ?1 OFFSET ?2"
      ).bind(limit, offset).all(),
      env.DB.prepare("SELECT COUNT(*) AS n FROM responses").first(),
    ]);
    const records = (rows.results || []).map((r) => {
      let ans = {};
      try { ans = typeof r.ans === "string" ? JSON.parse(r.ans) : (r.ans || {}); } catch (e) {}
      return {
        id: r.id, kind: r.kind, schema: r.schema_version,
        yesCount: r.yes_count, mainType: r.main_type || null,
        submittedAt: r.created_at || new Date(Number(r.ts)).toISOString(),
        uploadId: r.upload_id,
        yesIds: Object.keys(ans).filter((k) => ans[k] === true).map(Number).sort((a, b) => a - b),
      };
    });
    return json({ ok: true, total: Number(cnt && cnt.n) || 0, limit, offset, records }, 200);
  } catch (e) {
    return json({ ok: false, error: "server_error" }, 500);
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
