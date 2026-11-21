// 本地验证：词条智能体（定义起点 / GLM 质量门禁 / 兜底切换 / 结果归一）
import { ALLOWED_IDS, EXAMPLE_CRITERIA, EXAMPLE_ANCHORS } from "./functions/api/_culture/registry.js";
import { validateInput } from "./functions/api/_culture/validate.js";
import { retrieve, hasEvidence } from "./functions/api/_culture/retrieve.js";
import { buildMessages, validateAnswer, EXAMPLE_CRITERIA as PROMPT_CRITERIA } from "./functions/api/_culture/prompt.js";
import { resolveTerm, assessQuality, runCultureAgent } from "./functions/api/_culture/agent.js";

const fail = [];
if (Object.keys(PROMPT_CRITERIA || {}).length !== ALLOWED_IDS.length) {
  fail.push("prompt.js does not re-export full criteria registry");
}
const noEvidenceText = "今天天气很好，我想去打篮球和吃披萨，顺便买彩票中奖";
const bookGroundedText = "本企业依据心文化与企业文化建设顶层设计，明确使命、愿景、价值观，区分信息体、能量体与物质体，通过课程体系、讲师体系、培训体系与运营体系实现知行合一。";

// 1. 注册表完整性 + 词条定义 + 白名单 + 提示词起点
for (const id of ALLOWED_IDS) {
  const crit = EXAMPLE_CRITERIA[id];
  if (!crit || !crit.name || !crit.requirement) fail.push(`${id}: missing criteria`);
  if (!crit.definition) fail.push(`${id}: missing definition`);
  if (!EXAMPLE_ANCHORS[id] || !EXAMPLE_ANCHORS[id].length) fail.push(`${id}: missing anchors`);

  const term = resolveTerm(id);
  if (!term || !term.definition) fail.push(`${id}: resolveTerm failed`);

  const v = validateInput({ schema: "culture_check_v1", exampleId: id, text: crit.requirement });
  if (!v.ok) fail.push(`${id}: validate=${v.error}`);

  const msgs = buildMessages({ chunks: [] }, crit.requirement, id, term);
  if (!msgs[0].content.includes("[book:书名/章节]")) fail.push(`${id}: no citation rule`);
  if (!msgs[1].content.includes("词条定义·逻辑起点")) fail.push(`${id}: definition not used as starting point`);
  if (!msgs[1].content.includes(crit.name)) fail.push(`${id}: name missing in prompt`);
}

// 2. 终版词条示例：有书内依据时必须命中（ID 与终版词条表对齐）
const cases = [
  ["01-1-1", "以食载道，传递美好；心文化之根在于信仰为本，道德为尊"],
  ["01-1-6", "成功等于修心乘以性格乘以努力乘以能力，分物质体能量体信息体三个层面"],
  ["02-2-1", "我们的使命是以食载道传递美好，使是责任命是生命，用一生承担的事业"],
  ["04-4-1", "超级符号承载品牌调性与文化基因，企业三色绿色红色白色各有含义"],
  ["05-5-1", "宣誓是员工对职责与使命的承诺，仪式流程精确到主持词，礼乐按场合配曲目"],
  ["06-6-5", "三级荣誉分三级，每条价值观对应奖项，公司级品牌级店面级各有落点"],
];
for (const [id, text] of cases) {
  const r = retrieve(text, id, 6);
  if (!hasEvidence(r)) fail.push(`${id}: known case no evidence hit=${r.hit}`);
}

// 3. 全部 ID：无意义字符串必须拒答（防锚点充当证据）
for (const id of ALLOWED_IDS) {
  const r = retrieve(noEvidenceText, id, 6);
  if (hasEvidence(r)) fail.push(`${id}: nonsense accepted hit=${r.hit}`);
}

// 4. GLM 回答质量门禁：好答案放行，坏答案必须触发兜底
const probeResult = { chunks: [{ book: "生生", section: "卷二", text: "信息体、能量体、物质体三体并建。" }], hit: 3 };
const probeTerm = resolveTerm("01-1-1");
const goodAnswer = "文化观：符合之处是你抓住了心文化之根与本的部分表述。" +
  "不符合之处及依据是未把文化观与信息体、能量体、物质体的关系说清，书稿反复强调三体并建。" +
  "改写建议：先写清本企业信什么，再按物质体、能量体、信息体分别落到行为边界，逐条写清每条信条的释义与可观察行为，避免只留一句口号。[book:生生/卷二]";
if (!assessQuality(goodAnswer, probeResult, probeTerm).ok) fail.push("good answer rejected by quality gate");
for (const [label, bad] of [
  ["empty", ""],
  ["too_short", "文化观符合之处"],
  ["no_citation", "文化观符合之处是你抓住了根本。不符合之处及依据是没有出处。改写建议是重写一遍。"],
  ["term_not_anchored", "这段内容整体符合组织操作系统的口径。不符合之处及依据是没有三体。改写建议是补齐。 [book:生生/卷二]"],
  ["missing_structure", "文化观整体方向正确，但缺少结构。请把内容写得更具体。[book:生生/卷二]"],
]) {
  if (assessQuality(bad, probeResult, probeTerm).ok) fail.push(`bad answer accepted: ${label}`);
}

// 5. 智能体端到端（无模型环境）：拒答路径 + 全链降级路径
const refused = await runCultureAgent({ text: noEvidenceText, exampleId: "01-1-1" }, {});
if (!refused.refused || refused.evidenced || refused.switched) fail.push("agent refusal path invalid");

const degraded = await runCultureAgent({ text: cases[0][1], exampleId: "01-1-1" }, {});
if (!degraded.ok || degraded.refused) fail.push("agent fallback path not answered");
if (!degraded.switched || !degraded.degraded || degraded.tier !== "fallback") fail.push("fallback switch flags invalid");
if (!String(degraded.answer || "").includes("[book:")) fail.push("fallback answer missing citation");
if (!degraded.term || !degraded.term.definition) fail.push("result missing term definition");

// 6. 观察项 + 非法 ID + 出处校验
let grounded = 0;
for (const id of ALLOWED_IDS) {
  const r = retrieve(bookGroundedText, id, 6);
  if (hasEvidence(r)) grounded++;
}
const bad = validateInput({ schema: "culture_check_v1", exampleId: "not-a-real-id", text: "这是一段足够长的测试内容" });
if (bad.ok) fail.push("unknown id accepted");
const cited = "依据《生生》与《企业文化顶层设计》原文，此处应区分信息体、能量体与物质体，不能只做载体。" +
  "你填写的内容抓住了方向，但未完成三体解构，属于不符合之处。" +
  "改写建议：把每个关键词按物质体、能量体、信息体逐一解构。[book:生生/10.2]";
if (!validateAnswer(cited, true).ok) fail.push("valid cited answer rejected");

console.log("ids:", ALLOWED_IDS.length);
console.log("definitions:", ALLOWED_IDS.filter(id => !!EXAMPLE_CRITERIA[id].definition).length);
console.log("known 6 evidenced:", cases.length - fail.filter(x => x.includes("known case")).length, "/", cases.length);
console.log("nonsense refused:", ALLOWED_IDS.length - fail.filter(x => x.includes("nonsense")).length, "/", ALLOWED_IDS.length);
console.log("book-grounded probe evidenced:", grounded, "/", ALLOWED_IDS.length);
console.log("agent fallback switched:", degraded.switched, "tier:", degraded.tier);
console.log("failures:", fail.length);
for (const x of fail.slice(0, 40)) console.log(" -", x);
if (fail.length) process.exit(1);
