// 本地验证：67 个词条 ID 的白名单、检索、拒答与提示词出处约束（不触发真实模型）
import { ALLOWED_IDS, EXAMPLE_CRITERIA, EXAMPLE_ANCHORS } from "./functions/api/_culture/registry.js";
import { validateInput } from "./functions/api/_culture/validate.js";
import { retrieve, hasEvidence } from "./functions/api/_culture/retrieve.js";
import { buildMessages, validateAnswer } from "./functions/api/_culture/prompt.js";

const fail = [];
const noEvidenceText = "今天天气很好，我想去打篮球和吃披萨，顺便买彩票中奖";
const bookGroundedText = "本企业依据心文化与企业文化建设顶层设计，明确使命、愿景、价值观，区分信息体、能量体与物质体，通过课程体系、讲师体系、培训体系与运营体系实现知行合一。";

// 1. 注册表完整性 + 白名单 + 提示词出处约束
for (const id of ALLOWED_IDS) {
  const crit = EXAMPLE_CRITERIA[id];
  if (!crit || !crit.name || !crit.requirement) fail.push(`${id}: missing criteria`);
  if (!EXAMPLE_ANCHORS[id] || !EXAMPLE_ANCHORS[id].length) fail.push(`${id}: missing anchors`);

  const v = validateInput({ schema: "culture_check_v1", exampleId: id, text: crit.requirement });
  if (!v.ok) fail.push(`${id}: validate=${v.error}`);

  const msgs = buildMessages({ chunks: [] }, crit.requirement, id);
  if (!msgs[0].content.includes("[book:书名/章节]")) fail.push(`${id}: no citation rule`);
  if (!msgs[1].content.includes(crit.name)) fail.push(`${id}: name missing in prompt`);
}

// 2. 6 个既有示例：有书内依据时必须命中
const cases = [
  ["01-1-1", "以食载道，传递美好；心文化之根在于信仰为本"],
  ["01-1-6", "成功等于修心乘以性格乘以努力乘以能力，分物质体能量体信息体三个层面"],
  ["02-2-1", "我们的使命是以食载道传递美好，食是物质体也是能量体"],
  ["04-4-3", "我是企业人，以使命为己任，坚持价值观，为愿景奋斗的誓词"],
  ["05-5-1", "宣誓仪式固定流程，面向旗帜宣誓，先诵后唱，可重复执行"],
  ["06-6-5", "公司级荣誉按价值观分类，设标杆锚和标准锚，与待遇绑定"],
];
for (const [id, text] of cases) {
  const r = retrieve(text, id, 6);
  if (!hasEvidence(r)) fail.push(`${id}: known case no evidence hit=${r.hit}`);
}

// 3. 全部 67 个 ID：无意义字符串必须拒答（防锚点充当证据）
for (const id of ALLOWED_IDS) {
  const r = retrieve(noEvidenceText, id, 6);
  if (hasEvidence(r)) fail.push(`${id}: nonsense accepted hit=${r.hit}`);
}

// 4. 观察项：含书内术语的填写内容在多少个 ID 上可命中（不作为失败门禁）
let grounded = 0;
for (const id of ALLOWED_IDS) {
  const r = retrieve(bookGroundedText, id, 6);
  if (hasEvidence(r)) grounded++;
}

// 5. 非法 ID 与答案出处校验
const bad = validateInput({ schema: "culture_check_v1", exampleId: "not-a-real-id", text: "这是一段足够长的测试内容" });
if (bad.ok) fail.push("unknown id accepted");
const cited = "依据《生生》与《企业文化顶层设计》原文，此处应区分信息体、能量体与物质体，不能只做载体。" +
  "你填写的内容抓住了方向，但未完成三体解构，属于不符合之处。" +
  "改写建议：把每个关键词按物质体、能量体、信息体逐一解构。[book:生生/10.2]";
if (!validateAnswer(cited, true).ok) fail.push("valid cited answer rejected");

console.log("ids:", ALLOWED_IDS.length);
console.log("criteria:", Object.keys(EXAMPLE_CRITERIA).length);
console.log("anchors:", Object.keys(EXAMPLE_ANCHORS).length);
console.log("known 6 evidenced:", cases.length - fail.filter(x => x.includes("known case")).length, "/", cases.length);
console.log("nonsense refused:", ALLOWED_IDS.length - fail.filter(x => x.includes("nonsense")).length, "/", ALLOWED_IDS.length);
console.log("book-grounded probe evidenced:", grounded, "/", ALLOWED_IDS.length);
console.log("failures:", fail.length);
for (const x of fail.slice(0, 40)) console.log(" -", x);
if (fail.length) process.exit(1);
