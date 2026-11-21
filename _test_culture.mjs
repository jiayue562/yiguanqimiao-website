// 本地验证：知识包检索 + 拒答门禁 + 提示词出处约束（不触发真实模型）
import { META, CHUNKS, TERMS } from "./functions/api/_culture/kb.js";
import { retrieve, hasEvidence } from "./functions/api/_culture/retrieve.js";
import { buildMessages, validateAnswer, EXAMPLE_CRITERIA } from "./functions/api/_culture/prompt.js";

console.log("KB:", META.kb_version, "chunks", META.chunk_count, "terms", TERMS.length);

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
  const ev = hasEvidence(r);
  const msgs = buildMessages(r, text, id);
  const hasOut = msgs[0].content.includes("[book:书名/章节]");
  console.log(`${id} | hit=${r.hit} evidenced=${ev} chunks=${r.chunks.length} 出处约束=${hasOut} 首源=${r.chunks[0] ? r.chunks[0].book + "/" + r.chunks[0].section : "无"}`);
}

// 无依据场景：故意填与两本书无关的内容
const none = retrieve("今天天气很好，我想去打篮球和吃披萨，顺便买彩票中奖", "01-1-1", 6);
console.log("无依据场景 | hit=", none.hit, "evidenced=", hasEvidence(none));

// 校验器
const longCited = "依据《生生》书稿，文化是组织的操作系统，须同时建设信息体、能量体与物质体三体，不能只做载体。" +
  " [book:生生/卷二] 你填写的内容抓住了使命方向，但未区分三体，属于不符合之处。" +
  " 改写建议：把每个关键词按物质体、能量体、信息体逐一解构。[book:生生/10.2]";
console.log("valid(cited)=", validateAnswer(longCited, true));
console.log("valid(no_cite)=", validateAnswer("这是一段足够长但没有标注任何出处也没有提到无法判断的评估文字，应该被判为缺少引用。".repeat(3), true));
console.log("criteria keys=", Object.keys(EXAMPLE_CRITERIA).join(","));
