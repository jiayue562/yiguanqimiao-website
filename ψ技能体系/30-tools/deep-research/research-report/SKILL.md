---
name: deep-research-report
user-invocable: true
description: 灏哾eep璋冪爺缁撴灉姹囨€讳负markdown鎶ュ憡锛岃鐩栨墍鏈夊瓧娈碉紝璺宠繃涓嶇‘瀹氬€笺€?allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Research Report - 姹囨€绘姤鍛?
## 瑙﹀彂鏂瑰紡
`/research-report`

## 鎵ц娴佺▼

### Step 1: 瀹氫綅缁撴灉鐩綍
鍦ㄥ綋鍓嶅伐浣滅洰褰曟煡鎵?`*/outline.yaml`锛岃鍙杢opic鍜宱utput_dir閰嶇疆銆?
### Step 2: 鎵弿鍙€夋憳瑕佸瓧娈?璇诲彇鎵€鏈塉SON缁撴灉锛屾彁鍙栭€傚悎鍦ㄧ洰褰曚腑鏄剧ず鐨勫瓧娈碉紙鏁板€煎瀷銆佺畝鐭寚鏍囷級锛屼緥濡傦細
- github_stars
- google_scholar_cites
- swe_bench_score
- user_scale
- valuation
- release_date

浣跨敤AskUserQuestion璇㈤棶鐢ㄦ埛锛?- 鐩綍涓櫎浜唅tem鍚嶇О澶栵紝杩橀渶瑕佹樉绀哄摢浜涘瓧娈碉紵
- 鎻愪緵鍔ㄦ€侀€夐」鍒楄〃锛堝熀浜庡疄闄匤SON涓瓨鍦ㄧ殑瀛楁锛?
### Step 3: 鐢熸垚Python杞崲鑴氭湰
鍦?`{topic}/` 鐩綍涓嬬敓鎴?`generate_report.py`锛岃剼鏈姹傦細
- 璇诲彇output_dir涓嬫墍鏈塉SON
- 璇诲彇fields.yaml鑾峰彇瀛楁缁撴瀯
- 瑕嗙洊姣忎釜JSON鐨勬墍鏈夊瓧娈靛€?- 璺宠繃鍊煎寘鍚玔涓嶇‘瀹歖鐨勫瓧娈?- 璺宠繃uncertain鏁扮粍涓垪鍑虹殑瀛楁
- 鐢熸垚markdown鎶ュ憡鏍煎紡锛氱洰褰曪紙甯﹂敋鐐硅烦杞?鐢ㄦ埛閫夋嫨鐨勬憳瑕佸瓧娈碉級+ 璇︾粏鍐呭锛堟寜瀛楁鍒嗙被锛?- 淇濆瓨鍒?`{topic}/report.md`

**鐩綍鏍煎紡瑕佹眰**锛?- 蹇呴』鍖呭惈姣忎竴涓猧tem
- 姣忎釜item鏄剧ず锛氬簭鍙枫€佸悕绉帮紙閿氱偣閾炬帴锛夈€佺敤鎴烽€夋嫨鐨勬憳瑕佸瓧娈?- 绀轰緥锛歚1. [GitHub Copilot](#github-copilot) - Stars: 10k | Score: 85%`

#### 鑴氭湰鎶€鏈鐐癸紙蹇呴』閬靛惊锛?
**1. JSON缁撴瀯鍏煎**
鏀寔涓ょJSON缁撴瀯锛?- 鎵佸钩缁撴瀯锛氬瓧娈电洿鎺ュ湪椤跺眰 `{"name": "xxx", "release_date": "xxx"}`
- 宓屽缁撴瀯锛氬瓧娈靛湪category瀛恉ict涓?`{"basic_info": {"name": "xxx"}, "technical_features": {...}}`

瀛楁鏌ユ壘椤哄簭锛氶《灞?-> category鏄犲皠key -> 閬嶅巻鎵€鏈夊祵濂梔ict

**2. Category澶氳瑷€鏄犲皠**
fields.yaml鐨刢ategory鍚嶄笌JSON鐨刱ey鍙兘鏄换鎰忕粍鍚堬紙涓腑銆佷腑鑻便€佽嫳涓€佽嫳鑻憋級銆傚繀椤诲缓绔嬪弻鍚戞槧灏勶細
```python
CATEGORY_MAPPING = {
    "鍩烘湰淇℃伅": ["basic_info", "鍩烘湰淇℃伅"],
    "鎶€鏈壒鎬?: ["technical_features", "technical_characteristics", "鎶€鏈壒鎬?],
    "鎬ц兘鎸囨爣": ["performance_metrics", "performance", "鎬ц兘鎸囨爣"],
    "閲岀▼纰戞剰涔?: ["milestone_significance", "milestones", "閲岀▼纰戞剰涔?],
    "鍟嗕笟淇℃伅": ["business_info", "commercial_info", "鍟嗕笟淇℃伅"],
    "绔炰簤涓庣敓鎬?: ["competition_ecosystem", "competition", "绔炰簤涓庣敓鎬?],
    "鍘嗗彶娌块潻": ["history", "鍘嗗彶娌块潻"],
    "甯傚満瀹氫綅": ["market_positioning", "market", "甯傚満瀹氫綅"],
}
```

**3. 澶嶆潅鍊兼牸寮忓寲**
- list of dicts锛堝key_events, funding_history锛夛細姣忎釜dict鏍煎紡鍖栦负涓€琛岋紝鐢╜ | `鍒嗛殧kv
- 鏅€歭ist锛氱煭鍒楄〃鐢ㄩ€楀彿杩炴帴锛岄暱鍒楄〃鎹㈣鏄剧ず
- 宓屽dict锛氶€掑綊鏍煎紡鍖栵紝鐢ㄥ垎鍙锋垨鎹㈣鏄剧ず
- 闀挎枃鏈瓧绗︿覆锛堣秴杩?00瀛楃锛夛細娣诲姞鎹㈣绗<br>`鎴栦娇鐢╞lockquote鏍煎紡锛屾彁楂樺彲璇绘€?
**4. 棰濆瀛楁鏀堕泦**
鏀堕泦JSON涓湁浣唂ields.yaml涓病瀹氫箟鐨勫瓧娈碉紝鏀惧叆"鍏朵粬淇℃伅"鍒嗙被銆傛敞鎰忚繃婊わ細
- 鍐呴儴瀛楁锛歚_source_file`, `uncertain`
- 宓屽缁撴瀯椤剁骇key锛歚basic_info`, `technical_features`绛?- `uncertain`鏁扮粍锛氶渶瑕侀€愯鏄剧ず姣忎釜瀛楁鍚嶏紝涓嶈鍘嬬缉鎴愪竴琛?
**5. 涓嶇‘瀹氬€艰烦杩?*
璺宠繃鏉′欢锛?- 瀛楁鍊煎寘鍚玚[涓嶇‘瀹歖`瀛楃涓?- 瀛楁鍚嶅湪`uncertain`鏁扮粍涓?- 瀛楁鍊间负None鎴栫┖瀛楃涓?
### Step 4: 鎵ц鑴氭湰
杩愯 `python {topic}/generate_report.py`

## 杈撳嚭
- `{topic}/generate_report.py` - 杞崲鑴氭湰
- `{topic}/report.md` - 姹囨€绘姤鍛?

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[01-核心体系/龙心OS_联合进化系统深度解析-两套Skills关系]] — 联合进化系统深度解析：两套Skills的关系与运作机制
- [[09-技能库/llmification-knowledge-builder/references/practice-guide]] — Practice Guide.md - LLMification 实操指南
- [[09-技能库/resources_LLM-Wiki 知识库建设]] — LLM Wiki 鐭ヨ瘑搴撳缓璁?- 鐭ヨ瘑瀛︿範鎶ュ憡
- [[09-技能库/岗位智能体/v2.0/学习笔记]] — 岗位智能体 v1.0 → v2.0 改造清单 · 深度学习笔记
- [[ψ技能体系/20-claws/00-wuxing/土行人分智能体/references/theory]] — 鍦熻浜烘€ф牸鐗瑰緛鍏ㄨ锛氱悊璁恒€佺淮搴︺€佸疄璺典笌鍗囧崕
- [[ψ技能体系/20-claws/00-wuxing/水行人分智能体/references/theory]] — 姘磋浜虹鏍艰涓烘ā鍨嬶紙B=MAP锛夋繁搴︽暣鍚?
- [[ψ技能体系/30-tools/deep-research/research-add-items/SKILL]] — Research Add Items - 琛ュ厖璋冪爺瀵硅薄
- [[ψ技能体系/30-tools/deep-research/research/SKILL]] — Research Skill - 鍒濇璋冪爺

<!-- AI-LINKS-END -->
