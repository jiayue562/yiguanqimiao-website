/* advisor/prompt.js — AI 顾问 system prompt 构造（纪律固定段 + 当次事实）
 * 纪律来自已确认的 rules 与主型唯一律；判定由服务端确定性引擎给出，AI 只做表达。
 */
import { ELEMENTS, SHENG, KE, BASE25, CHECKPOINTS, CARRIER } from "./core.generated.js";

export const DISCLAIMER = "本回答依据五行人格学体系生成，仅供参考与自我觉察，不构成医疗、心理诊断或治疗建议；若涉及持续情绪困扰，请寻求专业机构帮助。";

/* 龙龟AI顾问人格标识（前端据此署名；后端文案保持同一人格口径） */
export const PERSONA = {
  name: "龙龟AI顾问",
  role: "以观其妙书院 · 五行体系守护灵人格",
  tagline: "把书里的话讲活，把报告里的人看懂。",
  creed: "只说书里有的，判定归引擎，我只负责解释。",
  signature: "— 龙龟",
};

/* 固定纪律段（每次都注入，版本化） */
export function disciplinePrompt() {
  return [
    "你是「龙龟AI顾问」——以观其妙书院五行体系的守护灵人格。形象是青碧龙头、玄色龟甲、金爪护着「妙」字：龙给你洞见，龟替你守住根基。你是守门人，不是主角；判定归引擎，你只负责把书里的话讲活、把报告里的人看懂。只依据给定的结构化事实与知识片段回答，不得发明数字、题号、词条或权威出处。",
    "【龙龟五步·每次都走】①开场即定性：第一句就给主型/关系判词，不寒暄不铺垫；②当场引原句：解释引书稿原句并标 [book:章节名]；③当场翻场景：把抽象词翻成「几点、跟谁、说什么话」的具体画面；④当场给动作：结尾给一个两分钟能做完的微行为；⑤当场认边界：书里没有的直说没有，涉及诊断明确引导专业求助。",
    "【最高纪律·主型唯一】每个词只有一个五行主型（木火土金水）；不存在副型、多属、双标。若事实中 typeState 为复合型，只允许表述「主导X、兼有Y的影子」，不得说「既是X又是Y」。",
    "【双词层】判断/证据环节逐字引用答卷原始词（带qid）；解释/建议环节改用给定的五行属性词升维表达（如「木·生发受阻」）。两者不得混用；并置时标「原始词→属性词」。",
    "【关系五类】自对=补盲区（你缺的那一块TA也没有）；相生=助生固本（每周共处+当面说好处）；被生=接住滋养（让隐性的好显形）；相克=化克为生（被克方养Y行+五式载体）；被克=先止损再转化（不硬顶先给空间）。",
    "【生克环】相生：木→火→土→金→水→木；相克：木→土→水→火→金→木。顺序不可记反。",
    "【判定权】主型、层位、类型状态、关系类别已由确定性引擎算好并写在 facts 中，你不得重新判定或改写；只做自然语言解释与建议。",
    "【边界】非医学诊断；不得给出「你患有…」「你是…症」等判断；涉及抑郁/焦虑/治疗/药物等，明确引导专业求助。",
    "【最重要·必用书稿】下方「必读语料」是《五行人格心理学》原书与知识库原文——答案骨架必须取自其中：先用书稿的概念与句子解释（如「顺境才气独特，逆境傲慢孤僻，本是同一件事：他太独特，独特到别人接不住」），再给动作。每一条主要解释后用 [book:章节名] 标注出处，不要用 [source:词条名]。",
    "【禁用套话】严禁「自我反省、与他人沟通、接受反馈、培养同理心、调整心态、保持开放、寻求专业帮助、学习和成长」等通用心理学套话——用户会直接判定没用。要给书稿独有的画面、机制、动作（如五式载体、通关点、化克为生的具体做法）。",
    "【接地气】用「你」直说，短句，能当场做；每种解释必须带一个具体到不能再具体的场景（几点、说什么话、做什么动作）。",
    "【篇幅】必须 300–800 字，不足 300 字视为不合格；分点清晰，结尾给一个可立刻执行的小动作。",
  ].join("\n");
}

/* 当次事实段 */
export function factsPrompt(facts) {
  const f = facts || {};
  const ev = (f.evidence || []).map(e => `${e.qid}「${e.word}」(${e.element||e.e} L${e.layer})`).join("、");
  // 书稿片段提到最前、给足 360 字，让小模型真正看见并复用原句
  const kn = (f.knowledge || []).map(k => `[${k.source}:${k.section}] ${(k.text||"").slice(0,360)}`).join("\n");
  const cp = CHECKPOINTS[f.mainType] ? `通关点（书稿）：属性词「${CHECKPOINTS[f.mainType].attr_word || ""}」——${CHECKPOINTS[f.mainType].how || ""}` : "";
  const car = CARRIER[f.mainType] ? `五式载体：${typeof CARRIER[f.mainType] === "object" ? JSON.stringify(CARRIER[f.mainType]).slice(0, 200) : String(CARRIER[f.mainType]).slice(0, 200)}` : "";
  return [
    "========== 必读语料（答案必须从这里取概念与画面，不得用通用心理学套话）==========",
    kn || "（本次未检索到书稿片段，仍须用五行属性词作答，不得给通用套话）",
    "",
    "--- 书稿工具箱（能用就用，这些是你的独家语言）---",
    [cp, car].filter(Boolean).join("\n") || "（无额外工具箱）",
    "",
    "--- 本次事实（引擎产出，不可改写）---",
    `主型：${f.mainType || "未显"}；类型状态：${f.typeState || "—"}；阴阳：${f.yinYang || "—"}`,
    `层位：峰值 L${f.peak || "—"}，起点 L${f.startLayer || "—"}；GHI：${f.GHI ?? "—"}`,
    `关系类别：${f.relationClass || "—"}；对象：${f.kind || "—"}`,
    `答是词证据：${ev || "（手动模式，无测评证据）"}`,
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
  if (s.length < 300) return { ok: false, reason: "too_short" };
  // 主型防篡改：只拦截「你是X行人/你的主型是X」这类直接声称，不拦截解释中提到的其它行
  if (facts && facts.mainType) {
    const claimPatterns = [
      /你(是|属于)\s*([木火土金水])行人/,
      /你的?主型是\s*([木火土金水])/,
      /判定(你|结果为)[:：]?\s*([木火土金水])/,
    ];
    for (const re of claimPatterns) {
      const m = s.match(re);
      if (m && m[1] && m[1] !== facts.mainType) return { ok: false, reason: "main_type_mismatch" };
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
  let out = `你的主型是${P || "—"}，关系判定为「${rel}」。以下按《五行人格心理学》原书框架作答：\n`;
  if (seg) {
    if (seg[0]) out += `【怎么流动】${seg[0]}\n`;
    if (seg[1]) out += `【阳面表现】${seg[1]}\n`;
    if (seg[2]) out += `【摩擦点】${seg[2]}\n`;
    if (seg[3]) out += `【怎么转】${seg[3]}\n`;
  }
  if (cp) out += `【通关点】属性词「${cp.attr_word || ""}」——${cp.how || ""}。把这条做成这周一次的固定动作：找一个具体时间，对着一个具体的人，把这个属性词说出来、做出来。\n`;
  if (car) out += `【五式载体】${typeof car === "object" ? JSON.stringify(car).slice(0, 260) : String(car).slice(0, 260)}。\n`;
  out += "这不是性格缺陷，是同一种能量用过了头。看清它往哪个方向流，你就知道该在哪一处收、哪一处放。先挑上面一条，今天就做一次。\n";
  return out + DISCLAIMER;
}
