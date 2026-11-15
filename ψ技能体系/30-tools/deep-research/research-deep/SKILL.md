---
name: deep-research-deep
user-invocable: true
description: 璇诲彇璋冪爺outline锛屼负姣忎釜item鍚姩鐙珛agent杩涜娣卞害璋冪爺銆傜鐢╰ask output銆?allowed-tools: Bash, Read, Write, Glob, WebSearch, Task
---

# Research Deep - 娣卞害璋冪爺

## 瑙﹀彂鏂瑰紡
`/research-deep`

## 鎵ц娴佺▼

### Step 1: 鑷姩瀹氫綅Outline
鍦ㄥ綋鍓嶅伐浣滅洰褰曟煡鎵?`*/outline.yaml` 鏂囦欢锛岃鍙杋tems鍒楄〃銆乪xecution閰嶇疆锛堝惈items_per_agent锛夈€?
### Step 2: 鏂偣缁紶妫€鏌?- 妫€鏌utput_dir涓嬪凡瀹屾垚鐨凧SON鏂囦欢
- 璺宠繃宸插畬鎴愮殑items

### Step 3: 鍒嗘壒鎵ц
- 鎸塨atch_size鍒嗘壒锛堝畬鎴愪竴鎵归渶瑕佸緱鍒扮敤鎴峰悓鎰忔墠鍙繘琛屼笅涓€鎵癸級
- 姣忎釜agent璐熻矗items_per_agent涓」鐩?- 鍚姩web-search-agent锛堝悗鍙板苟琛岋紝绂佺敤task output锛?
**鍙傛暟鑾峰彇**锛?- `{topic}`: outline.yaml涓殑topic瀛楁
- `{item_name}`: item鐨刵ame瀛楁
- `{item_related_info}`: item鐨勫畬鏁磞aml鍐呭锛坣ame + category + description绛夛級
- `{output_dir}`: outline.yaml涓璭xecution.output_dir锛堥粯璁?/results锛?- `{fields_path}`: {topic}/fields.yaml鐨勭粷瀵硅矾寰?- `{output_path}`: {output_dir}/{item_name_slug}.json鐨勭粷瀵硅矾寰勶紙slugify澶勭悊item_name锛氱┖鏍兼浛鎹负_锛岀Щ闄ょ壒娈婂瓧绗︼級

**纭害鏉?*锛氫互涓媝rompt蹇呴』涓ユ牸澶嶈堪锛屼粎鏇挎崲{xxx}涓殑鍙橀噺锛岀姝㈡敼鍐欑粨鏋勬垨鎺緸銆?
**Prompt妯℃澘**锛?```python
prompt = f"""## 浠诲姟
璋冪爺 {item_related_info}锛岃緭鍑虹粨鏋勫寲JSON鍒?{output_path}

## 瀛楁瀹氫箟
璇诲彇 {fields_path} 鑾峰彇鎵€鏈夊瓧娈靛畾涔?
## 杈撳嚭瑕佹眰
1. 鎸塮ields.yaml瀹氫箟鐨勫瓧娈佃緭鍑篔SON
2. 涓嶇‘瀹氱殑瀛楁鍊兼爣娉╗涓嶇‘瀹歖
3. JSON鏈熬娣诲姞uncertain鏁扮粍锛屽垪鍑烘墍鏈変笉纭畾鐨勫瓧娈靛悕
4. 鎵€鏈夊瓧娈靛€煎繀椤讳娇鐢ㄤ腑鏂囪緭鍑猴紙璋冪爺杩囩▼鍙敤鑻辨枃锛屼絾鏈€缁圝SON鍊间负涓枃锛?
## 杈撳嚭璺緞
{output_path}

## 楠岃瘉
瀹屾垚JSON杈撳嚭鍚庯紝杩愯楠岃瘉鑴氭湰纭繚瀛楁瀹屾暣瑕嗙洊锛?python ~/.claude/skills/research/validate_json.py -f {fields_path} -j {output_path}
楠岃瘉閫氳繃鍚庢墠绠楀畬鎴愪换鍔°€?"""
```

**One-shot绀轰緥**锛堝亣璁捐皟鐮擥itHub Copilot锛夛細
```
## 浠诲姟
璋冪爺 name: GitHub Copilot
category: 鍥介檯浜у搧
description: Microsoft/GitHub寮€鍙戯紝棣栦釜涓绘祦AI缂栫▼鍔╂墜锛屽競鍦轰唤棰濈害40%锛岃緭鍑虹粨鏋勫寲JSON鍒?/home/weizhena/AIcoding/aicoding-history/results/GitHub_Copilot.json

## 瀛楁瀹氫箟
璇诲彇 /home/weizhena/AIcoding/aicoding-history/fields.yaml 鑾峰彇鎵€鏈夊瓧娈靛畾涔?
## 杈撳嚭瑕佹眰
1. 鎸塮ields.yaml瀹氫箟鐨勫瓧娈佃緭鍑篔SON
2. 涓嶇‘瀹氱殑瀛楁鍊兼爣娉╗涓嶇‘瀹歖
3. JSON鏈熬娣诲姞uncertain鏁扮粍锛屽垪鍑烘墍鏈変笉纭畾鐨勫瓧娈靛悕
4. 鎵€鏈夊瓧娈靛€煎繀椤讳娇鐢ㄤ腑鏂囪緭鍑猴紙璋冪爺杩囩▼鍙敤鑻辨枃锛屼絾鏈€缁圝SON鍊间负涓枃锛?
## 杈撳嚭璺緞
/home/weizhena/AIcoding/aicoding-history/results/GitHub_Copilot.json

## 楠岃瘉
瀹屾垚JSON杈撳嚭鍚庯紝杩愯楠岃瘉鑴氭湰纭繚瀛楁瀹屾暣瑕嗙洊锛?python ~/.claude/skills/research/validate_json.py -f /home/weizhena/AIcoding/aicoding-history/fields.yaml -j /home/weizhena/AIcoding/aicoding-history/results/GitHub_Copilot.json
楠岃瘉閫氳繃鍚庢墠绠楀畬鎴愪换鍔°€?```

### Step 4: 绛夊緟涓庣洃鎺?- 绛夊緟褰撳墠鎵规瀹屾垚
- 鍚姩涓嬩竴鎵?- 鏄剧ず杩涘害

### Step 5: 姹囨€绘姤鍛?鍏ㄩ儴瀹屾垚鍚庤緭鍑猴細
- 瀹屾垚鏁伴噺
- 澶辫触/涓嶇‘瀹氭爣璁扮殑items
- 杈撳嚭鐩綍

## Agent閰嶇疆
- 鍚庡彴鎵ц: 鏄?- Task Output: 绂佺敤锛坅gent瀹屾垚鏃舵湁鏄庣‘杈撳嚭鏂囦欢锛?- 鏂偣缁紶: 鏄?

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[02-信仰文化体系/躯体系统_Harness Engineering核心内容深度解析]] — Harness Engineering核心内容深度解析
- [[09-技能库/resources_LLM-Wiki 知识库建设]] — LLM Wiki 鐭ヨ瘑搴撳缓璁?- 鐭ヨ瘑瀛︿範鎶ュ憡
- [[09-技能库/resources_MECE 原则与金字塔原理]] — MECE 鍘熷垯涓庨噾瀛楀鍘熺悊 - 鐭ヨ瘑瀛︿範鎶ュ憡
- [[ψ技能体系/20-claws/00-wuxing/五行人格心理学/references/理论体系]] — 鏍稿績鐞嗚浣撶郴 - 涓€蹇冧笁鐣屼簲琛屼節灞傝薄鎬濈淮浣撶郴
- [[ψ技能体系/20-claws/00-wuxing/土行人分智能体/references/theory]] — 鍦熻浜烘€ф牸鐗瑰緛鍏ㄨ锛氱悊璁恒€佺淮搴︺€佸疄璺典笌鍗囧崕
- [[ψ技能体系/20-claws/00-wuxing/火行人分智能体/references/theory]] — 鐏浜哄垎鏅鸿兘浣撹浆鍖栨妧鏈畬鏁存寚鍗?
- [[ψ技能体系/30-tools/deep-research/research-add-fields/SKILL]] — Research Add Fields - 琛ュ厖璋冪爺瀛楁
- [[ψ技能体系/30-tools/deep-research/research-add-items/SKILL]] — Research Add Items - 琛ュ厖璋冪爺瀵硅薄
- [[ψ技能体系/30-tools/deep-research/research/SKILL]] — Research Skill - 鍒濇璋冪爺

<!-- AI-LINKS-END -->
