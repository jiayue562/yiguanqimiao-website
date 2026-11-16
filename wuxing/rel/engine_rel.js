/* ============================================================
   五行人格学 · 关系测评引擎（一期网页版）
   依据：《关系分型测评报告结构设计》V1.0 + 《关系测评体系方案》V1.0
   铁规：词为唯一原点；答否词不做个体推断；判定过程全透明。
   口径：阳面词 = L1-L3 答是；阴面词 = L4-L9 答是（克证据要求阴克阳）；
   相生 木→火→土→金→水→木；相克 木克土→土克水→水克火→火克金→金克木。
   K/S 权重为一期经验值（方案 4.2/4.3），待施测校准。
   ============================================================ */

var REL_ELS = ["木", "火", "土", "金", "水"];
var REL_SHENG = { "木": "火", "火": "土", "土": "金", "金": "水", "水": "木" };
var REL_KE = { "木": "土", "土": "水", "水": "火", "火": "金", "金": "木" };

/* 段名与层名（与 engine.js 一致，避免重复加载依赖） */
if (typeof segmentOf === "undefined") {
  function segmentOf(layer) { return layer <= 3 ? 1 : (layer <= 6 ? 2 : 3); }
}

/* 四象限（词级，唯一划分单元）：
   共鸣区 自测是∧他测是；投射区 自测否∧他测是；防御区 自测是∧他测否；空白区 双否 */
function relQuadrant(i, selfAns, otherAns) {
  var s = selfAns[i] === true, o = otherAns[i] === true;
  if (s && o) return "resonance";
  if (!s && o) return "projection";
  if (s && !o) return "defense";
  return "blank";
}

/* 被生/被克方重要性（方案 4.2/4.3）：对方主行 ×1.2、次行 ×1.0、其他 ×0.8 */
function relTargetW(row, person) {
  if (row === person.mainType) return 1.2;
  if (row === person.secondType) return 1.0;
  return 0.8;
}

/* ============================================================
   主计算：computeRelation(selfAns, otherAns, data)
   ============================================================ */
function computeRelation(selfAns, otherAns, data) {
  var selfRes = scoreQuiz(selfAns, data);
  var otherRes = scoreQuiz(otherAns, data);
  /* 能量未显时按方案 2.3.4：暂定主行＝得分最高行 */
  function personOf(res) {
    return {
      res: res,
      mainType: res.mainType || res.sorted[0],
      secondType: res.typeState === "复合型" ? res.subType : res.sorted[1]
    };
  }
  var P = personOf(selfRes), Q = personOf(otherRes);

  /* 统计范围（悟空 2026-11-15 令）：只整理双方主行的词，其他行不参与四象限与统计 */
  var scopeRows = [P.mainType];
  if (scopeRows.indexOf(Q.mainType) === -1) scopeRows.push(Q.mainType);
  var scopeText = scopeRows.join("＋") + "行";

  /* 关系方向（悟空 2026-11-15 令）：按双方主类型判定——
     相生 木→火→土→金→水→木；相克 木克土→土克水→水克火→火克金→金克木 */
  var dirText, dirType;
  if (Q.mainType === P.mainType) {
    dirType = "tongqi";
    dirText = P.mainType + "行同气比和（双方主行同行，无生克损伤路径）";
  } else if (REL_SHENG[Q.mainType] === P.mainType) {
    dirType = "sheng";
    dirText = Q.mainType + "生" + P.mainType + "（对方主行生助我方主行）";
  } else if (REL_SHENG[P.mainType] === Q.mainType) {
    dirType = "sheng";
    dirText = P.mainType + "生" + Q.mainType + "（我方主行生助对方主行）";
  } else if (REL_KE[P.mainType] === Q.mainType) {
    dirType = "ke";
    dirText = P.mainType + "克" + Q.mainType + "（我方主行克对方主行）";
  } else {
    dirType = "ke";
    dirText = Q.mainType + "克" + P.mainType + "（对方主行克我方主行）";
  }

  /* 词级四象限分布（仅主行范围词库） */
  var quad = { resonance: [], projection: [], defense: [], blank: [] };
  data.forEach(function(it, i) {
    if (scopeRows.indexOf(it.e) === -1) return;
    quad[relQuadrant(i, selfAns, otherAns)].push({ it: it, i: i });
  });

  /* 行×层聚合（空白区专用，不逐词；仅主行范围） */
  var blankGrid = {};
  scopeRows.forEach(function(e) { blankGrid[e] = {}; for (var k = 1; k <= 9; k++) blankGrid[e][k] = 0; });
  quad.blank.forEach(function(w) { blankGrid[w.it.e][w.it.layer]++; });

  /* 证据对采集（词级全组合，仅主行范围内）：
     生证据：阳面词(源) 生 阳面词(靶)；克证据：阴面词(源) 克 阳面词(靶)；阳对阳克不计 */
  var shengPairs = [], kePairs = [];
  var selfWords = [], otherWords = [];
  data.forEach(function(it, i) {
    if (scopeRows.indexOf(it.e) === -1) return;
    if (selfAns[i] === true) { var w = {}; for (var k in it) w[k] = it[k]; w.i = i; selfWords.push(w); }
    if (otherAns[i] === true) { var w2 = {}; for (var k2 in it) w2[k2] = it[k2]; w2.i = i; otherWords.push(w2); }
  });

  selfWords.forEach(function(w1) {
    otherWords.forEach(function(w2) {
      var q1 = w1.layer <= 3, q2 = w2.layer <= 3;   /* 阳面判定 */
      var y1 = w1.layer >= 4, y2 = w2.layer >= 4;   /* 阴面判定（克源要求） */
      /* 反向：对方词 → 我方词 */
      if (q2 && REL_SHENG[w2.e] === w1.e && q1) {
        shengPairs.push(makePair(w2, w1, Q, P, "other", "sheng"));
      }
      if (y2 && REL_KE[w2.e] === w1.e && q1) {
        kePairs.push(makePair(w2, w1, Q, P, "other", "ke"));
      }
      /* 正向：我方词 → 对方词 */
      if (q1 && REL_SHENG[w1.e] === w2.e && q2) {
        shengPairs.push(makePair(w1, w2, P, Q, "self", "sheng"));
      }
      if (y1 && REL_KE[w1.e] === w2.e && q2) {
        kePairs.push(makePair(w1, w2, P, Q, "self", "ke"));
      }
    });
  });

  function makePair(src, tgt, S, T, side, type) {
    var srcQ = relQuadrant(src.i, selfAns, otherAns);
    var tgtQ = relQuadrant(tgt.i, selfAns, otherAns);
    var zone = { resonance: 1.0, defense: 0.9, projection: 0.6 }[srcQ];
    if (type === "ke") {
      var lay = src.layer <= 6 ? 0.6 : 1.0;              /* 层位分：L4-6=0.6，L7-9=1.0 */
      var main = src.e === S.mainType ? 1.2 : 1.0;       /* 主行系数（源） */
      var imp = relTargetW(tgt.e, T);                    /* 被克方重要性 */
      imp *= tgt.layer <= 3 ? 1.0 : 0.7;                 /* 被克词层位 L4-6 ×0.7（靶恒为阳面 L1-3，此项实际恒 1.0） */
      var k = lay * main * imp * zone;
      return { src: src, tgt: tgt, side: side, type: "ke", srcQ: srcQ, tgtQ: tgtQ,
        fac: { 层位: lay, 主行: main, 重要性: imp, 区位: zone }, score: k, bothRes: srcQ === "resonance" && tgtQ === "resonance" };
    } else {
      var lay2 = src.layer === 1 ? 1.0 : (src.layer === 2 ? 0.9 : 0.8); /* 生源层位分 */
      var main2 = src.e === S.mainType ? 1.2 : 1.0;
      var imp2 = relTargetW(tgt.e, T);
      var s = lay2 * main2 * imp2 * zone;
      return { src: src, tgt: tgt, side: side, type: "sheng", srcQ: srcQ, tgtQ: tgtQ,
        fac: { 层位: lay2, 主行: main2, 重要性: imp2, 区位: zone }, score: s, bothRes: srcQ === "resonance" && tgtQ === "resonance" };
    }
  }

  /* 分型判定（悟空 2026-11-15 令）：关系方向由双方主类型直接判定
     （如 我木 TA水 → 水生木 → 相生关系型）；主行范围内生/克证据对
     作为佐证统计呈现，不再由跨行词证据投票决定方向 */
  var sR = shengPairs.filter(function(p) { return p.bothRes; }).length;
  var kR = kePairs.filter(function(p) { return p.bothRes; }).length;
  var sAll = shengPairs.length, kAll = kePairs.length;
  var verdict, usedScope = "主行范围（" + scopeText + "）证据";
  if (dirType === "tongqi") verdict = "同气比和型";
  else if (dirType === "sheng") verdict = "相生关系型";
  else verdict = "相克关系型";
  var verdictNote = "关系方向按主类型判定：" + dirText
    + "。范围内佐证统计：生证据 S = " + sAll + "（其中共鸣区 " + sR + "），克证据 K = " + kAll + "（其中共鸣区 " + kR + "）。";

  /* 关系层级指数 RL = 双方峰值层中更深的一方 */
  var rl = null;
  if (selfRes.peak && otherRes.peak) rl = Math.max(selfRes.peak, otherRes.peak);
  else if (selfRes.peak) rl = selfRes.peak;
  else if (otherRes.peak) rl = otherRes.peak;

  /* 双线 Top3 推荐 */
  kePairs.sort(function(a, b) { return b.score - a.score; });
  shengPairs.sort(function(a, b) { return b.score - a.score; });

  /* ============================================================
     R3.5 层面生克图谱（v1.2）：三段层面 × 词对 × 生克价判定矩阵
     矩阵：相生组 阳面=生点/中=观察带/阴面=变相克点（生过头）；
           相克组 阳面=生点（克得其所）/中=摩擦带/阴面=克点；
           同气组 阳面=生点/中=观察带/阴面=克点（盲区重合）。
     词对：两池各取一词，行关系满足 生/克/同行，且两词同处一个层面段。
     ============================================================ */
  function segOfL(layer) { return layer <= 3 ? 1 : (layer <= 6 ? 2 : 3); }
  var SEG_VAL = {
    sheng: { 1: "生点", 2: "观察带", 3: "变相克点" },
    ke: { 1: "生点", 2: "摩擦带", 3: "克点" },
    tongqi: { 1: "生点", 2: "观察带", 3: "克点" }
  };
  var segMap = {};
  [1, 2, 3].forEach(function(seg) {
    var valence = SEG_VAL[dirType][seg];
    var pts = [];
    /* 生克方向按组合类型取对应环：相生用生环、相克用克环、同气同行 */
    var relFn = dirType === "ke" ? REL_KE : REL_SHENG;
    selfWords.forEach(function(w1) {
      otherWords.forEach(function(w2) {
        if (segOfL(w1.layer) !== seg || segOfL(w2.layer) !== seg) return;
        var src, tgt, side;
        if (dirType === "tongqi") {
          if (w1.e !== w2.e) return;
          src = w1; tgt = w2; side = "self";
        } else if (relFn[w1.e] === w2.e) { src = w1; tgt = w2; side = "self"; }
        else if (relFn[w2.e] === w1.e) { src = w2; tgt = w1; side = "other"; }
        else return;
        pts.push({ src: src, tgt: tgt, side: side, seg: seg, valence: valence });
      });
    });
    /* 排序：克点/变相克点取层位最深的词对（冲突主场）；生点取层位最浅的（最通畅） */
    pts.sort(function(a, b) { return (b.src.layer + b.tgt.layer) - (a.src.layer + a.tgt.layer); });
    if (valence === "生点") pts.reverse();
    segMap[seg] = { valence: valence, points: pts.slice(0, 4), total: pts.length };
  });

  return {
    selfRes: selfRes, otherRes: otherRes, P: P, Q: Q,
    scopeRows: scopeRows, scopeText: scopeText, dirText: dirText, dirType: dirType,
    quad: quad, blankGrid: blankGrid,
    shengPairs: shengPairs, kePairs: kePairs,
    sR: sR, kR: kR, sAll: shengPairs.length, kAll: kePairs.length,
    verdict: verdict, verdictNote: verdictNote, usedScope: usedScope,
    rl: rl,
    segMap: segMap, segTypeKey: dirType,
    topKe: kePairs.slice(0, 3), topSheng: shengPairs.slice(0, 3)
  };
}

/* ============================================================
   功课包文案（主生课 + 主克课 + 日课；B=MAP 模板，方案第五、六章）
   ============================================================ */
var REL_REPLACE = {
  "木": "被反驳想顶撞时，先复述对方观点再表态（只复述一句，不要求认同）",
  "火": "想争理时，先问自己一句「我要的是对，还是这段关系」，再开口",
  "土": "想抱怨嘀咕时，改说一件对方本周做到的具体的事",
  "金": "想分辩挑理时，先说一句「这一点你说得对」，再讲自己的看法",
  "水": "想退缩躲避时，先把眼前一件小事做完再停（两分钟也算）"
};
var REL_SHENG_ACT = "每周一次主动发起轻松共处时刻（散步 / 一起做饭 / 一起做一件小事），共处中当面说出对方本周的一个具体好处";

function relLessonPack(rel) {
  var nm = rel.otherName || "TA";
  var pack = { shengCard: null, keCard: null, daily: null, map90: null };

  /* 主克课（若克对存在） */
  if (rel.topKe.length) {
    var k = rel.topKe[0];
    var srcIsSelf = k.side === "self";
    var srcName = srcIsSelf ? "我的" : (nm + "的");
    var tgtName = srcIsSelf ? (nm + "的") : "我的";
    var cpRow = k.src.e;
    var cp = CHECKPOINTS[cpRow];
    var h = "<h3>主克课 · 化克为生（本轮先做，权重最高克对）</h3>";
    h += "<p><strong>克链</strong>：" + srcName + "「" + k.src.word + "」（" + k.src.e + "行 L" + k.src.layer + "，" + relQName(k.srcQ) + "）正在克伤" + tgtName + "「" + k.tgt.word + "」（" + k.tgt.e + "行 L" + k.tgt.layer + "，阳面）——K = " + k.score.toFixed(3) + "。</p>";
    h += "<p><strong>K 分构成</strong>（透明可审计）：层位分 " + k.fac["层位"] + " × 主行系数 " + k.fac["主行"] + " × 被克方重要性 " + k.fac["重要性"] + " × 区位系数 " + k.fac["区位"] + "。</p>";
    h += "<p><strong>通关点</strong>：" + cpRow + "→" + cp.to + " · 修「" + cp.name + "」——" + cp.how + "。</p>";
    h += "<p><strong>目标行为</strong>：" + REL_REPLACE[cpRow] + "。</p>";
    h += "<p><strong>P 触发点</strong>：锚定冲突瞬间——「当我" + (srcIsSelf ? "出现「" + k.src.word + "」这个反应" : "观察到" + nm + "出现类似反应") + "之后」，先做上面那个新动作。</p>";
    h += "<p><strong>A 能力</strong>：两分钟内可完成。先做观察版两周（只觉察记录、不动手改），再切替换版。</p>";
    h += "<p><strong>M 动机</strong>：代价——不转化，病链「" + ILLNESS_CHAINS[k.src.e] + "」继续伤关系；意义——克对转生后，对方的阳面反过来稳住我方（关系共赢）；庆祝——每次新动作完成即自我确认，每周复盘时互相点名对方本周做到的一个词。</p>";
    h += "<p class='muted'>功课归属：克源词在" + (srcIsSelf ? "你自己身上，直接领做" : nm + "身上，以「功课转达卡」交付——措辞为「建议共同看看」，不做指责工具") + "。</p>";
    pack.keCard = h;
  }

  /* 主生课（若生对存在） */
  if (rel.topSheng.length) {
    var s = rel.topSheng[0];
    var srcIsSelf2 = s.side === "self";
    var srcName2 = srcIsSelf2 ? "我的" : (nm + "的");
    var tgtName2 = srcIsSelf2 ? (nm + "的") : "我的";
    var h2 = "<h3>主生课 · 助生固本（增益方向）</h3>";
    h2 += "<p><strong>生链</strong>：" + srcName2 + "「" + s.src.word + "」（" + s.src.e + "行 L" + s.src.layer + "，" + relQName(s.srcQ) + "）一直在滋养" + tgtName2 + "「" + s.tgt.word + "」（" + s.tgt.e + "行 L" + s.tgt.layer + "）——S = " + s.score.toFixed(3) + "。</p>";
    h2 += "<p><strong>S 分构成</strong>：生源层位分 " + s.fac["层位"] + " × 主行系数 " + s.fac["主行"] + " × 被生方重要性 " + s.fac["重要性"] + " × 区位系数 " + s.fac["区位"] + "。</p>";
    h2 += "<p><strong>目标行为</strong>：" + REL_SHENG_ACT + "。用「" + s.src.word + "」的方式去做，滋养的正是对方的「" + s.tgt.word + "」。</p>";
    h2 += "<p><strong>P 触发点</strong>：锚点「每周日晚饭后」固定时段（双方同在），或任意一个每周固定共处场景。</p>";
    h2 += "<p><strong>A 能力</strong>：十五分钟内的低成本活动；说一个好处只要一句话。先做观察版两周：只留意并记下对方的好处，不开口。</p>";
    h2 += "<p><strong>M 动机</strong>：代价——生链荒废，关系不是冲突而是疏远平淡；意义——找好处聚阳气（拔阴取阳金→水通关点技术），对方的「" + s.tgt.word + "」反过来稳住「" + s.src.word + "」——我养 TA，TA 稳我；庆祝——说完好处双方互相确认，月小结回看好处清单。</p>";
    pack.shengCard = h2;
  }

  /* 日课（双方主行通关点，每日觉察一次） */
  var cpS = CHECKPOINTS[rel.P.mainType], cpQ = CHECKPOINTS[rel.Q.mainType];
  var d = "<h3>日课 · 双方主行通关点（每日各觉察一次）</h3><ul>"
    + "<li><strong>你自己（" + rel.P.mainType + "）</strong>：修「" + cpS.name + "」——" + cpS.how + "。</li>"
    + "<li><strong>" + nm + "（你眼中，" + rel.Q.mainType + "）</strong>：修「" + cpQ.name + "」——" + cpQ.how + "。<span class='muted'>（以功课转达卡交付，措辞「建议共同看看」）</span></li></ul>";
  pack.daily = d;

  /* 90 天关系行动地图 */
  pack.map90 = "<h3>90 天关系行动地图</h3><ul>"
    + "<li><strong>第 1–4 周（月一）</strong>：只做共鸣区措施——主生课 + 主克课观察版起步，每周 15 分钟共同复盘互相点名（起点纪律：先在共识的词上工作）。</li>"
    + "<li><strong>第 5–8 周（月二）</strong>：加入投射区求证练习（先求证后定义）；主克课切入替换版。</li>"
    + "<li><strong>第 9–12 周（月三）</strong>：防御区暴露练习（「在我感到 X 之后，我告诉对方这个词」）；第 13 周前后复测双卷，出层级显现对比。</li></ul>"
    + "<p class='muted'>90 天节奏：周 1–4 观察期 → 周 5–8 替换期 → 周 9–12 固化期；每轮至多两个微行为（主生课 + 主克课各一）。</p>";
  return pack;
}

function relQName(q) {
  return { resonance: "共鸣区", projection: "投射区", defense: "防御区", blank: "空白区" }[q] || q;
}
