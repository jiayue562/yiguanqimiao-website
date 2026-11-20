/* build-advisor-core.js — P0 构建期编译：把浏览器端计分引擎+题库+词库编译成服务端核心
 * 输入：wuxing/engine.js, wuxing/data.js, wuxing/rel/lexicon.js, wuxing/rel/base25.js
 * 输出：functions/api/_advisor/core.generated.js（ESM export，Cloudflare Workers 可用）
 * 纪律：只编译不改写口径；头部写源哈希供追溯；纯 Node 脚本，不依赖 WorkBuddy
 */
const fs = require("fs"), path = require("path"), crypto = require("crypto"), vm = require("vm");
const REPO = __dirname + "/..";
const W = path.join(REPO, "wuxing");
const REL = path.join(W, "rel");
const OUT = path.join(REPO, "functions/api/_advisor/core.generated.js");
function hash(p) { return crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex").slice(0, 16); }
function loadGlobal(files) {
  const ctx = { console };
  vm.createContext(ctx);
  for (const f of files) vm.runInContext(fs.readFileSync(f, "utf8"), ctx);
  return ctx;
}

/* 1) 计分引擎：从 engine.js 抽 scoreQuiz + 依赖常量（ELEMENTS/segmentOf） */
const engSrc = fs.readFileSync(path.join(W, "engine.js"), "utf8");
// engine.js 顶层定义 ELEMENTS / segmentOf / scoreQuiz；用 vm 执行整份文件后取函数引用
const ectx = { console };
vm.createContext(ectx);
vm.runInContext(engSrc + "\n;globalThis.__ELEMENTS = typeof ELEMENTS!=='undefined'?ELEMENTS:null;globalThis.__segmentOf = typeof segmentOf!=='undefined'?segmentOf:null;", ectx);
if (typeof ectx.scoreQuiz !== "function" || !ectx.__ELEMENTS) throw new Error("engine.js 结构变化：scoreQuiz/ELEMENTS 未导出");
const scoreQuizStr = vm.runInContext("scoreQuiz.toString()", ectx);
const elements = JSON.stringify(ectx.__ELEMENTS);
const segmentOfStr = ectx.__segmentOf ? vm.runInContext("segmentOf.toString()", ectx) : null;

/* 2) 题库：从 data.js 取 QUIZ_DATA */
const dctx = { console }; vm.createContext(dctx);
vm.runInContext(fs.readFileSync(path.join(W, "data.js"), "utf8") + "\n;globalThis.__QD = typeof QUIZ_DATA!=='undefined'?QUIZ_DATA:null;", dctx);
const quiz = dctx.__QD;
if (!Array.isArray(quiz) || quiz.length !== 225) throw new Error("QUIZ_DATA 非225题");

/* 3) 词库映射：lexicon.js 的 window.WXLEX */
const lctx = { window: {} }; vm.createContext(lctx);
vm.runInContext(fs.readFileSync(path.join(REL, "lexicon.js"), "utf8"), lctx);
const lex = lctx.window.WXLEX;
if (!lex || !lex.words) throw new Error("lexicon.js 无 WXLEX.words");

/* 4) 25组四段：base25.js 的 RT.relText.base25 */
const bctx = { RT: { relText: {} } }; vm.createContext(bctx);
vm.runInContext(fs.readFileSync(path.join(REL, "base25.js"), "utf8"), bctx);
const base25 = bctx.RT.relText.base25;
if (!base25 || !base25["木"]) throw new Error("base25.js 结构变化");

/* 5) 通关点与五式载体：report_text.js 的 RT_R */
const rctx = { RT_R: {} }; vm.createContext(rctx);
vm.runInContext(fs.readFileSync(path.join(REL, "report_text.js"), "utf8"), rctx);
const RT_R = rctx.RT_R;
const cp = RT_R.cpS || RT_R.checkpoints || {};
const carrier = RT_R.yCarrier || {};

const meta = {
  builtAt: new Date().toISOString(),
  hash: {
    engine: hash(path.join(W, "engine.js")),
    data: hash(path.join(W, "data.js")),
    lexicon: hash(path.join(REL, "lexicon.js")),
    base25: hash(path.join(REL, "base25.js")),
    reportText: hash(path.join(REL, "report_text.js")),
  },
  note: "构建期编译，勿手改；判定口径以源哈希为准"
};

const out = `/* core.generated.js — 构建期自动生成，勿手改 */
/* meta: ${JSON.stringify(meta)} */
export const META = ${JSON.stringify(meta)};
export const ELEMENTS = ${elements};
${segmentOfStr ? "const segmentOf = " + segmentOfStr + ";" : "const segmentOf = (l) => l <= 3 ? 1 : (l <= 6 ? 2 : 3);"}
export const scoreQuiz = ${scoreQuizStr};
export const QUIZ_DATA = ${JSON.stringify(quiz)};
export const LEXICON = ${JSON.stringify({ words: lex.words, rel25: lex.rel25 })};
export const BASE25 = ${JSON.stringify(base25)};
export const CHECKPOINTS = ${JSON.stringify(cp)};
export const CARRIER = ${JSON.stringify(carrier)};
export const SHENG = { "木":"火","火":"土","土":"金","金":"水","水":"木" };
export const KE = { "木":"土","土":"水","水":"火","火":"金","金":"木" };
export function judgeRelation(P, Q) {
  if (P === Q) return "自对";
  if (SHENG[P] === Q) return "相生";
  if (SHENG[Q] === P) return "被生";
  if (KE[P] === Q) return "相克";
  if (KE[Q] === P) return "被克";
  return "未知";
}
`;
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, out, "utf8");
console.log("BUILT", OUT, out.length, "bytes");
console.log("HASH", JSON.stringify(meta.hash));
