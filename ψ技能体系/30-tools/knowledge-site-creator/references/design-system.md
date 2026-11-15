# 知识学习网站 - 设计系统参考

> 从 word-root-workshop 提取的设计规范，供AI生成新页面时参考

## 1. 设计风格

**极简主义（Minimalism）**：
- Less is More，去除一切多余元素
- 清晰的视觉层级，专注内容本身
- 大留白，呼吸感

## 2. 配色方案

```css
:root {
  /* 主色 */
  --color-accent: #FBBF24;           /* 黄色主题色 */
  --color-accent-dark: #F59E0B;      /* 深黄色（hover） */

  /* 状态色 */
  --color-success: #10B981;          /* 绿色（成功/已掌握） */
  --color-error: #EF4444;            /* 红色（错误/警告） */

  /* 文字 */
  --color-text: #0F172A;             /* 深灰主文字 */
  --color-text-secondary: #64748B;   /* 次要文字 */
  --color-text-tertiary: #94A3B8;    /* 三级文字 */

  /* 背景 */
  --color-bg: #FFFFFF;               /* 白色背景 */
  --color-bg-secondary: #F8FAFC;     /* 浅灰背景 */
  --color-bg-hover: #F8FAFC;         /* hover背景 */

  /* 边框 */
  --color-border: #E2E8F0;           /* 边框颜色 */
}
```

## 3. 字体系统

```css
/* 字体族 */
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* 代码/术语字体 */
font-family: 'Courier New', monospace;

/* 标题 */
h1 { font-size: 3rem; font-weight: 700; }      /* 48px */
h2 { font-size: 2rem; font-weight: 600; }      /* 32px */
h3 { font-size: 1.5rem; font-weight: 600; }    /* 24px */

/* 正文 */
body { font-size: 1rem; line-height: 1.6; }    /* 16px */
```

## 4. 间距系统（8px网格）

```css
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;
--space-4xl: 96px;
```

## 5. 阴影系统（极浅）

```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.02);
--shadow-md: 0 2px 8px 0 rgba(0, 0, 0, 0.04);
--shadow-lg: 0 4px 16px 0 rgba(0, 0, 0, 0.06);
```

## 6. 圆角

```css
--radius: 8px;        /* 小圆角 */
--radius-lg: 12px;    /* 大圆角 */
```

## 7. 过渡动画

```css
--transition: 200ms cubic-bezier(0.4, 0, 0.2, 1);
```

## 8. 组件样式

### 8.1 按钮

```css
.btn {
  padding: 12px 24px;
  border-radius: var(--radius);
  font-weight: 600;
  transition: var(--transition);
  cursor: pointer;
  border: none;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-text);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
}

.btn-large {
  padding: 16px 32px;
  font-size: 1.125rem;
}
```

### 8.2 卡片

```css
.card {
  background: white;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: var(--transition);
}

.card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-md);
}
```

### 8.3 标签和徽章 🆕

**分类标签**（origin标签）：
```css
.root-origin {
  display: inline-block;
  background: var(--color-accent);     /* 黄色主题色 */
  color: var(--color-text);
  padding: 4px 12px;
  border-radius: var(--radius-sm);
  font-size: 14px;
  margin-top: var(--spacing-xs);
}
```

**已掌握徽章**（mastered-badge）：
```css
.mastered-badge {
  display: inline-block;
  background: var(--color-success);    /* 绿色，区分于分类标签 */
  color: #FFFFFF;                      /* 白色文字 */
  padding: 2px 8px;
  border-radius: var(--radius-sm);
  font-size: 12px;
  margin-top: var(--spacing-xs);
  margin-left: var(--spacing-xs);      /* 与前面的标签保持间距 */
}
```

**设计原则**：
- ✅ 使用不同颜色区分功能（黄色=分类，绿色=状态）
- ✅ 添加左边距避免拥挤（`margin-left: 8px`）
- ✅ 文字清晰明确（"✓ 已掌握" 而不是只有 "✓"）

### 8.4 导航栏

```css
.nav {
  border-bottom: 1px solid var(--color-border);
  padding: 16px 0;
  background: white;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.nav-brand {
  font-weight: 600;
  color: var(--color-text);
  font-size: 1.125rem;
  text-decoration: none;          /* 移除下划线 */
  transition: color 0.2s;
}

.nav-brand:hover {
  color: var(--color-primary-dark);  /* 悬停变色 */
}

.nav-link {
  color: var(--color-text-secondary);
  font-weight: 500;
  transition: var(--transition);
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-text);
}
```

**⚠️ 重要**：`.nav-brand` 必须是 `<a href="/">` 链接，不是 `<div>`，点击可回到首页。

## 9. 布局模式

### 9.1 Hero区（首页）

```css
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4xl) 0;  /* 96px 垂直留白 */
  text-align: center;
}

.hero-title {
  font-size: 4rem;              /* 64px */
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin-bottom: var(--space-lg);
}

.hero-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-2xl);
}
```

### 9.2 统计卡片（3列网格）

```css
.stat-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-xl);
  margin: var(--space-4xl) 0;
}

.stat-card {
  text-align: center;
  padding: var(--space-2xl);
}

.stat-value {
  font-size: 3rem;
  font-weight: 700;
  color: var(--color-text);
}

.stat-label {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-top: var(--space-sm);
}
```

### 9.3 内容容器

```css
.container {
  max-width: 800px;      /* 主要内容最大宽度 */
  margin: 0 auto;
  padding: 0 var(--space-lg);
}

.container-wide {
  max-width: 1200px;     /* 宽版容器 */
}
```

## 10. 响应式断点

```css
/* Mobile */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .stat-grid {
    grid-template-columns: 1fr;
    gap: var(--space-lg);
  }
}
```

## 11. 使用原则

1. **颜色使用**：
   - 主题色（黄色）：主要CTA、重点元素、hover状态
   - 灰色系：文字、边框、背景
   - 避免过多颜色，保持极简

2. **间距使用**：
   - 遵循8px网格系统
   - 组件内间距：16px-24px
   - 组件间间距：32px-48px
   - 页面留白：96px

3. **阴影使用**：
   - 极浅阴影，不要太重
   - 仅用于卡片、按钮hover等需要层次感的地方

4. **圆角使用**：
   - 小元素（按钮、标签）：8px
   - 大元素（卡片、容器）：12px

5. **动画使用**：
   - 使用统一的过渡时间（200ms）
   - hover效果：轻微上移 + 阴影
   - 避免过度动画

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/龙脑-思维模型顶层设计/02-思维模型/10-思维结构类/十方破局：0到10维思维框架]] — 十方破局：0到10维思维框架
- [[20-工作记录与复盘/journal_2026-03-22_方法论沉淀]] — 方法论沉淀 - 2026-03-22
- [[09-技能库/岗位智能体/v3.0/visual-spec]] — 岗位智能体 · HTML输出视觉设计规范
- [[ψ技能体系/20-claws/02-culture/品牌调性/隐秘联系集_v1.0]] — 味藏品牌调性 - 隐秘联系集
- [[ψ技能体系/20-claws/02-culture/品牌调性/龙心OS深度学习白皮书_v1.0]] — 味藏品牌调性智能体
- [[ψ技能体系/30-tools/fbs-bookwriter/references/03-product/NS08213-06-typography]] — 中文排版规范
- [[ψ技能体系/30-tools/knowledge-site-creator/README]] — Knowledge Site Creator
- [[ψ技能体系/30-tools/knowledge-site-creator/SKILL]] — Knowledge Site Creator - 通用知识学习网站生成器

<!-- AI-LINKS-END -->
