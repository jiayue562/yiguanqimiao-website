/* manyuan/prompt.js — 本书 AI 助理 prompt 构造 + 出参校验 + 确定性兜底
 * 领域：绑定《满愿与圆满之道》全书，A/B 档手动模式（无测评判定引擎）。
 * 三条不可退让的底线：只依据本书正文；无依据明确说无法回答；不编造。
 */
export const DISCLAIMER = "本回答依据《满愿与圆满之道》全书正文生成，仅为原文解读与学习参考，不构成任何医疗、心理或投资建议。";

export const REFUSAL = "这本书的正文里没有找到能回答这个问题的依据。为了不误导你，我不能凭空编造。你可以换一个与本书内容相关的问题，或把正在读的那一段原文一并贴出来，我再依据原文为你解释。";

/* 固定纪律段（版本化，每次注入） */
export function disciplinePrompt() {
  return [
    "你是《满愿与圆满之道（全书）》的随书 AI 助理，作者悟空（贾悦），以观其妙书院出品。",
    "【最高纪律·唯一知识源】你只能依据下方「必读语料」中来自本书正文的片段回答。这些片段是本书的完整检索结果。你不可以使用任何本书之外的知识、常识、网络信息或你自己的记忆来补充、联想或发挥。",
    "【无依据必须拒答】如果「必读语料」为空，或其中内容不足以回答读者的问题，你必须直接说明：「这本书的正文里没有找到能回答这个问题的依据，我无法回答」。绝不可以用通用知识、套话或猜测凑出一段看似合理的答案。宁可说无法回答，也不编造。",
    "【结合章节解释】回答时必须引用「必读语料」里的原句，先用原句说明本书怎么讲，再用你自己的话把含义解释清楚；每一处主要解释后用 [book:章节名] 标注出处。出处只能来自给定片段，不得杜撰章节名。",
    "【判定权归原文】本书是实修解读类著作，不含性格测评或量化判定。你不得给出「你是XX型」「你患有XX」之类判定；不得作医疗、心理、投资诊断。涉及健康、治疗、药物等，引导读者寻求专业机构。",
    "【禁用套话】严禁「保持开放、自我反省、有效沟通、调整心态、学习与成长、接纳自己」等放之四海皆准的通用空话。要给本书独有的原句、概念与具体场景。",
    "【文风篇幅】用「你」直说、短句、接地气；篇幅 150–600 字，讲清楚即可，不强求凑长；结尾给一个可当场做的小 action 或一句原文要点。",
    "【多轮追问】若提供「追问上下文」，它是本会话前几轮的简短摘要，用于理解「它/这个/上面」指代，但不得当作新的知识依据——事实依据仍只来自本次「必读语料」。",
  ].join("\n");
}

/* 当次事实段：语料 + 上下文 + 选中段落 */
export function factsPrompt(result, selectedText, historyDigest) {
  const chunks = (result && result.chunks) || [];
  const kn = chunks.map(k => `[book:${k.section}] ${(k.text || "").slice(0, 520)}`).join("\n\n");
  const sel = selectedText ? ("\n--- 读者选中/指向的段落（读者明确要问这段）---\n" + String(selectedText).slice(0, 400)) : "";
  const hist = historyDigest && historyDigest.length
    ? ("\n--- 追问上下文（前几轮摘要，仅供理解指代，非事实依据）---\n" + historyDigest.map((h, i) => `${i + 1}. ${h}`).join("\n"))
    : "";
  return [
    "========== 必读语料（本书正文检索结果·唯一事实依据）==========",
    kn || "（本次未检索到本书正文片段——此时必须按「无依据必须拒答」处理）",
    sel,
    hist,
  ].filter(Boolean).join("\n");
}

export function buildMessages(result, question, selectedText, historyDigest) {
  const sys = disciplinePrompt() + "\n\n" + factsPrompt(result, selectedText, historyDigest);
  return [
    { role: "system", content: sys },
    { role: "user", content: String(question || "").slice(0, 300) },
  ];
}

/* 出参校验：空/超长/拒答合规/诊断红线 */
export function validateAnswer(answer, hasEvidenceFlag) {
  const s = String(answer || "").trim();
  if (!s) return { ok: false, reason: "empty" };
  if (s.length > 2000) return { ok: false, reason: "too_long" };
  if (/抑郁症|焦虑症|强迫症|双相|精神分裂|确诊|服药|停药|处方/.test(s)) return { ok: false, reason: "diagnostic" };
  return { ok: true };
}

/* 确定性兜底：全链失败仍可读；无依据则明确拒答，有依据则摘原句 */
export function fallbackAnswer(result) {
  const chunks = (result && result.chunks) || [];
  if (!chunks.length) return REFUSAL + "\n\n" + DISCLAIMER;
  const c = chunks[0];
  return "这本书里 \u300C" + c.section + "\u300D部分有一段相关原文，先摘录给你：\n\n「"
    + (c.text || "").slice(0, 320) + "」\n\n[book:" + c.section + "]\n\n"
    + "（AI 生成服务暂时不可用，以上为书中原文摘录，请自行参详。）\n\n" + DISCLAIMER;
}
