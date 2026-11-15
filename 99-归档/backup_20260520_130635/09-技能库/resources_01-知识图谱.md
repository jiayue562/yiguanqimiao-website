# 人机协同五象限 - 知识图谱

> 🕸️ 可视化展示各体系之间的关系

---

## 🌐 核心关系图

```mermaid
graph TB
    subgraph 学术谱系
        A[Johari Window 1955] --> B[SECI 模型 1995]
        B --> C[延伸心智 1998]
        C --> D[库恩范式 1962/1970]
        D --> E[超级个体 2020s]
        E --> F[人机协同五象限 v3.0 2026]
    end
    
    subgraph 五象限模型
        F --> Q1[效率协作者]
        F --> Q2[知识拓展者]
        F --> Q3[思辨对话者]
        F --> Q4[协同探索者]
        F --> Q5[未知共创者]
    end
    
    subgraph 龙心 OS 协同
        Q2 -.协同.-> G[知识学习 Skill]
        Q3 -.协同.-> H[五色光思维 Skill]
        Q4 -.落地.-> I[知行合一 Skill]
        Q5 -.引擎.-> J[象思维 Skill]
    end
    
    subgraph 东方智慧
        K[天君臣佐使] --> F
        L[易经思维] --> Q5
        M[五行人格] --> F
    end
    
    style Q5 fill:#ff6b6b,color:#fff
    style F fill:#4ecdc4,color:#fff
```

---

## 📊 五象限价值递进图

```mermaid
graph LR
    Q1[效率协作者<br/>执行提效] --> Q2[知识拓展者<br/>认知扩展]
    Q2 --> Q3[思辨对话者<br/>深度思考]
    Q3 --> Q4[协同探索者<br/>共同求解]
    Q4 --> Q5[未知共创者<br/>颠覆创新]
    
    style Q1 fill:#a8d5ba
    style Q2 fill:#95c4e8
    style Q3 fill:#f9d5a3
    style Q4 fill:#e8a8a8
    style Q5 fill:#ff6b6b,color:#fff
```

---

## 🔗 双向链接网络

```mermaid
graph TD
    subgraph 人机协同五象限
        MAIN[00-INDEX<br/>总索引]
        SKILL[SKILL.md<br/>主文档]
        THEORY[theory.md<br/>理论文档]
        PRACTICE[practice-guide.md<br/>实践指南]
    end
    
    subgraph 上游理论
        JOHARI[Johari Window]
        SECI[SECI 模型]
        EXTEND[延伸心智]
        KUHN[库恩范式]
    end
    
    subgraph 协同 Skills
        KNOW[知识学习]
        ACT[知行合一]
        IMG[象思维]
        COLOR[五色光]
    end
    
    MAIN --> SKILL
    MAIN --> THEORY
    MAIN --> PRACTICE
    
    THEORY -.引用.-> JOHARI
    THEORY -.引用.-> SECI
    THEORY -.引用.-> EXTEND
    THEORY -.引用.-> KUHN
    
    SKILL -.协同.-> KNOW
    SKILL -.落地.-> ACT
    SKILL -.引擎.-> IMG
    SKILL -.多角度.-> COLOR
    
    style MAIN fill:#4ecdc4,color:#fff
    style Q5 fill:#ff6b6b,color:#fff
```

---

## 🏷️ 标签体系

```mermaid
graph TB
    subgraph 核心标签
        CORE1[#人机协同]
        CORE2[#五象限]
        CORE3[#超级个体]
        CORE4[#象思维]
    end
    
    subgraph 象限标签
        Q1_TAG[#效率协作者]
        Q2_TAG[#知识拓展者]
        Q3_TAG[#思辨对话者]
        Q4_TAG[#协同探索者]
        Q5_TAG[#未知共创者]
    end
    
    subgraph 应用标签
        APP1[#个人成长]
        APP2[#组织创新]
        APP3[#AI 产品设计]
    end
    
    CORE1 --> Q1_TAG
    CORE1 --> Q2_TAG
    CORE1 --> Q3_TAG
    CORE1 --> Q4_TAG
    CORE1 --> Q5_TAG
    
    CORE2 --> Q1_TAG
    CORE2 --> Q2_TAG
    CORE2 --> Q3_TAG
    CORE2 --> Q4_TAG
    CORE2 --> Q5_TAG
    
    Q5_TAG --> APP1
    Q5_TAG --> APP2
    Q5_TAG --> APP3
    
    style CORE4 fill:#ff6b6b,color:#fff
    style Q5_TAG fill:#ff6b6b,color:#fff
```

---

## 📁 文件关系图

```mermaid
graph TB
    ROOT[人机协同五象限/]
    
    ROOT --> INDEX[00-INDEX.md<br/>总索引]
    ROOT --> SKILL[SKILL.md<br/>主文档]
    ROOT --> CHECK[CHECKLIST.md<br/>检查清单]
    ROOT --> COMP[COMPLETION_REPORT.md<br/>完成报告]
    
    ROOT --> REF[references/]
    REF --> THEORY[theory.md]
    REF --> PRACTICE[practice-guide.md]
    REF --> PROMPTS[prompts.md]
    REF --> SOP[sop.md]
    
    ROOT --> TMP[templates/]
    TMP --> IO[io-templates.md]
    TMP --> WF[workflow-template.md]
    
    ROOT --> TRG[triggers/]
    TRG --> RULES[trigger-rules.yaml]
    TRG --> ROUTES[skill-routes.yaml]
    TRG --> AUTO[auto-activate.json]
    
    style INDEX fill:#4ecdc4,color:#fff
    style SKILL fill:#4ecdc4,color:#fff
    style THEORY fill:#95c4e8
    style Q5 fill:#ff6b6b,color:#fff
```

---

## 🎯 使用导航

### 快速入口
1. **新手入门** → [[00-INDEX]] → [[theory]]
2. **立即使用** → [[SKILL]] → 触发词
3. **深度实践** → [[practice-guide]] → [[prompts]]
4. **配置规则** → [[trigger-rules]] → [[skill-routes]]

### 学习路径
```
00-INDEX (总览)
    ↓
theory (理论完整理解)
    ↓
practice-guide (实践指南)
    ↓
prompts (提示词模板)
    ↓
io-templates (实战应用)
```

---

## 🔄 知识流动

```mermaid
graph LR
    subgraph 三库同步
        AGENTS[~/.agents/skills/]
        OpcClaw[OpcClaw 知识库]
        Obsidian[Obsidian Vault]
        IMA[IMA 云端]
    end
    
    AGENTS -->|Step 17| OpcClaw
    AGENTS -->|Step 18| Obsidian
    Obsidian -->|sync-all.ps1| IMA
    
    style AGENTS fill:#4ecdc4,color:#fff
    style OpcClaw fill:#95c4e8
    style Obsidian fill:#a8d5ba
    style IMA fill:#f9d5a3
```

---

_知识图谱完成 · 2026-04-16 · 龙心 OS 人机协同五象限 Skill v3.0_
