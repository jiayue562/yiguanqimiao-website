/* advisor/validate.js — 入参校验 + 事实构造（判定一律服务端重算） */
import { scoreQuiz, QUIZ_DATA, judgeRelation, ELEMENTS } from "./core.generated.js";

export const SCHEMA = "wxr_advisor_v1";
const ELS = new Set(ELEMENTS);

export function validateInput(body) {
  if (!body || body.schema !== SCHEMA) return { ok: false, error: "bad_schema" };
  const mode = body.mode;
  if (mode !== "report" && mode !== "manual") return { ok: false, error: "bad_mode" };
  const q = String(body.question || "").trim();
  if (q.length < 1 || q.length > 300) return { ok: false, error: "bad_question" };
  if (mode === "report") {
    if (!Array.isArray(body.yesIds)) return { ok: false, error: "yes_ids_required" };
    if (body.yesIds.length > 225) return { ok: false, error: "too_many_ids" };
    for (const id of body.yesIds) if (!Number.isInteger(id) || id < 0 || id > 224) return { ok: false, error: "bad_qid" };
    const kind = body.kind === "other" ? "other" : "self";
    return { ok: true, mode, question: q, kind, yesIds: body.yesIds };
  }
  // manual
  if (!ELS.has(body.mainType)) return { ok: false, error: "bad_main_type" };
  return { ok: true, mode, question: q, mainType: body.mainType };
}

/* 由 yesIds 构造 ans 并服务端重算，产出 facts（不信任客户端任何判定字段） */
export function buildFacts(input, qEl) {
  if (input.mode === "manual") {
    return { kind: "manual", mainType: input.mainType, typeState: "手动模式", yinYang: "—",
      peak: null, startLayer: null, GHI: null, relationClass: judgeRelation(input.mainType, qEl || input.mainType),
      evidence: [], manual: true };
  }
  const ans = {};
  input.yesIds.forEach(i => { ans[i] = true; });
  const res = scoreQuiz(ans, QUIZ_DATA);
  const P = res.mainType || null;
  const Q = qEl || P;
  const evidence = (res.yesWords || []).slice(0, 12).map(w => ({
    qid: "Q" + (w.orig != null ? w.orig : (w.i != null ? w.i : "")),
    word: w.word || w.raw_word || "", element: w.e, layer: w.layer,
  }));
  return {
    kind: input.kind, mainType: P, typeState: res.typeState, yinYang: res.yinYang ? res.yinYang.verdict : "—",
    peak: res.peak, startLayer: res.startLayer, GHI: res.GHI,
    relationClass: P ? judgeRelation(P, Q) : "未显",
    evidence, manual: false,
  };
}

/* qid 还原：data.js 条目无 qid 字段时用下标+1（题库新题号=原始题号，已验证 identity=true） */
export function qidOf(ansIndex) { return "Q" + (ansIndex + 1); }
