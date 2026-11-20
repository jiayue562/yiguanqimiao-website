/* manyuan/validate.js — 入参校验（A/B 档手动模式：无测评判定、无 yesIds） */
export const SCHEMA = "manyuan_assistant_v1";

export function validateInput(body) {
  if (!body || body.schema !== SCHEMA) return { ok: false, error: "bad_schema" };
  const q = String(body.question || "").trim();
  if (q.length < 1 || q.length > 300) return { ok: false, error: "bad_question" };
  const selectedText = String(body.selectedText || "").slice(0, 400);
  const currentAnchor = String(body.currentAnchor || "").slice(0, 40);
  // 追问摘要：最多 12 轮、每轮 ≤40 字，只接受字符串数组（不存逐字原文）
  let historyDigest = [];
  if (Array.isArray(body.historyDigest)) {
    historyDigest = body.historyDigest
      .filter(x => typeof x === "string")
      .slice(-12)
      .map(x => x.slice(0, 40));
  }
  return { ok: true, question: q, selectedText, currentAnchor, historyDigest };
}

/* 会话摘要 key（前端生成 sid；服务端不存逐字） */
export function sessionKey(body) {
  return String((body && body.sid) || "anon").slice(0, 40);
}
