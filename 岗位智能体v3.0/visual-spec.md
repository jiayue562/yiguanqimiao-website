# 岗位智能体 · HTML输出视觉设计规范

> **版本**：v1.0 | **创建日期**：2026-05-18 | **维护者**：龙龟神将  
> **定位**：龙爪HTML输出必须遵循的视觉设计规范，确保风格统一、组件复用、响应式一致

---

## 一、设计哲学

**深色顶栏 + 白色画布 + 浅灰网格 = 专注内容的视觉层次**

- 顶栏传达品牌感（深色=稳重/专业）
- 画布承载内容（白色=干净/聚焦）
- 网格提供节奏（浅灰=呼吸/分区）

---

## 二、CSS变量体系（必须遵循）

```css
:root {
  --topbar-bg: #1e293b;       /* 深色顶栏 */
  --canvas-bg: #ffffff;        /* 白色画布 */
  --grid-bg: #f5f6f8;          /* 浅灰网格 */
  --accent: #c0392b;           /* 警示红 */
  --gold: #d4a017;             /* 金标色·龙爪品牌色 */
  --green: #27ae60;            /* 达标绿 */
  --blue: #2980b9;             /* 过程蓝 */
  --orange: #e67e22;           /* 关注橙 */
  --purple: #8e44ad;           /* 特殊紫 */
  --text-primary: #2c3e50;     /* 主文字 */
  --text-secondary: #5d6d7e;   /* 副文字 */
  --text-light: #95a5a6;       /* 浅文字 */
  --border: #dce1e8;           /* 边框 */
  --card-radius: 10px;         /* 卡片圆角 */
  --card-shadow: 0 2px 12px rgba(0,0,0,0.06); /* 卡片阴影 */
}
```

---

## 三、颜色编码逻辑

| 颜色 | CSS类名 | 语义 | 使用场景 |
|------|---------|------|---------|
| 绿色 | `.tag-g` / `--green` | 达标/完成/优势 | 7S评分8-10、完成率≥100%、阳面优势 |
| 红色 | `.tag-r` / `--accent` | 预警/未达标/薄弱 | 7S评分1-4、风险指标P0、阴面风险 |
| 橙色 | `.tag-o` / `--orange` | 关注/偏弱/进行中 | 7S评分5-7、过程指标异常、待提升 |
| 蓝色 | `.tag-b` / `--blue` | 过程/监控/信息 | 过程指标、监控数据、信息展示 |
| 紫色 | `.tag-p` / `--purple` | 特殊/战略/文化 | 心文化评估、战略命题、特殊标注 |

**五色光思维映射**：
- 绿色 → 黄光思维（乐观、利益、价值）
- 红色 → 蓝光思维（困难、问题、风险）
- 橙色 → 红光思维（直觉、感受、预感）
- 蓝色 → 白光思维（数据、信息、事实）
- 紫色 → 绿光思维（创新、变革、原创）

---

## 四、通用组件库

### 4.1 顶栏 (.topbar)

```css
.topbar {
  background: var(--topbar-bg);
  color: #e8e8f0;
  padding: 0 40px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 20px rgba(0,0,0,0.15);
}
```

### 4.2 卡片 (.card)

```css
.card {
  background: var(--canvas-bg);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: 30px;
  margin-bottom: 24px;
  border: 1px solid var(--border);
}
```

### 4.3 进度条 (.progress-bar)

```css
.progress-bar {
  height: 6-8px;
  border-radius: 4px;
  background: #e9ecef;
  overflow: hidden;
}
.progress-bar .fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--green), #2ecc71);
  transition: width 1s ease-out;
}
```

**颜色规则**：
- 8-10分：`background: var(--green)` + `var(--green)` 进度条
- 5-7分：`background: var(--orange)` 进度条
- 1-4分：`background: var(--accent)` 进度条

### 4.4 仪表盘卡片 (.dash-card)

```css
.dash-card {
  background: var(--grid-bg);
  border-radius: 10px;
  padding: 18px;
  text-align: center;
}
/* 网格布局：4列 */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 14px;
}
```

**组件结构**：图标 + 标签 + 大数字 + 副文本

### 4.5 Tab切换

```css
.cal-tab {
  padding: 7px 16px;
  border-radius: 18px;
  font-size: 12.5px;
  cursor: pointer;
  border: 1.5px solid var(--border);
  background: white;
  transition: all 0.2s;
}
.cal-tab.active {
  border-color: var(--gold);
  color: var(--gold);
  background: #fffdf5;
}
```

**JS函数**：

```javascript
function switchCal(tab) {
  document.querySelectorAll('.cal-tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.cal-panel').forEach(p => p.style.display = 'none');
  tab.classList.add('active');
  document.getElementById(tab.dataset.panel).style.display = 'block';
}
```

### 4.6 标签 (.tag)

```css
.tag { display: inline-block; padding: 2px 9px; border-radius: 9px; font-size: 10.5px; font-weight: 600; }
.tag-g { background: #e8f8f0; color: var(--green); }
.tag-r { background: #fde8e8; color: var(--accent); }
.tag-o { background: #fef5e7; color: var(--orange); }
.tag-b { background: #eaf2f8; color: var(--blue); }
.tag-p { background: #f4ecf7; color: var(--purple); }
```

---

## 五、响应式断点

```css
@media (max-width: 900px) {
  /* 4列→2列 */
  .dashboard-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
  /* 全部→1列 */
  .dashboard-grid { grid-template-columns: 1fr; }
  .topbar { padding: 0 16px; }
  .card { padding: 20px 16px; }
}
```

---

## 六、交互规范

### 6.1 进度条动画

```javascript
// setTimeout渐入：页面加载后0→目标宽度的过渡动画
setTimeout(() => {
  document.querySelectorAll('.progress-bar .fill').forEach(bar => {
    bar.style.width = bar.dataset.width;
  });
}, 100);
```

### 6.2 Tab切换

```javascript
// 见4.5节的switchCal函数
```

---

## 七、校验清单

| 序号 | 检查项 | 标准 |
|------|--------|------|
| 1 | CSS变量是否全部使用 | 8个核心变量必须出现在:root中 |
| 2 | 颜色编码是否一致 | 绿=达标/红=预警/橙=关注/蓝=过程/紫=特殊 |
| 3 | 卡片样式是否统一 | 白色背景+10px圆角+阴影+1px边框 |
| 4 | 响应式是否完整 | 900px+600px两个断点 |
| 5 | 进度条是否有动画 | setTimeout渐入 |
| 6 | 7S评分颜色是否正确 | 8-10绿/5-7橙/1-4红 |
| 7 | 顶栏是否sticky | position:sticky;top:0 |
| 8 | 字体是否指定 | -apple-system, PingFang SC, Microsoft YaHei |

---

*岗位智能体 · HTML输出视觉设计规范 · v1.0 · 2026-05-18*
