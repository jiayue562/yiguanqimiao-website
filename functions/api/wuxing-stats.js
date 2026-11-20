// Pages Function：测评统计接口
// GET /api/wuxing-stats → { ok:true, total:N, byKind:{self:N,other:N}, lastAt:ISO }
// 统计口径：responses 表全部提交次数 count(*)，与 D1 实际行数一致
// DB 未绑定时返回 total:0 且不报错，前端显示 0，不影响测评流程
const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};
function json(obj, status) {
  return new Response(JSON.stringify(obj), { status, headers: { "content-type": "application/json", ...CORS } });
}

export async function onRequestGet(context) {
  const { env } = context;
  try {
    if (!env || !env.DB) return json({ ok: true, total: 0, byKind: { self: 0, other: 0 }, lastAt: null }, 200);
    const [totalRow, byKind, lastRow] = await Promise.all([
      env.DB.prepare("SELECT COUNT(*) AS n FROM responses").first(),
      env.DB.prepare("SELECT kind, COUNT(*) AS n FROM responses GROUP BY kind").all(),
      env.DB.prepare("SELECT MAX(created_at) AS last FROM responses").first(),
    ]);
    const byKindObj = { self: 0, other: 0 };
    for (const r of (byKind.results || [])) {
      if (r.kind === "self" || r.kind === "other") byKindObj[r.kind] = Number(r.n) || 0;
    }
    return json({
      ok: true,
      total: Number(totalRow && totalRow.n) || 0,
      byKind: byKindObj,
      lastAt: (lastRow && lastRow.last) || null,
    }, 200);
  } catch (e) {
    // 统计失败不阻塞页面：回退 0，前端照常显示
    return json({ ok: true, total: 0, byKind: { self: 0, other: 0 }, lastAt: null, degraded: true }, 200);
  }
}

export async function onRequestOptions() {
  return new Response(null, { status: 204, headers: CORS });
}
