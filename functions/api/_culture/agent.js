/* _culture/agent.js — 企业文化词条评估智能体
 * 统一支撑 67 个词条页的「填写内容 · 知识库评估」模块。
 *
 * 编排顺序：
 *   1. 词条解析：exampleId → name / definition / requirement（registry.js）
 *   2. 知识库检索：词条定义 + 锚点参与排序，证据只来自用户填写内容
 *   3. GLM 优先：glmOnly 调用，单独做质量门禁
 *   4. 兜底切换：GLM 不可用 / 失败 / 回答不达标 → 网站既有链（Workers AI → 确定性原文兜底）
 *   5. 结果归一：拒答、出处、免责、词条、降级标记统一返回
 *
 * 硬纪律：唯一知识源仍是《生生》+《企业文化顶层设计》；无证据直接拒答；不编造书外结论。
 */
import { EXAMPLE_CRITERIA } from "./registry.js";
import { META } from "./kb.js";
import { retrieve, hasEvidence } from "./retrieve.js";
import { buildMessages, fallbackAnswer, REFUSAL, DISCLAIMER, PERSONA } from "./prompt.js";
import { generate } from "../_advisor/model.js";

/* GLM 回答质量门禁：不达标就切换兜底，不让用户收到"看似有话、实则无用"的回答
 * 达标四要件：① ≥300 字 ② 带 [book:] 出处 ③ 锚定词条 ④ 复述并用词条定义作判断标准
 */
export const MIN_ANSWER_CHARS = 300;
const STRICT_MIN = MIN_ANSWER_CHARS;

function coreName(name) {
  return String(name || "")
    .replace(/^[一二三四五六七八]\s*/, "")
    .replace(/^\d+(?:\.\d+)*\s*/, "")
    .replace(/（[^）]*）/g, "")
    .trim();
}

/* 抽取定义中的关键片段，用于判断模型是否真的把定义当标尺用了。
 * 取定义里连续的 6 个汉字作为指纹；定义过短则退化为整句。 */
function definitionFingerprint(definition) {
  const s = String(definition || "").replace(/\s+/g, "");
  if (!s) return "";
  const m = s.match(/[\u4e00-\u9fa5]{6,}/);
  return m ? m[0].slice(0, 8) : s.slice(0, 8);
}

export function resolveTerm(exampleId) {
  const c = exampleId && EXAMPLE_CRITERIA[exampleId];
  if (!c) return null;
  return {
    id: exampleId,
    name: c.name || "",
    definition: c.definition || "",
    requirement: c.requirement || "",
  };
}

/* GLM 回答质量门禁：不达标就切换兜底，不让用户收到"看似有话、实则无用"的回答 */
export function assessQuality(answer, result, term, opts) {
  const s = String(answer || "").trim();
  if (!s) return { ok: false, reason: "empty" };
  // 确定性兜底走专属校验：必须达到 300 字、带出处、含定义判据与三段结构
  if (opts && opts.allowFallback && /判断骨架|模型暂未接通|原文摘录/.test(s)) {
    if (s.length < STRICT_MIN) return { ok: false, reason: "too_short" };
    if (!/\[book:/.test(s)) return { ok: false, reason: "no_citation" };
    if (!/判断标准|定义/.test(s)) return { ok: false, reason: "definition_not_used_as_criterion" };
    return { ok: true, reason: "deterministic_fallback" };
  }
  if (s.length < STRICT_MIN) return { ok: false, reason: "too_short" };
  if (!/\[book:/.test(s)) return { ok: false, reason: "no_citation" };
  if (/依据两本书无法判断|未检索到.{0,12}判据/.test(s) && hasEvidence(result)) {
    return { ok: false, reason: "refused_with_evidence" };
  }
  const core = coreName(term && term.name);
  if (core && !s.includes(core)) return { ok: false, reason: "term_not_anchored" };
  // 词条定义必须被当作判断标准：答案需出现「定义/判断标准/边界/标尺」等判据词，
  // 且复述定义的关键片段（去重空格后比对），否则视为没按定义判断。
  const hasCriterionWord = /定义|判断标准|判断标尺|划定边界|边界|界定/.test(s);
  const fp = definitionFingerprint(term && term.definition);
  const compact = s.replace(/\s+/g, "");
  const quotesDef = fp ? compact.includes(fp) : false;
  if (!hasCriterionWord || !quotesDef) return { ok: false, reason: "definition_not_used_as_criterion" };
  const parts = ["符合之处", "不符合之处", "改写建议"].filter(x => s.includes(x)).length;
  if (parts < 2) return { ok: false, reason: "missing_structure" };
  if (/作为(?:一个)?(?:AI|人工智能|语言模型)/i.test(s)) return { ok: false, reason: "meta_chatter" };
  return { ok: true, reason: "ok" };
}

function withDisclaimer(answer) {
  const s = String(answer || "").trim();
  return s.includes(DISCLAIMER) ? s : s + "\n\n" + DISCLAIMER;
}

function withCitations(answer, result) {
  let s = String(answer || "").trim();
  if (/\[book:/.test(s)) return s;
  const srcs = (result.chunks || []).slice(0, 3)
    .map(c => `[book:${c.book}/${c.section}]`);
  return srcs.length ? s + "\n\n【依据】" + srcs.join("；") + "。" : s;
}

function baseOut(term, result) {
  return {
    ok: true,
    refused: false,
    evidenced: true,
    example: term ? term.name : "",
    term,
    sources: (result.chunks || []).map(c => ({ book: c.book, section: c.section })),
    persona: PERSONA,
    disclaimer: DISCLAIMER,
    kbVersion: META.kb_version,
  };
}

function refusalOut(term, quality) {
  return {
    ok: true,
    answer: REFUSAL + "\n\n" + DISCLAIMER,
    refused: true,
    evidenced: false,
    degraded: false,
    switched: false,
    model: null,
    tier: "refused",
    tried: [],
    quality,
    example: term ? term.name : "",
    term,
    sources: [],
    persona: PERSONA,
    disclaimer: DISCLAIMER,
    kbVersion: META.kb_version,
  };
}

/* 智能体主入口：返回统一结果对象，不直接返回 Response（由 Pages Function 包装） */
export async function runCultureAgent({ text, exampleId }, env) {
  const term = resolveTerm(exampleId);
  if (!term) return { ok: false, error: "bad_example", disclaimer: DISCLAIMER };

  // 词条定义参与检索排序；证据仍只来自用户填写内容
  const result = retrieve(text, exampleId, 6, {
    extraKws: [term.definition, term.requirement, term.name],
  });
  if (!hasEvidence(result)) {
    return refusalOut(term, { ok: false, reason: "no_evidence" });
  }

  const messages = buildMessages(result, text, exampleId, term);
  const strictMessages = buildMessages(result, text, exampleId, term, { strict: true });
  const tried = [];

  // 第一路：GLM 优先，独立判定，避免"有输出但答非所问"直接进入用户眼前
  let gen = await generate(env, messages, {
    maxTokens: 1800, temperature: 0.3, glmOnly: true,
  });
  tried.push(...(gen.tried || []));
  let quality = assessQuality(gen.text, result, term);
  let switched = false;

  // 第二路：GLM 不可用 / 调用失败 / 回答效果不佳 → 网站既有兜底链
  if (!quality.ok) {
    switched = true;
    gen = await generate(env, strictMessages, {
      maxTokens: 1800, temperature: 0.35, skipGlm: true,
    });
    tried.push(...(gen.tried || []));
    quality = assessQuality(gen.text, result, term, { allowFallback: gen.tier === "fallback" });
  }

  // 最终保底：模型链全断时，用知识库原文摘录，保证稳定且有出处
  if (!gen.text || (!quality.ok && gen.tier !== "fallback")) {
    gen = {
      text: fallbackAnswer(result, term),
      model: "deterministic-fallback",
      tier: "fallback",
      tried: [],
    };
    quality = { ok: true, reason: "deterministic_fallback" };
    switched = true;
  }

  const out = {
    ...baseOut(term, result),
    answer: withDisclaimer(withCitations(gen.text, result)),
    degraded: switched || gen.tier !== "glm",
    switched,
    model: gen.model || null,
    tier: gen.tier,
    tried,
    quality,
  };
  return out;
}
