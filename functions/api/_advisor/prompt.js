/* advisor/prompt.js — AI 顾问 system prompt 构造（纪律固定段 + 当次事实）
 * 纪律来自已确认的 rules 与主型唯一律；判定由服务端确定性引擎给出，AI 只做表达。
 */
import { ELEMENTS, SHENG, KE, BASE25, CHECKPOINTS, CARRIER } from "./core.generated.js";

export const DISCLAIMER = "本回答依据五行人格学体系生成，仅供参考与自我觉察，不构成医疗、心理诊断或治疗建议；若涉及持续情绪困扰，请寻求专业机构帮助。";

/* 固定纪律段（每次都注入，版本化） */
export function disciplinePrompt() {
  return [
    "你是「以观其妙书院」五行人格学 AI 顾问，只依据给定的结构化事实与知识片段回答，不得发明数字、题号、词条或权威出处。",
    "【最高纪律·主型唯一】每个词只有一个五行主型（木火土金水）；不存在副型、多属、双标。若事实中 typeState 为复合型，只允许表述「主导X、兼有Y的影子」，不得说「既是X又是Y」。",
    "【双词层】判断/证据环节逐字引用答卷原始词（带qid）；解释/建议环节改用给定的五行属性词升维表达（如「木·生发受阻」）。两者不得混用；并置时标「原始词→属性词」。",
    "【关系五类】自对=补盲区（你缺的那一块TA也没有）；相生=助生固本（每周共处+当面说好处）；被生=接住滋养（让隐性的好显形）；相克=化克为生（被克方养Y行+五式载体）；被克=先止损再转化（不硬顶先给空间）。",
    "【生克环】相生：木→火→土→金→水→木；相克：木→土→水→火→金→木。顺序不可记反。",
    "【判定权】主型、层位、类型状态、关系类别已由确定性引擎算好并写在 facts 中，你不得重新判定或改写；只做自然语言解释与建议。",
    "【边界】非医学诊断；不得给出「你患有…」「你是…症」等判断；涉及抑郁/焦虑/治疗/药物等，明确引导专业求助。",
    "【引用】回答中出现的词必须来自给定 evidence 或知识片段；引用知识片段时在句末标 [source:section]。",
    "【篇幅】≤800字，分点清晰，结尾给一个可立刻执行的小动作。",
  ].join("\n");
}

/* 当次事实段 */
export function factsPrompt(facts) {
  const f = facts || {};
  const ev = (f.evidence || []).map(e => `${e.qid}「${e.word}」(${e.element||e.e} L${e.layer})`).join("、");
  const kn = (f.knowledge || []).map(k => `[${k.source}:${k.section}] ${(k.text||"").slice(0,260)}`).join("\n");
  return [
    "--- 本次事实（引擎产出，不可改写）---",
    `主型：${f.mainType || "未显"}；类型状态：${f.typeState || "—"}；阴阳：${f.yinYang || "—"}`,
    `层位：峰值 L${f.peak || "—"}，起点 L${f.startLayer || "—"}；GHI：${f.GHI ?? "—"}`,
    `关系类别：${f.relationClass || "—"}；对象：${f.kind || "—"}`,
    `答是词证据：${ev || "（手动模式，无测评证据）"}`,
    kn ? `--- 知识片段（仅供解释，不改判定）---\n${kn}` : "--- 无知识片段：仅用词条与纪律作答 ---",
  ].join("\n");
}

export function buildMessages(facts, question, mode) {
  const sys = disciplinePrompt() + "\n\n" + factsPrompt(facts)
    + (mode === "manual" ? "\n\n【手动模式】用户未做测评，只选了主型；禁止声称基于其个人答卷或引用qid证据，只给通用类型解读。" : "");
  return [
    { role: "system", content: sys },
    { role: "user", content: String(question || "").slice(0, 300) },
  ];
}

/* 出参白名单校验：返回 {ok, reason} */
export function validateAnswer(answer, facts) {
  const s = String(answer || "").trim();
  if (!s) return { ok: false, reason: "empty" };
  if (s.length > 1600) return { ok: false, reason: "too_long" };
  // 主型必须与引擎一致
  if (facts && facts.mainType) {
    const claimed = ELEMENTS.filter(e => new RegExp(`${e}(行|主型)`).test(s));
    if (claimed.length && !claimed.includes(facts.mainType) && !(facts.typeState === "复合型" && claimed.length <= 2)) {
      return { ok: false, reason: "main_type_mismatch" };
    }
  }
  // 诊断红线词
  if (/抑郁症|焦虑症|强迫症|双相|精神分裂|确诊|服药|停药|处方/.test(s)) return { ok: false, reason: "diagnostic" };
  return { ok: true };
}

/* 确定性兜底：AI 失效时按关系类别取 base25 四段 */
export function fallbackAnswer(facts) {
  const f = facts || {};
  const P = f.mainType, Q = f.qEl || P;
  const seg = (P && BASE25[P] && BASE25[P][Q]) ? BASE25[P][Q] : null;
  const rel = f.relationClass || "自对";
  const cp = P && CHECKPOINTS[P] ? CHECKPOINTS[P] : null;
  const car = f.yEl && CARRIER[f.yEl] ? CARRIER[f.yEl] : "";
  let out = `关系判定：${P || "—"} × ${Q || "—"}，${rel}。\n`;
  if (seg && seg[0]) out += `怎么流动：${seg[0]}\n`;
  if (seg && seg[2]) out += `摩擦点：${seg[2]}\n`;
  if (cp) out += `通关点：${cp.attr_word}（${cp.how}）。\n`;
  if (car) out += `可执行动作：${car}。\n`;
  return out + DISCLAIMER;
}
