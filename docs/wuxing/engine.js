/* ============================================================
   五行人格学在线测评 · 计分引擎（二期：百分制三步判定版）
   判定流程（悟空 2026-11-15 指定）：
     第一步 百分制换算——各行答是数（满分45）归一化为满分100；
     第二步 类型判定——五属性得分最高者为主导类型；
     第三步 阴阳判定——主导型内比较阳性能量（L1-L3 答是）与
            阴性能量（L7-L9 答是）占比，L4-L6 为中间带；
     第四步 层级判定——主导型内峰值层（平局取更深）＋起点层（最深非空层）。
   口径基线：九层三段＝健康(L1-L3)／一般(L4-L6)／不健康(L7-L9)，B0
   相生 木→火→土→金→水→木；相克 木克土→土克水→水克火→火克金→金克木
   起点规则（悟空 2026-11-15 确认）：建议一律以答「是」词中层位最深者
   （最趋向 L9 方向的非空层）为起点，三模型流水线＝拔阴取阳→化克为生→B=MAP
   ============================================================ */

const ELEMENTS = ["木", "火", "土", "金", "水"];

const ELEMENT_COLOR = {
  "木": { main: "#3B6D11", light: "#EAF3DE" },   /* 绿 */
  "火": { main: "#A32D2D", light: "#FCEBEB" },   /* 红 */
  "土": { main: "#D4A825", light: "#FBF3D9" },   /* 黄 */
  "金": { main: "#5F5E5A", light: "#F1EFE8" },   /* 深灰（悟空 2026-11-15 令：真白在浅底不可辨，色条/色块改深灰填充） */
  "水": { main: "#185FA5", light: "#E6F1FB" }    /* 蓝 */
};

/* 文字安全色：白色色条在白底上不可读，凡文字/边框处用此色（悟空 2026-11-15 配色令：木绿火红土黄金灰水蓝） */
const EL_TEXT = {
  "木": "#3B6D11", "火": "#A32D2D", "土": "#9A7B0A", "金": "#5F5E5A", "水": "#185FA5"
};

/* 三段配色（悟空 2026-11-15 配色令：健康蓝 / 一般深灰 / 不健康红） */
const SEG_COLOR = { 1: "#2E6DA8", 2: "#6E6E68", 3: "#C0392B" };
const SEG_TEXT = { 1: "#2E6DA8", 2: "#6E6E68", 3: "#C0392B" };

const LAYER_NAMES = {
  1: "解放", 2: "心理能力", 3: "社会价值",
  4: "失衡", 5: "人际控制", 6: "过度补偿",
  7: "侵害", 8: "妄想强迫", 9: "病态破坏"
};

const SEGMENT_NAMES = { 1: "健康段", 2: "一般段", 3: "不健康段" };
function segmentOf(layer) { return layer <= 3 ? 1 : (layer <= 6 ? 2 : 3); }

/* 拔阴取阳五大通关点（权威文件口径） */
const CHECKPOINTS = {
  "木": { to: "火", name: "忍辱", how: "控制脾气，不随意发火；关注别人的情绪，忍住不顶撞" },
  "火": { to: "土", name: "放任的对治", how: "不报委屈，多找自己的问题，不找别人的问题" },
  "土": { to: "金", name: "不怨人", how: "停止嘀嘀咕咕，内心有决断，知道该做什么" },
  "金": { to: "水", name: "感恩", how: "找别人的好处，聚人缘、聚阳光" },
  "水": { to: "木", name: "认不是", how: "承认错误不找借口，改掉小习惯" }
};

/* 五行病链条（拔阴取阳权威文件：内在想法→外在行为→命运结果） */
const ILLNESS_CHAINS = {
  "木": "不服人 → 顶撞人 → 招难",
  "火": "好争理 → 起贪争 → 受苦",
  "土": "好怨人 → 被欺人 → 受累",
  "金": "好分辩 → 伤人 → 受贫",
  "水": "好烦人 → 厌人 → 受气"
};

/* 五类型文案（初稿，待悟空审定） */
const TYPES = {
  "木": {
    name: "木行人", xiang: "曲直 · 生发",
    metaphor: "如春天的树木，向上生长，向外舒展。",
    core: "木行人的底色是「生发」：有主见、敢开创、成长欲强，心里认准了方向就会一直往前走。为人正直，看重仁德，天生带着一股「要把事情做起来」的劲。",
    traits: ["有主见，认准方向不轻易回头", "敢想敢做，喜欢开新路", "正直坦率，看重仁德", "学习欲与成长欲强"],
    strengths: ["开创力强，能从无到有把事情带起来", "方向感好，能在混乱中给出主张", "成长快，愿意不断突破自己", "能带动身边的人一起往前走"],
    watch: "木的阴面是「不服人」：急起来容易顶撞人、听不进意见。木行病链条是「不服人→顶撞人→招难」。",
    growth: "木行人的功课是修「忍辱」（木→火通关点）：想发脾气时先停一下，关注对方的情绪，忍住不顶撞——能忍辱的木，就是觉悟的木。"
  },
  "火": {
    name: "火行人", xiang: "炎上 · 礼明",
    metaphor: "如夏天的火焰，光明外放，热情照人。",
    core: "火行人的底色是「炎上」：热情开朗、表达力强、走到哪里都带着光和热。重礼数、讲分寸，天生擅长把气氛点亮、把人心焐热。",
    traits: ["热情开朗，感染力强", "表达力好，善于点燃气氛", "重礼节，讲分寸", "行动快，说做就做"],
    strengths: ["天生的带动者，能把冷场变热闹", "表达与感染力强，适合面向人群", "行动力快，想到就动", "对人真诚，容易结缘"],
    watch: "火的阴面是「好争理」：急起来容易争执、贪多求快。火行病链条是「好争理→起贪争→受苦」。",
    growth: "火行人的功课是「找自己的问题」（火→土通关点）：不报委屈，遇事先看自己哪里没做到位——多从自身找原因，热情就变成了真正的照明。"
  },
  "土": {
    name: "土行人", xiang: "稼穑 · 承载",
    metaphor: "如厚德的大地，承载包容，稳定可信。",
    core: "土行人的底色是「承载」：稳重、诚信、包容，说话办事让人踏实。不急不躁，能装得下事、扛得住难，是团队里最可靠的那块基石。",
    traits: ["稳重踏实，说到做到", "包容宽厚，能容人容事", "务实肯干，注重积累", "诚信为本，值得托付"],
    strengths: ["可靠性高，托付的事放心", "善于组织与积累，稳扎稳打", "包容性强，能调和各方", "抗压力好，是团队的地基"],
    watch: "土的阴面是「好怨人」：不顺时容易嘀嘀咕咕、埋在心里。土行病链条是「好怨人→被欺人→受累」。",
    growth: "土行人的功课是修「不怨人」（土→金通关点）：停止嘀咕，内心有决断，知道该做什么——怨气一化，脾胃开了，智慧就出来了。"
  },
  "金": {
    name: "金行人", xiang: "从革 · 义气",
    metaphor: "如秋天的金属，收敛果决，重义有情。",
    core: "金行人的底色是「从革」：果断利落、原则性强、精益求精。对事讲标准，对人讲义气，认准的规矩不轻易让步，该变革时敢下手。",
    traits: ["果断利落，决策不拖泥带水", "原则性强，讲标准讲规矩", "重义气，认人不认利", "精益求精，追求到位"],
    strengths: ["决断力强，关键时刻拿得了主意", "执行力高，说到就做到", "标准意识好，能把品质守住", "重情重义，凝聚人心"],
    watch: "金的阴面是「好分辩」：恼起来容易挑剔、刻薄、得理不饶人。金行病链条是「好分辩→伤人→受贫」。",
    growth: "金行人的功课是修「感恩」（金→水通关点）：多找别人的好处——找好处就是聚人缘、聚阳光；找别人的不好处，吸的是阴气。"
  },
  "水": {
    name: "水行人", xiang: "润下 · 智慧",
    metaphor: "如冬天的流水，柔静下沉，智慧渗透。",
    core: "水行人的底色是「润下」：柔和、沉静、有智慧。不争一时之先，却能渗透到别人到不了的地方；遇事能静下来想清楚，适应力极强。",
    traits: ["沉静柔和，遇事不慌", "智慧内敛，想得深看得远", "适应力强，能屈能伸", "包容含蓄，润物无声"],
    strengths: ["谋略深，能在静中看清全局", "适应力与韧性极强", "包容性好，能化冲突于无形", "善于滋养他人，是背后的力量"],
    watch: "水的阴面是「好烦人」：忧烦多了容易退缩、失去方向。水行病链条是「好烦人→厌人→受气」。",
    growth: "水行人的功课是修「认不是」（水→木通关点）：承认错误不找借口，改掉拖拖沓沓的小习惯——水清了，智慧自然亮出来。"
  }
};

/* ============================================================
   计分引擎
   ans: { 原始题号(index): true/false }；data: QUIZ_DATA
   ============================================================ */
function scoreQuiz(ans, data) {
  const R = {};           // 每行答是数（全部九层）
  const W = {};           // 行分：行内 L1-L3 答是数（0-15）
  const layers = {};      // 每层答是数（0-25）
  const seg = { 1: 0, 2: 0, 3: 0 };
  const yesWords = [];    // 答是词（按原始层位）
  ELEMENTS.forEach(e => { R[e] = 0; W[e] = 0; });
  for (let k = 1; k <= 9; k++) layers[k] = 0;

  data.forEach((it, i) => {
    if (ans[i] !== true) return;
    R[it.e]++; layers[it.layer]++; seg[segmentOf(it.layer)]++;
    if (it.layer <= 3) W[it.e]++;
    yesWords.push(it);
  });

  const total = yesWords.length;
  const GHI = total > 0 ? Math.round(seg[1] / total * 100) : null;

  /* 第一步 · 百分制换算：各行答是数（满分 45）归一化为满分 100 */
  const P = {};
  ELEMENTS.forEach(e => { P[e] = Math.round(R[e] / 45 * 100); });

  /* 第二步 · 类型判定：百分制得分最高者为主导类型
     阈值（一期经验值）：最高分 <11（不足 5 词）→ 能量未显；
     最高分领先 ≥7（约 3 词差）→ 单一型，否则复合型 */
  const sorted = ELEMENTS.slice().sort((a, b) => P[b] - P[a] || R[b] - R[a]);
  const top = sorted[0], second = sorted[1];
  let typeState, mainType = null, subType = null;
  if (P[top] < 11) {
    typeState = "能量未显";
  } else if (P[top] - P[second] >= 7) {
    typeState = "单一型"; mainType = top;
  } else {
    typeState = "复合型"; mainType = top; subType = second;
  }

  /* 第三步 · 阴阳判定（主导型内）：
     阳＝该行 L1-L3 答是数；阴＝该行 L7-L9 答是数；L4-L6 为中间带。
     阳占两极≥60% → 阳性主导；≤40% → 阴性主导；之间 → 阴阳并存；
     两极皆无答是 → 阴阳未显（阈值为一期经验值） */
  let yinYang = null;
  if (mainType) {
    const pole = { y: 0, m: 0, n: 0 };
    yesWords.forEach(w => {
      if (w.e !== mainType) return;
      const s = segmentOf(w.layer);
      if (s === 1) pole.y++; else if (s === 3) pole.n++; else pole.m++;
    });
    const poles = pole.y + pole.n;
    const yangPct = poles > 0 ? Math.round(pole.y / poles * 100) : null;
    const yinPct = poles > 0 ? 100 - yangPct : null;
    let verdict;
    if (poles === 0) verdict = "阴阳未显";
    else if (yangPct >= 60) verdict = "阳性主导";
    else if (yangPct <= 40) verdict = "阴性主导";
    else verdict = "阴阳并存";
    yinYang = { y: pole.y, m: pole.m, n: pole.n, yangPct, yinPct, verdict };
  }

  /* 第四步 · 层级判定（主导型内）：
     行内峰值层＝该行答是词最集中的层（平局取更深）；行内起点层＝最深非空层 */
  let mainLayers = null, mainPeak = null, mainPeakVal = 0, mainStart = null, mainStartWords = [];
  if (mainType) {
    mainLayers = {}; for (let k = 1; k <= 9; k++) mainLayers[k] = 0;
    yesWords.forEach(w => { if (w.e === mainType) mainLayers[w.layer]++; });
    let pv = -1;
    for (let k = 1; k <= 9; k++) { if (mainLayers[k] >= pv) { pv = mainLayers[k]; mainPeak = k; } }
    if (pv > 0) { mainPeakVal = pv; } else { mainPeak = null; }
    for (let k = 9; k >= 1; k--) { if (mainLayers[k] > 0) { mainStart = k; break; } }
    if (mainStart) {
      mainStartWords = yesWords.filter(w => w.e === mainType && w.layer === mainStart)
        .sort((a, b) => P[b.e] - P[a.e]).slice(0, 5);
    }
  }

  // 峰值层（全九层，峰值法；层分平局取更深，与起点规则方向一致）
  let peak = null, peakVal = -1;
  for (let k = 1; k <= 9; k++) {
    if (layers[k] >= peakVal) { peakVal = layers[k]; peak = k; }
  }
  peak = peakVal > 0 ? peak : null;

  // 起点规则：答是词 L9→L1 第一个非空层（全九层口径，供建议流水线使用）
  let startLayer = null;
  for (let k = 9; k >= 1; k--) { if (layers[k] > 0) { startLayer = k; break; } }
  const startWords = startLayer
    ? yesWords.filter(w => w.layer === startLayer)
        .sort((a, b) => P[b.e] - P[a.e])
        .slice(0, 5)
    : [];

  return { R, W, P, layers, mainLayers, seg, total, GHI,
    sorted, typeState, mainType, subType,
    yinYang, mainPeak, mainPeakVal, mainStart, mainStartWords,
    peak, peakVal, startLayer, startWords, yesWords };
}

/* 起点建议文案生成（一期模板版；三模型流水线：拔阴取阳→化克为生→B=MAP） */
function buildAdvice(res) {
  /* 起点规则退化处理：最深非空层在健康段（L1-L3）＝无趋向 L9 的词，不出转化起点 */
  if (!res.startLayer || res.startLayer <= 3) {
    return { noStart: true, html: "<p>本次作答中，你答「是」的词都落在健康段（L1–L3），没有趋向 L9 方向的转化起点。这不是问题，而是好状态——报告转为巩固型建议：把你的优势行为固化成习惯锚点（每周固定时间做一件滋养它的小事），并保持觉察。九层测评的转化建议会在出现一般段及以上词时自动给出。</p>" };
  }
  const seg = segmentOf(res.startLayer);
  const main = res.mainType || res.sorted[0];
  const cp = CHECKPOINTS[main];
  const wordsStr = res.startWords.map(w => `「${w.word}」`).join("、");
  const segName = SEGMENT_NAMES[seg];
  const layerName = LAYER_NAMES[res.startLayer];
  let html = `<p><strong>起点词组（${segName} · L${res.startLayer} ${layerName}）</strong>：${wordsStr}</p>`;
  html += `<p>按照起点规则，建议从这些最深处的词开始转化，而不是先去巩固优点。</p>`;
  html += `<p><strong>第一步 · 拔阴取阳（觉察）</strong>：你的主行是${main}，五行病链条是「${ILLNESS_CHAINS[main]}」。对照起点词，观察这个链条最近在你身上如何发生——先觉察，不急于改变。</p>`;
  if (seg === 2) {
    html += `<p><strong>第二步 · 化克为生（觉察方向）</strong>：${segName}的状态还不是病，但已开始消耗——主行${main}的阴面正在克伤自己其他行的阳面（如${main}的怒气压制承载）。转化枢纽：修「${cp.name}」——${cp.how}。</p>`;
  } else {
    html += `<p><strong>第二步 · 化克为生（转化路径）</strong>：${segName}的词答「是」属于需要认真对待的能量状态信号。转化枢纽：修「${cp.name}」——${cp.how}。按「${main}→${cp.to}」通关点把克链还原为生链，建议每日一次觉察练习，持续三个月。</p>`;
    html += `<p style="color:#A32D2D"><strong>提示</strong>：不健康段的词属于能量状态信号，非医学诊断。如这些状态已明显影响生活，请同时寻求专业心理咨询支持。</p>`;
  }
  html += `<p><strong>第三步 · 福格行为模型（微行为落地）</strong>：从起点词中选一个最贴你的词，设计一个两分钟内可完成的小行为——锚点句式「当我出现这个念头之后，我就做（那个小动作）」。先只做观察记录两周，再进入替换。三个月后复测，看这个词在九层上的位置是否向 L1 方向移动。</p>`;
  return { noStart: false, html };
}
