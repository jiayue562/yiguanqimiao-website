---
name: deep-research-research
user-invocable: true
allowed-tools: Read, Write, Glob, WebSearch, Task, AskUserQuestion
description: 瀵圭洰鏍囪瘽棰樿繘琛屽垵姝ヨ皟鐮旓紝鐢熸垚璋冪爺outline銆傜敤浜庡鏈皟鐮斻€乥enchmark璋冪爺銆佹妧鏈€夊瀷绛夊満鏅€?---

# Research Skill - 鍒濇璋冪爺

## 瑙﹀彂鏂瑰紡
`/research <topic>`

## 鎵ц娴佺▼

### Step 1: 妯″瀷鍐呴儴鐭ヨ瘑鐢熸垚鍒濇妗嗘灦
鍩轰簬topic锛屽埄鐢ㄦā鍨嬪凡鏈夌煡璇嗙敓鎴愶細
- 璇ラ鍩熺殑涓昏鐮旂┒瀵硅薄/items鍒楄〃
- 寤鸿鐨勮皟鐮斿瓧娈垫鏋?
杈撳嚭{step1_output}锛屼娇鐢ˋskUserQuestion纭锛?- items鍒楄〃鏄惁闇€瑕佸鍑忥紵
- 瀛楁妗嗘灦鏄惁婊¤冻闇€姹傦紵

### Step 2: Web Search琛ュ厖
浣跨敤AskUserQuestion璇㈤棶鏃堕棿鑼冨洿锛堝锛氭渶杩?涓湀銆?024骞磋嚦浠娿€佷笉闄愶級銆?
**鍙傛暟鑾峰彇**锛?- `{topic}`: 鐢ㄦ埛杈撳叆鐨勮皟鐮旇瘽棰?- `{YYYY-MM-DD}`: 褰撳墠鏃ユ湡
- `{step1_output}`: Step 1鐢熸垚鐨勫畬鏁磋緭鍑哄唴瀹?- `{time_range}`: 鐢ㄦ埛鎸囧畾鐨勬椂闂磋寖鍥?
**纭害鏉?*锛氫互涓媝rompt蹇呴』涓ユ牸澶嶈堪锛屼粎鏇挎崲{xxx}涓殑鍙橀噺锛岀姝㈡敼鍐欑粨鏋勬垨鎺緸銆?
鍚姩1涓獁eb-search-agent锛堝悗鍙帮級锛?*Prompt妯℃澘**锛?```python
prompt = f"""## 浠诲姟
璋冪爺璇濋: {topic}
褰撳墠鏃ユ湡: {YYYY-MM-DD}

鍩轰簬浠ヤ笅鍒濇妗嗘灦锛岃ˉ鍏呮渶鏂癷tems鍜屾帹鑽愯皟鐮斿瓧娈点€?
## 宸叉湁妗嗘灦
{step1_output}

## 鐩爣
1. 楠岃瘉宸叉湁items鏄惁閬楁紡閲嶈瀵硅薄
2. 鏍规嵁閬楁紡瀵硅薄杩涜琛ュ厖items
3. 缁х画鎼滅储{topic}鐩稿叧涓攞time_range}鍐呯殑items骞惰ˉ鍏?4. 琛ュ厖鏂癴ields

## 杈撳嚭瑕佹眰
鐩存帴杩斿洖缁撴瀯鍖栫粨鏋滐紙涓嶅啓鏂囦欢锛夛細

### 琛ュ厖Items
- item_name: 绠€瑕佽鏄庯紙涓轰粈涔堝簲璇ュ姞鍏ワ級
...

### 鎺ㄨ崘琛ュ厖瀛楁
- field_name: 瀛楁鎻忚堪锛堜负浠€涔堥渶瑕佽繖涓淮搴︼級
...

### 淇℃伅鏉ユ簮
- [鏉ユ簮1](url1)
- [鏉ユ簮2](url2)
"""
```

**One-shot绀轰緥**锛堝亣璁捐皟鐮擜I Coding鍙戝睍鍙诧級锛?```
## 浠诲姟
璋冪爺璇濋: AI Coding 鍙戝睍鍙?褰撳墠鏃ユ湡: 2025-12-30

鍩轰簬浠ヤ笅鍒濇妗嗘灦锛岃ˉ鍏呮渶鏂癷tems鍜屾帹鑽愯皟鐮斿瓧娈点€?
## 宸叉湁妗嗘灦
### Items鍒楄〃
1. GitHub Copilot: Microsoft/GitHub寮€鍙戯紝棣栦釜涓绘祦AI缂栫▼鍔╂墜
2. Cursor: AI-first IDE锛屽熀浜嶸SCode
...

### 瀛楁妗嗘灦
- 鍩烘湰淇℃伅: name, release_date, company
- 鎶€鏈壒鎬? underlying_model, context_window
...

## 鐩爣
1. 楠岃瘉宸叉湁items鏄惁閬楁紡閲嶈瀵硅薄
2. 鏍规嵁閬楁紡瀵硅薄杩涜琛ュ厖items
3. 缁х画鎼滅储AI Coding 鍙戝睍鍙茬浉鍏充笖2024骞磋嚦浠婂唴鐨刬tems骞惰ˉ鍏?4. 琛ュ厖鏂癴ields

## 杈撳嚭瑕佹眰
鐩存帴杩斿洖缁撴瀯鍖栫粨鏋滐紙涓嶅啓鏂囦欢锛夛細

### 琛ュ厖Items
- item_name: 绠€瑕佽鏄庯紙涓轰粈涔堝簲璇ュ姞鍏ワ級
...

### 鎺ㄨ崘琛ュ厖瀛楁
- field_name: 瀛楁鎻忚堪锛堜负浠€涔堥渶瑕佽繖涓淮搴︼級
...

### 淇℃伅鏉ユ簮
- [鏉ユ簮1](url1)
- [鏉ユ簮2](url2)
```

### Step 3: 璇㈤棶鐢ㄦ埛宸叉湁瀛楁
浣跨敤AskUserQuestion璇㈤棶鐢ㄦ埛鏄惁鏈夊凡瀹氫箟鐨勫瓧娈垫枃浠讹紝濡傛湁鍒欒鍙栧苟鍚堝苟銆?
### Step 4: 鐢熸垚Outline锛堝垎绂绘枃浠讹級
鍚堝苟{step1_output}銆亄step2_output}鍜岀敤鎴峰凡鏈夊瓧娈碉紝鐢熸垚涓や釜鏂囦欢锛?
**outline.yaml**锛坕tems + 閰嶇疆锛夛細
- topic: 璋冪爺涓婚
- items: 璋冪爺瀵硅薄鍒楄〃
- execution:
  - batch_size: 骞惰agent鏁伴噺锛堥渶AskUserQuestion纭锛?  - items_per_agent: 姣忎釜agent璋冪爺椤圭洰鏁帮紙闇€AskUserQuestion纭锛?  - output_dir: 缁撴灉杈撳嚭鐩綍锛堥粯璁?/results锛?
**fields.yaml**锛堝瓧娈靛畾涔夛級锛?- 瀛楁鍒嗙被鍜屽畾涔?- 姣忎釜瀛楁鐨刵ame銆乨escription銆乨etail_level
- detail_level鍒嗗眰锛氭瀬绠€ 鈫?绠€瑕?鈫?璇︾粏
- uncertain: 涓嶇‘瀹氬瓧娈靛垪琛紙淇濈暀瀛楁锛宒eep闃舵鑷姩濉厖锛?
### Step 5: 杈撳嚭骞剁‘璁?- 鍒涘缓鐩綍: `./{topic_slug}/`
- 淇濆瓨: `outline.yaml` 鍜?`fields.yaml`
- 灞曠ず缁欑敤鎴风‘璁?
## 杈撳嚭璺緞
```
{褰撳墠宸ヤ綔鐩綍}/{topic_slug}/
  鈹溾攢鈹€ outline.yaml    # items鍒楄〃 + execution閰嶇疆
  鈹斺攢鈹€ fields.yaml     # 瀛楁瀹氫箟
```

## 鍚庣画鍛戒护
- `/research-add-items` - 琛ュ厖items
- `/research-add-fields` - 琛ュ厖瀛楁
- `/research-deep` - 寮€濮嬫繁搴﹁皟鐮?

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[ψ技能体系/20-claws/00-wuxing/五行人格心理学/references/理论体系]] — 鏍稿績鐞嗚浣撶郴 - 涓€蹇冧笁鐣屼簲琛屼節灞傝薄鎬濈淮浣撶郴
- [[ψ技能体系/30-tools/deep-research/research-add-fields/SKILL]] — Research Add Fields - 琛ュ厖璋冪爺瀛楁
- [[ψ技能体系/30-tools/deep-research/research-add-items/SKILL]] — Research Add Items - 琛ュ厖璋冪爺瀵硅薄
- [[ψ技能体系/30-tools/deep-research/research-deep/SKILL]] — Research Deep - 娣卞害璋冪爺
- [[ψ技能体系/30-tools/deep-research/research-report/SKILL]] — Research Report - 姹囨€绘姤鍛?
- [[ψ技能体系/30-tools/fbs-bookwriter/scripts/agents/fbs-writer]] — FBS Writer Agent

<!-- AI-LINKS-END -->
