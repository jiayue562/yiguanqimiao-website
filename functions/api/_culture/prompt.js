/* _culture/prompt.js — 企业文化填写内容评估的提示词与校验
 * 硬纪律：唯一知识源 = 检索到的《生生》《企业文化顶层设计》原文块；无依据拒答；不编造。
 */

export const DISCLAIMER = "本评估仅依据《生生：文化操作系统》与《企业文化顶层设计》两本书的原文，不引入书外结论；判定供参考，最终以共创共识为准。";
export const REFUSAL = "依据《生生》与《企业文化顶层设计》两本书，未检索到与这段填写内容直接相关的判据，因此无法判断其是否符合。请补充更具体的表述，或对照本节的「定义／引导／填写要点」重写后再提交。";

export const PERSONA = "以观其妙书院 · 企业文化知识库评估";

import { EXAMPLE_CRITERIA } from "./registry.js";
export { EXAMPLE_CRITERIA };
/* 67 个词条的统一判据在 registry.js；6 个既有示例保留人工精判据。 */

export function buildMessages(result, userText, exampleId) {
  const crit = (exampleId && EXAMPLE_CRITERIA[exampleId]) || null;
  const evidence = result.chunks.map((c, i) =>
    `【${i + 1}】《${c.book}》· ${c.section}\n${c.text}`
  ).join("\n\n");

  const system = [
    "你是以观其妙书院的企业文化知识库评估员，只负责依据给定书稿原文判断用户填写的内容。",
    "铁律（违反即为失败）：",
    "1. 唯一知识源是下方【必读书稿】。严禁使用任何书外知识、常识、个人观点或推测。",
    "2. 若填写内容在书稿中找不到对应判据，必须明确说「依据两本书无法判断」，不得勉强评价。",
    "3. 每条判断都要标注依据出自哪本书、哪一节，格式 [book:书名/章节]。",
    "4. 不诊断、不评价个人，只评估这段填写内容是否符合本节要求与书稿口径。",
    "5. 用中文，300-600 字，分「符合之处」「不符合之处及依据」「改写建议」三部分。",
    "6. 改写建议中的每一条也必须能追溯到必读书稿，不得凭空发挥。",
  ].join("\n");

  const user = [
    crit ? `【当前示例】${crit.name}\n【本节要求】${crit.requirement}\n` : "",
    "【用户填写的内容】\n" + userText,
    "\n【必读书稿（唯一知识源）】\n" + evidence,
    "\n请按铁律评估：先说符合之处，再逐条指出不符合之处及对应书稿依据，最后给出可追溯的改写建议。",
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

export function fallbackAnswer(result) {
  const secs = (result.chunks || []).slice(0, 3)
    .map(c => `《${c.book}》·${c.section}`).join("；");
  return "模型暂未接通，现按知识库原文给出依据骨架：\n" +
    (result.chunks || []).slice(0, 3).map((c, i) =>
      `[book:${c.book}/${c.section}] ${String(c.text).slice(0, 160)}…`
    ).join("\n\n") +
    (secs ? `\n\n【依据章节】${secs}。` : "");
}
