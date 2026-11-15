---
name: ima-skill-notes
description: 通过 IMA OpenAPI 管理个人笔记，支持搜索、列表、读取、新建。
---

# Notes (绗旇)

> Prerequisites: see root `../SKILL.md` for setup, credentials, and `ima_api()` helper.

API base path: `openapi/note/v1`

閫氳繃 IMA OpenAPI 绠＄悊鐢ㄦ埛涓汉绗旇锛屾敮鎸佽鍙栵紙鎼滅储銆佸垪琛ㄣ€佽幏鍙栧唴瀹癸級鍜屽啓鍏ワ紙鏂板缓銆佽拷鍔狅級銆?
瀹屾暣鐨勬暟鎹粨鏋勫拰鎺ュ彛鍙傛暟璇﹁ `references/api.md`銆?
> **闅愮瑙勫垯锛?* 绗旇鍐呭灞炰簬鐢ㄦ埛闅愮锛屽湪缇よ亰鍦烘櫙涓彧灞曠ず鏍囬鍜屾憳瑕侊紝绂佹灞曠ず绗旇姝ｆ枃銆?
## 鎺ュ彛鍐崇瓥琛?
| 鐢ㄦ埛鎰忓浘                                                                                                  | 璋冪敤鎺ュ彛                     | 鍏抽敭鍙傛暟                                                                      |
| --------------------------------------------------------------------------------------------------------- | ---------------------------- | ----------------------------------------------------------------------------- |
| 鎼滅储/鏌ユ壘绗旇                                                                                             | `search_note_book`           | `query_info`锛圦ueryInfo 瀵硅薄锛?                                               |
| 鏌ョ湅绗旇鏈垪琛?                                                                                           | `list_note_folder_by_cursor` | `cursor`(蹇呭～锛岄椤典紶`"0"`) + `limit`(蹇呭～)                                   |
| 娴忚鏌愮瑪璁版湰閲岀殑绗旇,褰撶敤鎴疯〃杩?鏈€鏂?銆?鏈€杩?涔嬬被鐨勯€氱敤闄愬畾锛屾病鏈夋寚鏄庣瑪璁版湰鏃讹紝閮藉簲璇ョ洿鎺ュ湪鍏ㄩ儴绗旇閲屽幓鎷?| `list_note_by_folder_id`     | `folder_id`(閫夊～,绌轰负鍏ㄩ儴绗旇鏈? + `cursor`(蹇呭～锛岄娆′紶`""`) + `limit`(蹇呭～) |
| 璇诲彇绗旇姝ｆ枃                                                                                              | `get_doc_content`            | `doc_id` + `target_content_format`(蹇呭～锛屾帹鑽恅0`绾枃鏈?                       |
| 鏂板缓涓€绡囩瑪璁帮紙鐢ㄦ埛鏄庣‘璇?鏂板缓/鍒涘缓绗旇"鏃惰蛋姝ゆ帴鍙ｏ級                                                       | `import_doc`                 | `content` + `content_format`(蹇呭～锛屽浐瀹歚1`) + 鍙€?`folder_id`                |
| 寰€宸叉湁绗旇杩藉姞鍐呭锛堚殸锔?**鏁忔劅鎿嶄綔**锛氱敤鎴峰繀椤绘槑纭寚瀹氱洰鏍囩瑪璁帮紝鍚﹀垯鍏堢‘璁ゅ啀鎿嶄綔锛?                         | `append_doc`                 | `doc_id` + `content` + `content_format`(蹇呭～锛屽浐瀹歚1`)                        |

## 鈿狅笍 鏂板缓 vs. 杩藉姞 鈥?琛屼负瑙勫垯

**鏂板缓绗旇锛坄import_doc`锛?* 鍜?**杩藉姞鍐呭鍒板凡鏈夌瑪璁帮紙`append_doc`锛?* 鏄袱涓畬鍏ㄤ笉鍚岀殑鎿嶄綔锛屽姟蹇呮纭尯鍒嗭細

### 鏄庣‘璧版柊寤虹殑淇″彿璇?
鐢ㄦ埛璇翠互涓嬩换涓€琛ㄨ堪鏃讹紝**鐩存帴璋冪敤 `import_doc` 鍒涘缓鏂扮瑪璁?*锛?
- "**鏂板缓**绗旇"銆?**鍒涘缓**绗旇"銆?**鍐欎竴绡?*绗旇"
- "**鏂板缓**涓€绡囩瑪璁拌褰曡繖浜涘唴瀹?

### 鏄庣‘璧拌拷鍔犵殑淇″彿璇?
鐢ㄦ埛璇翠互涓嬩换涓€琛ㄨ堪鏃讹紝**璋冪敤 `append_doc` 杩藉姞鍒板凡鏈夌瑪璁?*锛堜絾浠嶉渶纭鐩爣绗旇锛岃涓嬫柟瑙勫垯锛夛細

- "鎶婅繖娈佃瘽**杩藉姞鍒?*銆奨X銆嬬瑪璁伴噷"
- "鍦ㄩ偅绡囩瑪璁?*鏈熬鍔犱笂**杩欐鍐呭"

### 妯＄硦鍦烘櫙 鈥?蹇呴』鍏堣闂敤鎴?
浠ヤ笅琛ㄨ堪**鏃㈠彲鑳芥槸鏂板缓銆佷篃鍙兘鏄拷鍔?*锛宎gent **涓嶅緱鑷鍋囪**锛屽繀椤诲厛鍚戠敤鎴风‘璁わ細

- "甯垜璁颁竴涓?銆?璁板綍涓€涓?銆?淇濆瓨涓虹瑪璁?銆?瀛樻垚绗旇"
- "鎶婅繖娈靛唴瀹硅鍒扮瑪璁伴噷"
- "娣诲姞鍒扮瑪璁伴噷"
- 浠讳綍鍏朵粬鏈槑纭〃杈?鏂板缓"鎴?杩藉姞"鎰忓浘鐨勮〃杩?
璇㈤棶绀轰緥锛?> "鎮ㄦ槸鎯?*鍒涘缓涓€绡囨柊绗旇**锛岃繕鏄?*杩藉姞鍒版煇绡囧凡鏈夌瑪璁?*锛?

### 杩藉姞鍒板凡鏈夌瑪璁版槸鏁忔劅鎿嶄綔

`append_doc` 浼?*涓嶅彲鎾ら攢鍦颁慨鏀?*鐢ㄦ埛鐨勭幇鏈夌瑪璁帮紝鍥犳蹇呴』璋ㄦ厧澶勭悊锛?
1. **鐢ㄦ埛鏄庣‘鎸囧畾浜嗙洰鏍囩瑪璁?* 鈥?鍙互鐩存帴杩藉姞銆備緥濡傦細
   - "鎶婅繖娈佃瘽杩藉姞鍒般€婁細璁邯瑕併€嬬瑪璁伴噷"
   - "鍦ㄩ偅绡囩瑪璁版湯灏惧姞涓婅繖娈靛唴瀹?锛堜笂涓嬫枃涓凡鏈夋槑纭殑绗旇瀵硅薄锛?
2. **鐢ㄦ埛娌℃湁鏄庣‘鎸囧畾鐩爣绗旇** 鈥?**蹇呴』鍏堝悜鐢ㄦ埛纭**锛屼笉瑕佽嚜琛岀寽娴嬨€備緥濡傦細
   - 鐢ㄦ埛璇?娣诲姞鍒扮瑪璁伴噷" 鈫?璇㈤棶锛?鎮ㄦ兂杩藉姞鍒板摢绡囧凡鏈夌瑪璁帮紵璇锋彁渚涚瑪璁版爣棰樻垨璁╂垜甯偍鎼滅储銆?
   - 鐢ㄦ埛璇?鎶婅繖涓姞鍒颁箣鍓嶉偅绡囩瑪璁? 鈫?濡傛灉涓婁笅鏂囦腑鏈夊绡囩瑪璁版垨涓嶇‘瀹氭槸鍝瘒 鈫?鍒楀嚭鍊欓€夌瑪璁拌鐢ㄦ埛閫夋嫨

> **鍘熷垯**锛氫笉纭畾鏃讹紝鍏堥棶銆傚畞鍙闂竴鍙ワ紝涔熶笉瑕佽鏀圭敤鎴风殑宸叉湁绗旇鎴栬嚜浣滀富寮犲垱寤烘柊绗旇銆?
### 馃柤锔?鏈湴鍥剧墖涓嶆敮鎸?
`import_doc` 鍜?`append_doc` 鐨?`content` 瀛楁浠呮敮鎸佺函鏂囨湰/Markdown锛?*涓嶆敮鎸佹湰鍦板浘鐗?*銆?
鍐欏叆绗旇鍐呭鍓嶏紝蹇呴』妫€鏌ュ苟澶勭悊鍥剧墖寮曠敤锛?
1. **杩囨护鏈湴鍥剧墖** 鈥?濡傛灉鐢ㄦ埛鎻愪緵鐨勫唴瀹逛腑鍖呭惈鏈湴鍥剧墖璺緞锛堝 `![](file:///...)`, `![](/Users/...)`, `![](C:\...)` 绛夛級锛?*绉婚櫎杩欎簺鍥剧墖寮曠敤**锛屼笉瑕佸皢鍏跺啓鍏ョ瑪璁般€?2. **鍛婄煡鐢ㄦ埛** 鈥?绉婚櫎鍚庝富鍔ㄦ彁閱掔敤鎴凤細
   > "绗旇鎺ュ彛鏆備笉鏀寔涓婁紶鏈湴鍥剧墖锛屼互涓嬪浘鐗囧凡琚繃婊わ細`xxx.png`銆乣yyy.jpg`銆傛偍鍙互鍏堝皢鍥剧墖涓婁紶鍒扮綉缁滐紝鍐嶇敤缃戠粶閾炬帴鎻掑叆绗旇銆?
3. **淇濈暀缃戠粶鍥剧墖** 鈥?浠?`http://` 鎴?`https://` 寮€澶寸殑鍥剧墖閾炬帴鍙互姝ｅ父淇濈暀銆?
## 甯哥敤宸ヤ綔娴?
### 鏌ユ壘骞堕槄璇荤瑪璁?
鍏堟悳绱㈣幏鍙?`docid`锛屽啀鐢?`get_doc_content` 璇诲彇姝ｆ枃锛?
```bash
# 1. 鎸夋爣棰樻悳绱?ima_api "openapi/note/v1/search_note_book" '{"search_type": 0, "query_info": {"title": "浼氳绾"}, "start": 0, "end": 20}'
# 浠庤繑鍥炵殑 docs[].doc.basic_info.docid 涓彇鐩爣绗旇 ID

# 2. 璇诲彇姝ｆ枃锛堢函鏂囨湰鏍煎紡锛孧arkdown 鏍煎紡鐩墠涓嶆敮鎸侊級
ima_api "openapi/note/v1/get_doc_content" '{"doc_id": "鐩爣docid", "target_content_format": 0}'
```

### 娴忚绗旇鏈噷鐨勭瑪璁?
鍏堟媺绗旇鏈垪琛ㄨ幏鍙?`folder_id`锛屽啀鎷夎绗旇鏈笅鐨勭瑪璁帮細

```bash
# 1. 鍒楀嚭绗旇鏈紙棣栭〉 cursor 浼?"0"锛?ima_api "openapi/note/v1/list_note_folder_by_cursor" '{"cursor": "0", "limit": 20}'

# 2. 鎷夊彇鎸囧畾绗旇鏈殑绗旇锛堥椤?cursor 浼?""锛?ima_api "openapi/note/v1/list_note_by_folder_id" '{"folder_id": "user_list_xxx", "cursor": "", "limit": 20}'
```

### 鏂板缓绗旇

```bash
# 鏂板缓鍒伴粯璁や綅缃?ima_api "openapi/note/v1/import_doc" '{"content_format": 1, "content": "# 鏍囬\n\n姝ｆ枃鍐呭"}'

# 鏂板缓鍒版寚瀹氱瑪璁版湰
ima_api "openapi/note/v1/import_doc" '{"content_format": 1, "content": "# 鏍囬\n\n姝ｆ枃鍐呭", "folder_id": "绗旇鏈琁D"}'
# 杩斿洖 doc_id锛屽悗缁彲鐢ㄤ簬 append_doc
```

### 杩藉姞鍐呭鍒板凡鏈夌瑪璁?
```bash
ima_api "openapi/note/v1/append_doc" '{"doc_id": "绗旇ID", "content_format": 1, "content": "\n## 琛ュ厖鍐呭\n\n杩藉姞鐨勬枃鏈?}'
```

### 鎸夋鏂囨悳绱?
```bash
ima_api "openapi/note/v1/search_note_book" '{"search_type": 1, "query_info": {"content": "椤圭洰鎺掓湡"}, "start": 0, "end": 20}'
```

## 鏍稿績鍝嶅簲瀛楁

**鎼滅储缁撴灉**锛坄SearchedDoc`锛夛細绗旇淇℃伅璺緞涓?`doc.basic_info`锛圖ocBasic锛夛紝鍏抽敭瀛楁锛歚docid`銆乣title`銆乣summary`銆乣folder_id`銆乣folder_name`銆乣create_time`锛圲nix 姣锛夈€乣modify_time`銆乣status`銆傞澶栧寘鍚?`highlight_info`锛堥珮浜尮閰嶏紝key 涓?`doc_title`锛寁alue 鍚?`<em>楂樹寒璇?/em>`锛夈€?
**绗旇鏈潯鐩?*锛坄NoteBookFolder`锛夛細淇℃伅璺緞涓?`folder.basic_info`锛圢oteBookFolderBasic锛夛紝鍏抽敭瀛楁锛歚folder_id`銆乣name`銆乣note_number`銆乣create_time`銆乣modify_time`銆乣folder_type`锛坄0`=鐢ㄦ埛鑷缓锛宍1`=鍏ㄩ儴绗旇锛宍2`=鏈垎绫伙級銆乣status`銆?
**绗旇鍒楄〃鏉＄洰**锛坄NoteBookInfo`锛夛細淇℃伅璺緞涓?`basic_info.basic_info`锛圖ocBasicInfo 鈫?DocBasic锛夛紝鍏抽敭瀛楁锛歚docid`銆乣title`銆乣summary`銆乣folder_id`銆乣folder_name`銆乣create_time`銆乣modify_time`銆乣status`銆?
**鍐欏叆缁撴灉**锛坄import_doc`/`append_doc`锛夛細杩斿洖 `doc_id`锛堟柊寤烘垨鐩爣绗旇鐨勫敮涓€ ID锛夈€?
瀹屾暣瀛楁瀹氫箟瑙?`references/api.md`銆?
## 鍒嗛〉

- **娓告爣鍒嗛〉 鈥?绗旇鏈垪琛?*锛坄list_note_folder_by_cursor`锛夛細棣栨 `cursor: "0"`锛屽悗缁敤 `next_cursor`锛宍is_end=true` 鏃跺仠姝€?- **娓告爣鍒嗛〉 鈥?绗旇鍒楄〃**锛坄list_note_by_folder_id`锛夛細棣栨 `cursor: ""`锛屽悗缁敤 `next_cursor`锛宍is_end=true` 鏃跺仠姝€?- **鍋忕Щ閲忓垎椤?*锛坄search_note_book`锛夛細棣栨 `start: 0, end: 20`锛岀炕椤垫椂閫掑锛宍is_end=true` 鏃跺仠姝€?
## 鏋氫妇鍊?
- **`content_format`锛?* `0`=绾枃鏈紝`1`=Markdown锛宍2`=JSON銆傚啓鍏ワ紙`import_doc`/`append_doc`锛夌洰鍓嶄粎鏀寔 `1`锛圡arkdown锛夈€傝鍙栵紙`get_doc_content`锛夋帹鑽?`0`锛堢函鏂囨湰锛夛紝Markdown 鏍煎紡涓嶆敮鎸併€?- **`search_type`锛?* `0`=鏍囬妫€绱紙榛樿锛夛紝`1`=姝ｆ枃妫€绱?- **`sort_type`锛?* `0`=鏇存柊鏃堕棿锛堥粯璁わ級锛宍1`=鍒涘缓鏃堕棿锛宍2`=鏍囬锛宍3`=澶у皬锛堜粎 `search_note_book` 浣跨敤锛?- **`folder_type`锛?* `0`=鐢ㄦ埛鑷缓锛宍1`=鍏ㄩ儴绗旇锛堟牴鐩綍锛夛紝`2`=鏈垎绫?
## 娉ㄦ剰浜嬮」

- `folder_id` 涓嶅彲涓?`"0"`锛屾牴鐩綍 ID 鏍煎紡涓?`user_list_{userid}`锛堜粠 `folder_type=1` 鐨勭瑪璁版湰鏉＄洰鑾峰彇锛?- 绗旇鍐呭鏈夊ぇ灏忎笂闄愶紝瓒呰繃鏃惰繑鍥?`100009`锛屽彲鎷嗗垎涓哄娆?`append_doc` 鍐欏叆
- 鍐欏叆鍐呭涓嶆敮鎸佹湰鍦板浘鐗囷紝鍐欏叆鍓嶅繀椤昏繃婊ゆ湰鍦板浘鐗囪矾寰勫苟鍛婄煡鐢ㄦ埛锛堣瑙?馃柤锔?鏈湴鍥剧墖涓嶆敮鎸?瑙勫垯锛?- 灞曠ず绗旇鍒楄〃鏃跺彧灞曠ず鏍囬銆佹憳瑕佸拰淇敼鏃堕棿锛屼笉瑕佷富鍔ㄥ睍绀烘鏂?- 鏃堕棿瀛楁鏄?Unix 姣鏃堕棿鎴筹紝灞曠ず鏃惰浆涓哄彲璇绘牸寮?- 杩斿洖鏁版嵁涓哄祵濂楃粨鏋勶細鎼滅储缁撴灉鍙?`docs[].doc.basic_info.docid`锛岀瑪璁版湰鍙?`note_book_folders[].folder.basic_info.folder_id`锛岀瑪璁板垪琛ㄥ彇 `note_book_list[].basic_info.basic_info.docid`锛屾敞鎰忔寜灞傜骇瑙ｆ瀽

## 閿欒澶勭悊

| 閿欒鐮?| 鍚箟                   | 寤鸿澶勭悊                     |
| ------ | ---------------------- | ---------------------------- |
| 100001 | 鍙傛暟閿欒               | 妫€鏌ヨ姹傚弬鏁版牸寮忓拰蹇呭～瀛楁   |
| 100002 | 鏃犳晥 ID                | 妫€鏌ュ嚟璇侀厤缃?                |
| 100003 | 鏈嶅姟鍣ㄥ唴閮ㄩ敊璇?        | 绛夊緟鍚庨噸璇?                  |
| 100004 | size 涓嶅悎娉?/ 绌洪棿涓嶅 | 妫€鏌ュ弬鏁拌寖鍥?                |
| 100005 | 鏃犳潈闄?                | 纭鎿嶄綔鐨勬槸鐢ㄦ埛鑷繁鐨勭瑪璁?  |
| 100006 | 绗旇宸插垹闄?            | 鍛婄煡鐢ㄦ埛璇ョ瑪璁颁笉瀛樺湪         |
| 100008 | 鐗堟湰鍐茬獊               | 閲嶆柊鑾峰彇鍐呭鍚庡啀鎿嶄綔         |
| 100009 | 瓒呰繃澶у皬闄愬埗           | 鎷嗗垎涓哄娆?`append_doc` 鍐欏叆 |
| 310001 | 绗旇鏈笉瀛樺湪           | 妫€鏌?`folder_id` 鏄惁姝ｇ‘    |
| 20002  | apiKey瓒呰繃鏈€澶ч檺棰?    |
| 20004  | apikey 閴存潈澶辫触        | 妫€鏌ュ嚟璇侀厤缃槸鍚︽纭?        |

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ima-skill/notes/SKILL]] — Notes (笔记)
- [[09-技能库/ima-skills/ima-skill/notes/SKILL]] — Notes (笔记)
- [[09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/notes/SKILL]] — Notes (笔记)
- [[09-技能库/腾讯ima/notes/SKILL]] — Notes (笔记)
- [[ψ技能体系/00-foundation/ima/notes/SKILL]] — Notes (笔记)
- [[ψ技能体系/30-tools/ima-skill/knowledge-base/SKILL]] — Knowledge Base (鐭ヨ瘑搴?

<!-- AI-LINKS-END -->
