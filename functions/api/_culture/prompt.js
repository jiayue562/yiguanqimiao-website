/* _culture/prompt.js — 企业文化填写内容评估的提示词与校验
 * 硬纪律：唯一知识源 = 检索到的《生生》《企业文化顶层设计》原文块；无依据拒答；不编造。
 */

export const DISCLAIMER = "本评估仅依据《生生：文化操作系统》与《企业文化顶层设计》两本书的原文，不引入书外结论；判定供参考，最终以共创共识为准。";
export const REFUSAL = "依据《生生》与《企业文化顶层设计》两本书，未检索到与这段填写内容直接相关的判据，因此无法判断其是否符合。请补充更具体的表述，或对照本节的「定义／引导／填写要点」重写后再提交。";

export const PERSONA = "以观其妙书院 · 企业文化知识库评估";

import { EXAMPLE_CRITERIA } from "./registry.js";
export { EXAMPLE_CRITERIA };
/* 67 个词条的统一判据在 registry.js；6 个既有示例保留人工精判据。 */

export function buildMessages(result, userText, exampleId, term, opts) {
  const crit = (exampleId && EXAMPLE_CRITERIA[exampleId]) || null;
  const evidence = result.chunks.map((c, i) =>
    `【${i + 1}】《${c.book}》· ${c.section}\n${c.text}`
  ).join("\n\n");

  const system = [
    "你是以观其妙书院的企业文化词条评估智能体，接入 GLM 大模型与限定知识库，只负责依据给定书稿原文判断用户填写的内容。",
    "铁律（违反即为失败）：",
    "1. 唯一知识源是下方【必读书稿】。严禁使用任何书外知识、常识、个人观点或推测。",
    "2. 若填写内容在书稿中找不到对应判据，必须明确说「依据两本书无法判断」，不得勉强评价。",
    "3. 每条判断都要标注依据出自哪本书、哪一节，格式 [book:书名/章节]。",
    "4. 不诊断、不评价个人，只评估这段填写内容是否符合当前词条要求与书稿口径。",
    "5. 用中文，回答不少于 300 字（建议 300-600 字），分「符合之处」「不符合之处及依据」「改写建议」三部分；低于 300 字视为不合格。",
    "6. 改写建议中的每一条也必须能追溯到必读书稿，不得凭空发挥。",
    "7. 【词条定义·判断标准】是本次评估的标尺：先用定义划定本词条的边界——凡填写内容溢出定义所界定的范围，即判为「不符合本节词条」，即使其表述本身正确。定义决定「对不对题」，书稿原文决定「内容对不对」。",
    "8. 开头必须先复述词条定义并说明你据以判断的标准，再进入三部分评估。",
  ].join("\n");

  const user = [
    term ? `【当前词条】${term.name}\n【词条定义·判断标准】${term.definition || "（见本节四行体例）"}\n` : "",
    crit ? `【本节要求】${crit.requirement}\n` : "",
    "【用户填写的内容】\n" + userText,
    "\n【必读书稿（唯一知识源）】\n" + evidence,
    opts && opts.strict
      ? "\n请严格遵守：先复述【词条定义·判断标准】作为判据；再用它衡量填写内容是否落在词条边界内；分「符合之处」「不符合之处及依据」「改写建议」三部分，每部分都回扣定义；每条判断标注 [book:书名/章节]；全文不少于 300 字；无依据就明确说无法判断。"
      : "\n请按铁律评估：先复述词条定义并据以划定判断标准，再说符合之处，接着逐条指出不符合之处及对应书稿依据，最后给出可追溯的改写建议；全文不少于 300 字。",
  ].join("\n");

  return [
    { role: "system", content: system },
    { role: "user", content: user },
  ];
}

export function validateAnswer(answer, evidenced) {
  if (!answer || String(answer).trim().length < 60) return { ok: false, reason: "too_short" };
  if (/\[book:/.test(answer)) return { ok: true };
  if (/依据两本书无法判断|未检索到|无法判断/.test(answer)) return { ok: true };
  return { ok: false, reason: "no_citation" };
}

export function fallbackAnswer(result, term) {
  const secs = (result.chunks || []).slice(0, 4)
    .map(c => `《${c.book}》·${c.section}`).join("；");
  const def = term && term.definition ? String(term.definition) : "（见本节四行体例中的定义）";
  const name = term && term.name ? term.name : "本节词条";
  const cites = (result.chunks || []).slice(0, 4).map((c, i) =>
    `[book:${c.book}/${c.section}] ${String(c.text).slice(0, 110)}…`).join("\n");
  return [
    "模型暂未接通，以下按知识库原文与词条定义给出可核查的判断骨架，供你逐条比对。",
    "【词条定义·判断标准】" + name + "：" + def,
    "据以判断：先以上述定义划定本词条的边界——填写内容若溢出定义界定的范围，即使表述正确，也判为不符合本节词条；定义决定「对不对题」，下面的书稿原文决定「内容对不对」。",
    "【符合之处】请对照下方书稿原文，逐句确认你的填写是否落在定义边界内、并与原文口径一致；能对应到原文的，即为可保留部分。",
    "【不符合之处及依据】凡未在下方原文中找到对应判据的表述，或超出定义边界的内容，都不能判定为符合，需按原文口径修正。",
    "【改写建议】把每一条改写都落到下方原文可追溯的表述上，逐条标注 [book:书名/章节]；改写后再次用定义复核是否切题。",
    "【知识库原文摘录】",
    cites,
    secs ? "\n【依据章节】" + secs + "。" : "",
  ].join("\n");
}
