---
name: ima-skill-knowledge-base
description: 通过 IMA Wiki OpenAPI 管理知识库，支持上传文件、添加网页链接、搜索内容。
---

# Knowledge Base (鐭ヨ瘑搴?

> Prerequisites: see root `../SKILL.md` for setup, credentials, and `ima_api()` helper.

API base path: `openapi/wiki/v1`

閫氳繃 IMA Wiki OpenAPI 绠＄悊鐢ㄦ埛鐭ヨ瘑搴擄紝鏀寔涓婁紶鏂囦欢銆佹坊鍔犵綉椤甸摼鎺ャ€佹悳绱㈢煡璇嗗簱鍐呭銆佹祻瑙堢煡璇嗗簱鍒楄〃鍜岃幏鍙栫煡璇嗗簱璇︽儏銆?
瀹屾暣鐨勬暟鎹粨鏋勫拰鎺ュ彛鍙傛暟璇﹁ `references/api.md`銆?
## 鎺ュ彛鍐崇瓥琛?
| 鐢ㄦ埛鎰忓浘                                      | 璋冪敤鎺ュ彛                                                               | 鍏抽敭鍙傛暟                                                                 |
| --------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| 涓婁紶鏂囦欢鍒扮煡璇嗗簱                              | `check_repeated_names` 鈫?`create_media` 鈫?COS Upload 鈫?`add_knowledge` | `media_type`锛堟寜鎵╁睍鍚嶏級锛宍knowledge_base_id`锛宍file_name`锛宍file_size`  |
| 涓婁紶鏂囦欢鍒扮煡璇嗗簱鐨勬煇涓枃浠跺す                  | 鍏堝畾浣嶆枃浠跺す 鈫?鍚屼笂锛坄folder_id` 浼犲叆鐩爣鏂囦欢澶?ID锛?                  | 瑙併€屾枃浠跺す鎿嶄綔銆嶇珷鑺?                                                    |
| 娣诲姞缃戦〉/寰俊鏂囩珷鍒扮煡璇嗗簱                     | `import_urls`                                                          | `urls`锛?-10 涓級锛宍knowledge_base_id`锛屽彲閫?`folder_id`锛堢渷鐣ュ垯鏍圭洰褰曪級 |
| 娣诲姞绗旇鍒扮煡璇嗗簱                              | `add_knowledge`                                                        | `media_type=11`锛宍note_info.content_id=<doc_id>`锛宍knowledge_base_id`    |
| 娣诲姞 URL锛堟枃浠跺瀷锛夊埌鐭ヨ瘑搴?                   | `check_repeated_names` 鈫?涓嬭浇鏂囦欢 鈫?璧?涓婁紶鏂囦欢"娴佺▼                   | URL 鎸囧悜 PDF/Word/PPT 绛夋枃浠舵椂锛屾寜鏂囦欢鏂瑰紡澶勭悊                           |
| 妫€鏌ユ枃浠跺悕鏄惁閲嶅                            | `check_repeated_names`                                                 | `params[].name`锛宍params[].media_type`锛宍knowledge_base_id`锛宍folder_id` |
| 鑾峰彇鐭ヨ瘑搴撲俊鎭?                               | `get_knowledge_base`                                                   | `ids`锛?-20 涓紝涓嶉噸澶嶏級                                                 |
| 娴忚鐭ヨ瘑搴撳唴瀹瑰垪琛?/ 娴忚鏂囦欢澶?              | `get_knowledge_list`                                                   | `knowledge_base_id`锛宍cursor`锛宍limit`(1~50)锛屽彲閫?`folder_id`           |
| 鍦ㄧ煡璇嗗簱涓悳绱紙鍚枃浠跺拰鏂囦欢澶癸級              | `search_knowledge`                                                     | `query`锛宍knowledge_base_id`锛宍cursor`                                   |
| 鎸夊叧閿瘝鏌ユ壘鐭ヨ瘑搴擄紙鐢ㄦ埛鐭ラ亾鍚嶅瓧浣嗕笉鐭ラ亾 ID锛?| `search_knowledge_base`                                                | `query`锛宍cursor`锛宍limit`(1~50)                                         |
| 鏌ョ湅/浜嗚В鑷繁鏈夊摢浜涚煡璇嗗簱                     | `search_knowledge_base`锛坄query` 浼犵┖瀛楃涓诧級                          | `query: ""`锛宍cursor`锛宍limit`(1~50)                                     |
| 娣诲姞鍐呭浣?*鏈寚瀹?*鐩爣鐭ヨ瘑搴?               | `get_addable_knowledge_base_list` 鈫?灞曠ず鍒楄〃璁╃敤鎴烽€夋嫨                 | `cursor`锛宍limit`(1~50)                                                  |

### `search_knowledge_base` vs `get_addable_knowledge_base_list` 閫夋嫨鎸囧崡

杩欎袱涓帴鍙ｅ鏄撴贩娣嗭紝閫夋嫨瑙勫垯锛?
| 鍦烘櫙                                             | 浣跨敤鎺ュ彛                                       | 鍘熷洜                               |
| ------------------------------------------------ | ---------------------------------------------- | ---------------------------------- |
| 鐢ㄦ埛璇翠簡鐭ヨ瘑搴撳悕绉帮紙濡?娣诲姞鍒颁骇鍝佹枃妗ｅ簱"锛?      | `search_knowledge_base`                        | 鎸夊悕绉版悳绱紝鎵惧埌 ID 鍚庣户缁搷浣?    |
| 鐢ㄦ埛鎯虫祻瑙?浜嗚В鏌愪釜鐭ヨ瘑搴?                       | `search_knowledge_base` 鈫?`get_knowledge_base` | 鍏堟悳鍒?ID锛屽啀鑾峰彇璇︽儏              |
| 鐢ㄦ埛鎯虫煡鐪嬭嚜宸辨湁鍝簺鐭ヨ瘑搴擄紙鏃犲叿浣撳叧閿瘝锛?      | `search_knowledge_base`锛坄query: ""`锛?        | 绌?query 杩斿洖鐢ㄦ埛鐨勬墍鏈夌煡璇嗗簱鍒楄〃  |
| 鐢ㄦ埛瑕佹坊鍔犲唴瀹逛絾**娌¤娣诲姞鍒板摢涓煡璇嗗簱**         | `get_addable_knowledge_base_list`              | 鍒楀嚭鏈夋潈闄愭坊鍔犵殑鐭ヨ瘑搴擄紝璁╃敤鎴烽€夋嫨 |
| 鐢ㄦ埛璇?娣诲姞鍒扮煡璇嗗簱"浣嗕笂涓嬫枃涓棤娉曠‘瀹氬摢涓煡璇嗗簱 | `get_addable_knowledge_base_list`              | 鍚屼笂锛屼笉瑕佺寽娴嬶紝璁╃敤鎴烽€夋嫨         |

**缁濅笉瑕?*鍦ㄧ敤鎴峰凡鏄庣‘鎸囧畾鐭ヨ瘑搴撳悕绉版椂璋冪敤 `get_addable_knowledge_base_list`锛岀洿鎺ョ敤 `search_knowledge_base` 鎸夊悕绉版悳绱㈠嵆鍙€?
## 鏂囦欢绫诲瀷妫€娴?
浣跨敤 `scripts/preflight-check.cjs` 鑴氭湰鑷姩瀹屾垚绫诲瀷妫€娴嬪拰澶у皬鏍￠獙銆傝剼鏈寜浠ヤ笅浼樺厛绾цВ鏋愶細

1. **`--content-type` 宸叉彁渚涗笖鍙瘑鍒?* 鈫?content-type 浼樺厛锛岀洿鎺ヤ娇鐢?2. **`--content-type` 涓嶅彲璇嗗埆** 鈫?鍥為€€鍒版墿灞曞悕
3. **鏈彁渚?`--content-type`** 鈫?浣跨敤鎵╁睍鍚?4. **涓よ€呴兘鏃犳硶璇嗗埆** 鈫?鎷掔粷澶勭悊

```bash
# 鏈夋墿灞曞悕锛堣嚜鍔ㄦ帹鏂級
node .claude/skills/ima-skill/knowledge-base/scripts/preflight-check.cjs --file report.pdf

# 鏃犳墿灞曞悕鎴栨墿灞曞悕涓嶅彲璇嗗埆锛堥渶浼犲叆 content-type锛屽浠?HTTP HEAD 鑾峰彇锛?node .claude/skills/ima-skill/knowledge-base/scripts/preflight-check.cjs --file downloaded_file --content-type application/pdf
```

鎵╁睍鍚嶄笌绫诲瀷鐨勫搴斿叧绯伙細

| 鎵╁睍鍚?             | media_type | content_type                                                                 |
| ------------------- | ---------- | ---------------------------------------------------------------------------- |
| `.pdf`              | 1          | `application/pdf`                                                            |
| `.doc`              | 3          | `application/msword`                                                         |
| `.docx`             | 3          | `application/vnd.openxmlformats-officedocument.wordprocessingml.document`    |
| `.ppt`              | 4          | `application/vnd.ms-powerpoint`                                              |
| `.pptx`             | 4          | `application/vnd.openxmlformats-officedocument.presentationml.presentation`  |
| `.xls`              | 5          | `application/vnd.ms-excel`                                                   |
| `.xlsx`             | 5          | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`          |
| `.csv`              | 5          | `text/csv`                                                                   |
| `.md` / `.markdown` | 7          | `text/markdown`                                                              |
| `.png`              | 9          | `image/png`                                                                  |
| `.jpg` / `.jpeg`    | 9          | `image/jpeg`                                                                 |
| `.webp`             | 9          | `image/webp`                                                                 |
| `.txt`              | 13         | `text/plain`                                                                 |
| `.xmind`            | 14         | `application/x-xmind` / `application/vnd.xmind.workbook` / `application/zip` |
| `.mp3`              | 15         | `audio/mpeg`                                                                 |
| `.m4a`              | 15         | `audio/x-m4a`                                                                |
| `.wav`              | 15         | `audio/wav`                                                                  |
| `.aac`              | 15         | `audio/aac`                                                                  |

鏈瘑鍒殑鎵╁睍鍚嶆垨鏃犳墿灞曞悕锛?*鐩存帴鍛婄煡鐢ㄦ埛璇ユ枃浠剁被鍨嬩笉琚敮鎸侊紝绔嬪嵆缁堟鎿嶄綔**銆備笉瑕佺寽娴嬫垨榛樿涓烘煇涓被鍨嬶紝**涓嶈璇㈤棶鐢ㄦ埛鏄惁浠嶈涓婁紶**銆?
> **涓嶆敮鎸佺殑绫诲瀷**锛氳棰戞枃浠讹紙`.mp4`銆乣.avi`銆乣.mov` 绛夛級銆丅ilibili锛坄bilibili.com/video/`锛夊拰 YouTube锛坄youtube.com/watch`锛夐摼鎺ャ€佹湰鍦?HTML 鏂囦欢锛坄file://`锛?*鏃犳硶**閫氳繃 skill 娣诲姞鍒扮煡璇嗗簱銆傜洿鎺ュ憡鐭ョ敤鎴枫€岃鏂囦欢绫诲瀷涓嶆敮鎸侊紝浠呮敮鎸佸湪 ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆嶏紝**涓嶈鎻愪緵涓婁紶閫夐」鎴栬闂槸鍚︾户缁?*銆?
## URL 绫诲瀷妫€娴?
娣诲姞 URL 鍒扮煡璇嗗簱鏃讹紝闇€瑕佹牴鎹?URL 妯″紡鍜?Content-Type 鍒ゆ柇绫诲瀷銆傛娴嬫寜浠ヤ笅浼樺厛绾ц繘琛岋細

**1. Content-Type 涓?`text/html` 鏃讹紝鎸?URL 妯″紡鍖哄垎锛?*

| URL 妯″紡                                            | media_type | 绫诲瀷           | 澶勭悊鏂瑰紡                                                  |
| --------------------------------------------------- | ---------- | -------------- | --------------------------------------------------------- |
| 鍖归厤 `mp.weixin.qq.com/s/` 鎴?`mp.weixin.qq.com/s?` | 6          | 寰俊鍏紬鍙锋枃绔?| 浣跨敤 `import_urls`                                        |
| 浠?`https://www.bilibili.com/video/` 寮€澶?          | 鉂?16      | 瑙嗛缃戦〉       | **涓嶆敮鎸?*锛屽憡鐭ョ敤鎴枫€屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|
| 浠?`https://www.youtube.com/watch` 寮€澶?            | 鉂?16      | 瑙嗛缃戦〉       | **涓嶆敮鎸?*锛屽憡鐭ョ敤鎴枫€屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|
| 浠?`file://` 寮€澶?                                  | 鉂?        | 鏈湴 HTML      | **涓嶆敮鎸?*锛屽憡鐭ョ敤鎴枫€屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|
| 鍏朵粬 `text/html` 椤甸潰                               | 2          | 鏅€氱綉椤?      | 浣跨敤 `import_urls`                                        |

**2. Content-Type 涓烘枃浠剁被鍨嬫椂锛?* 鎸夋枃浠剁被鍨嬫娴嬭〃澶勭悊锛圥DF銆乄ord銆丒xcel 绛夛級銆?
**3. 鍏朵粬锛?* 鍛婄煡鐢ㄦ埛璇ョ被鍨嬩笉琚敮鎸併€?
## 娣诲姞鍓嶇疆妫€鏌ワ紙Pre-flight Check锛?
鍦ㄦ墽琛屼换浣曟坊鍔犵煡璇嗗埌鐭ヨ瘑搴撶殑鎿嶄綔鍓嶏紙`add_knowledge`銆乣import_urls`銆佷笂浼犳枃浠舵祦绋嬶級锛?*蹇呴』鎸変互涓嬮『搴忛€愰」妫€鏌?*锛屼换涓€椤逛笉閫氳繃鍒?*绔嬪嵆缁堟骞跺憡鐭ョ敤鎴凤紝涓嶈璇㈤棶鏄惁浠嶈灏濊瘯涓婁紶**锛?
### 1. 绫诲瀷鏀寔妫€鏌?
| 妫€鏌ラ」             | 鏉′欢                                                                      | 涓嶉€氳繃鏃剁殑澶勭悊                                |
| ------------------ | ------------------------------------------------------------------------- | --------------------------------------------- |
| 鏂囦欢鎵╁睍鍚嶆槸鍚︽敮鎸?| 鎵╁睍鍚嶄笉鍦ㄣ€屾枃浠剁被鍨嬫娴嬨€嶈〃涓?                                           | 鍛婄煡鐢ㄦ埛璇ユ枃浠剁被鍨嬩笉琚敮鎸?                   |
| 瑙嗛鏂囦欢           | `.mp4`銆乣.avi`銆乣.mov` 绛夎棰戞墿灞曞悕                                       | 鍛婄煡鐢ㄦ埛銆屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|
| 瑙嗛缃戦〉 URL       | `https://www.bilibili.com/video/` 鎴?`https://www.youtube.com/watch` 寮€澶?| 鍛婄煡鐢ㄦ埛銆屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|
| 鏈湴 HTML 鏂囦欢     | `file://` 鍗忚                                                            | 鍛婄煡鐢ㄦ埛銆屼粎鏀寔鍦?ima 妗岄潰绔唴娣诲姞杩涚煡璇嗗簱銆?|

### 2. 鏂囦欢澶у皬妫€鏌?
涓婁紶鍓嶅繀椤绘牎楠屾枃浠跺ぇ灏忥紝瓒呴檺鏂囦欢搴?*鍦ㄤ笂浼犲墠鎷︽埅**锛屼笉瑕佸彂璧疯姹傦細

| 鏂囦欢绫诲瀷                    | media_type  | 鏈€澶уぇ灏?|
| --------------------------- | ----------- | -------- |
| Excel銆乀XT銆乆mind銆丮arkdown | 5/13/14/7   | 10 MB    |
| 鍥剧墖                        | 9           | 30 MB    |
| PDF銆乄ord銆丳PT銆侀煶棰戝強鍏朵粬  | 1/3/4/15 绛?| 200 MB   |

### 3. 闊抽鏃堕暱妫€鏌?
闊抽鏂囦欢锛坢edia_type=15锛夐澶栭檺鍒讹細**鏈€闀?2 灏忔椂**銆傝秴杩囨椂鍛婄煡鐢ㄦ埛銆?
### 4. 鏂囦欢鍚嶉噸澶嶆鏌?
浠呴€傜敤浜庢枃浠剁被鍨嬶紙media_type 1/3/4/5/7/9/13/14/15锛夛紝涓嶉€傜敤浜庣綉椤碉紙2/6锛夈€佺瑪璁帮紙11锛夌瓑锛?
- 璋冪敤 `check_repeated_names` 妫€鏌?- `is_repeated=true`锛氳闂敤鎴锋槸鍚︿繚鐣欎袱鑰咃紙杩藉姞鏃堕棿鎴筹級鎴栧彇娑?- 涓嶆敮鎸?鏇挎崲"鎿嶄綔

> **妫€鏌ラ『搴忓緢閲嶈**锛氬厛鍋氱被鍨嬪拰澶у皬妫€鏌ワ紙鏈湴鍗冲彲鍒ゆ柇锛夛紝閫氳繃鍚庡啀璋冪敤杩滅▼鎺ュ彛妫€鏌ラ噸鍚嶃€傞伩鍏嶅涓嶆敮鎸佹垨瓒呴檺鐨勬枃浠跺彂璧蜂笉蹇呰鐨勭綉缁滆姹傘€?
## 甯哥敤宸ヤ綔娴?
### 涓婁紶鏂囦欢鍒扮煡璇嗗簱

瀹屾垚銆屾坊鍔犲墠缃鏌ャ€嶅悗锛屾墽琛屼互涓嬫楠わ細鍒涘缓濯掍綋 鈫?涓婁紶 COS 鈫?娣诲姞鐭ヨ瘑銆?
> 鍓嶇疆妫€鏌ワ紙绫诲瀷妫€娴嬨€佸ぇ灏忔牎楠屻€侀噸鍚嶆鏌ワ級瑙併€屾坊鍔犲墠缃鏌ャ€嶇珷鑺傘€?
```bash
# 1. 鍓嶇疆妫€鏌?鈥?绫诲瀷銆佸ぇ灏忎竴姝ュ畬鎴?#    鏈夋墿灞曞悕鏃讹細鑷姩浠庢墿灞曞悕鎺ㄦ柇 media_type 鍜?content_type
#    鏃犳墿灞曞悕鏃讹細闇€閫氳繃 --content-type 浼犲叆锛堝浠?HTTP HEAD 鑾峰彇锛?PREFLIGHT=$(node .claude/skills/ima-skill/knowledge-base/scripts/preflight-check.cjs \
  --file "/path/to/report.pdf")
echo "$PREFLIGHT"
# pass=false 鏃剁洿鎺ョ粓姝紝灏?reason 灞曠ず缁欑敤鎴?
# 2. 浠?preflight 缁撴灉鎻愬彇瀛楁锛堢敤浜庡悗缁?API 璋冪敤锛?FILE_NAME=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.file_name)")
FILE_EXT=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.file_ext)")
FILE_SIZE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.file_size))")
MEDIA_TYPE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(String(d.media_type))")
CONTENT_TYPE=$(echo "$PREFLIGHT" | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8'));process.stdout.write(d.content_type)")

# 3. 閲嶅悕妫€鏌ワ紙浠呮枃浠剁被鍨嬶紝瑙併€屾坊鍔犲墠缃鏌ャ€嶇 4 姝ワ級

# 4. create_media 鈥?鑾峰彇 media_id 鍜?COS 涓婁紶鍑瘉
ima_api "openapi/wiki/v1/create_media" "{
  \"file_name\": \"$FILE_NAME\",
  \"file_size\": $FILE_SIZE,
  \"content_type\": \"$CONTENT_TYPE\",
  \"knowledge_base_id\": \"<kb_id>\",
  \"file_ext\": \"$FILE_EXT\"
}"
# 浠庤繑鍥炲€兼彁鍙?media_id 鍜?cos_credential 鍚勫瓧娈?
# 5. 涓婁紶鏂囦欢鍒?COS
node .claude/skills/ima-skill/knowledge-base/scripts/cos-upload.cjs \
  --file "/path/to/report.pdf" \
  --secret-id "<cos_credential.secret_id>" \
  --secret-key "<cos_credential.secret_key>" \
  --token "<cos_credential.token>" \
  --bucket "<cos_credential.bucket_name>" \
  --region "<cos_credential.region>" \
  --cos-key "<cos_credential.cos_key>" \
  --content-type "$CONTENT_TYPE" \
  --start-time "<cos_credential.start_time>" \
  --expired-time "<cos_credential.expired_time>"

# 6. add_knowledge 鈥?灏嗗凡涓婁紶鐨勬枃浠跺叧鑱斿埌鐭ヨ瘑搴?ima_api "openapi/wiki/v1/add_knowledge" "{
  \"media_type\": $MEDIA_TYPE,
  \"media_id\": \"<media_id>\",
  \"title\": \"$FILE_NAME\",
  \"knowledge_base_id\": \"<kb_id>\",
  \"file_info\": {
    \"cos_key\": \"<cos_credential.cos_key>\",
    \"file_size\": $FILE_SIZE,
    \"file_name\": \"$FILE_NAME\"
  }
}"
```

#### 鎵归噺涓婁紶鏃剁殑閲嶅澶勭悊

褰撲笂浼犲涓枃浠舵椂锛屽彲涓€娆℃€ф鏌ユ墍鏈夋枃浠跺悕锛堟渶澶?2000 涓級锛?
```bash
# 鎵归噺妫€鏌?ima_api "openapi/wiki/v1/check_repeated_names" '{
  "params": [
    {"name": "report.pdf", "media_type": 1},
    {"name": "slides.pptx", "media_type": 4},
    {"name": "data.xlsx", "media_type": 5}
  ],
  "knowledge_base_id": "<kb_id>",
  "folder_id": "<folder_id>"
}'
# 娉ㄦ剰锛氬鏋滄槸鏍圭洰褰曪紝鐪佺暐 folder_id 瀛楁
# 閬嶅巻 results锛屽 is_repeated=true 鐨勬枃浠惰闂敤鎴凤細
# - "浠ヤ笅鏂囦欢鍦ㄧ煡璇嗗簱涓凡瀛樺湪鍚屽悕鏂囦欢锛歳eport.pdf銆乨ata.xlsx銆傛槸鍚︿繚鐣欎袱鑰咃紵锛堜笉鏀寔鏇挎崲锛?
# - 鐢ㄦ埛閫夋嫨"淇濈暀涓よ€?鐨勬枃浠讹細杩藉姞鏃堕棿鎴冲悗缁х画涓婁紶
# - 鐢ㄦ埛閫夋嫨"鍙栨秷"鐨勬枃浠讹細浠庝笂浼犲垪琛ㄤ腑绉婚櫎
```

**鏃堕棿鎴冲懡鍚嶈鍒?*锛氬湪鏂囦欢鍚嶏紙涓嶅惈鎵╁睍鍚嶏級鏈熬杩藉姞 `_YYYYMMDDHHmmss`锛屼緥濡?`report_20260317153000.pdf`銆?
### 娣诲姞缃戦〉/寰俊鏂囩珷鍒扮煡璇嗗簱

浣跨敤 `import_urls` 鎵归噺瀵煎叆缃戦〉鍜屽井淇″叕浼楀彿鏂囩珷锛?-10 涓?URL锛夛紝鏈嶅姟绔嚜鍔ㄨ瘑鍒被鍨嬶細

```bash
# 娣诲姞鍒版牴鐩綍锛堜笉浼?folder_id锛?ima_api "openapi/wiki/v1/import_urls" '{
  "knowledge_base_id": "<kb_id>",
  "urls": [
    "https://example.com/article",
    "https://mp.weixin.qq.com/s/xxxxx"
  ]
}'

# 娣诲姞鍒版寚瀹氭枃浠跺す锛堜紶 folder_id锛屼互 folder_ 寮€澶达級
ima_api "openapi/wiki/v1/import_urls" '{
  "knowledge_base_id": "<kb_id>",
  "folder_id": "<folder_id>",
  "urls": [
    "https://example.com/article"
  ]
}'
# 杩斿洖 results 鏄犲皠锛歿 "<url>": { url, ret_code, media_id } }
# ret_code=0 琛ㄧず鎴愬姛锛岄潪 0 鏌ョ湅 errmsg
```

### 娣诲姞绗旇鍒扮煡璇嗗簱

灏嗗凡鏈夌瑪璁帮紙閫氳繃 `doc_id` 寮曠敤锛夌洿鎺ュ叧鑱斿埌鐭ヨ瘑搴擄紝鏃犻渶涓嬭浇鍐呭锛?
```bash
ima_api "openapi/wiki/v1/add_knowledge" '{
  "media_type": 11,
  "note_info": { "content_id": "<doc_id>" },
  "title": "绗旇鏍囬",
  "knowledge_base_id": "<kb_id>"
}'
```

### 娣诲姞 URL 鍒扮煡璇嗗簱锛堣嚜鍔ㄦ娴嬫枃浠跺瀷 URL锛?
褰撶敤鎴锋彁渚?URL 鏃讹紝闇€鍏堝垽鏂 URL 鎸囧悜鐨勬槸缃戦〉杩樻槸鍙笅杞芥枃浠讹紙PDF銆乄ord銆丳PT 绛夛級銆?
**鍒ゆ柇瑙勫垯**锛堟寜浼樺厛绾э級锛?
1. **URL 璺緞鍖呭惈鏂囦欢鎵╁睍鍚?*锛氬 `https://arxiv.org/pdf/2603.12268` 浠?`/pdf/` 寮€澶达紝鎴?`https://example.com/report.pdf` 浠?`.pdf` 缁撳熬 鈫?鏂囦欢鍨?2. **鍙戦€?HEAD 璇锋眰妫€鏌?Content-Type**锛歚curl -sI -L <url>` 鏌ョ湅鍝嶅簲澶?   - `application/pdf` 鈫?PDF 鏂囦欢
   - `application/msword` 鎴?`application/vnd.openxmlformats-*` 鈫?Word/PPT/Excel 鏂囦欢
   - `text/html` 鈫?缃戦〉
3. **宸茬煡鏂囦欢鍨?URL 妯″紡**锛?   - `arxiv.org/pdf/*` 鈫?PDF
   - `*.pdf`銆乣*.docx`銆乣*.pptx`銆乣*.xlsx` 缁撳熬 鈫?瀵瑰簲鏂囦欢绫诲瀷
   - GitHub raw 鏂囦欢閾炬帴 鈫?鎸夋墿灞曞悕鍒ゆ柇

**鏂囦欢鍨?URL 澶勭悊娴佺▼**锛?
```bash
# 1. 鎺㈡祴 URL 绫诲瀷
CONTENT_TYPE=$(curl -sI -L "https://arxiv.org/pdf/2603.12268" | grep -i "^content-type:" | tail -1 | awk '{print $2}' | tr -d '\r')
# 缁撴灉濡?application/pdf 鈫?鏂囦欢鍨?
# 2. 涓嬭浇鏂囦欢鍒颁复鏃剁洰褰?TEMP_DIR=$(mktemp -d)
# 鏍规嵁 Content-Type 鎴?URL 鎺ㄦ柇鏂囦欢鍚嶅拰鎵╁睍鍚?curl -sL -o "$TEMP_DIR/paper.pdf" "https://arxiv.org/pdf/2603.12268"

# 3. 鍓嶇疆妫€鏌ワ紙浼犲叆 content-type 浣滀负澶囩敤锛屾枃浠跺悕鏈夋墿灞曞悕鏃朵細浼樺厛鐢ㄦ墿灞曞悕锛?PREFLIGHT=$(node .claude/skills/ima-skill/knowledge-base/scripts/preflight-check.cjs \
  --file "$TEMP_DIR/paper.pdf" --content-type "$CONTENT_TYPE")
echo "$PREFLIGHT"
# pass=false 鏃剁洿鎺ョ粓姝?
# 4. 鎸?涓婁紶鏂囦欢鍒扮煡璇嗗簱"娴佺▼澶勭悊锛歝reate_media 鈫?COS Upload 鈫?add_knowledge
# 锛堝弬瑙佷笂鏂?涓婁紶鏂囦欢鍒扮煡璇嗗簱"宸ヤ綔娴侊級

# 5. 娓呯悊涓存椂鏂囦欢
rm -rf "$TEMP_DIR"
```

**鏂囦欢鍚嶆帹鏂?*锛?
- 浼樺厛浠?`Content-Disposition` 鍝嶅簲澶存彁鍙栨枃浠跺悕
- 鍏舵浠?URL 璺緞涓彁鍙栵紙濡?`/pdf/2603.12268` 鈫?`2603.12268.pdf`锛?- 鏈€鍚庝娇鐢?URL 鐨勬渶鍚庝竴娈佃矾寰?+ 鏍规嵁 Content-Type 琛ュ厖鎵╁睍鍚?
### 鏂囦欢澶规搷浣?
鐭ヨ瘑搴撳唴瀹逛互鏂囦欢澶圭粨鏋勭粍缁囥€?*鏂囦欢澶规湰韬篃鏄竴绉嶇煡璇嗘潯鐩?*锛屽湪 `get_knowledge_list` 鍜?`search_knowledge` 鐨勮繑鍥炵粨鏋滀腑浼氬悓鏃跺寘鍚枃浠跺拰鏂囦欢澶广€?
#### 鏍稿績姒傚康

- `folder_id`锛氭枃浠跺す鐨勫敮涓€鏍囪瘑锛?*濮嬬粓浠?`folder_` 鍓嶇紑寮€澶?*锛堝 `folder_abc123`锛夛紝鍦?`add_knowledge`銆乣import_urls`銆乣get_knowledge_list`銆乣check_repeated_names` 绛夋帴鍙ｄ腑鐢ㄤ簬鎸囧畾鐩爣鏂囦欢澶?- **鎿嶄綔鏍圭洰褰曟椂锛屼笉瑕佷紶 `folder_id` 鍙傛暟**锛堢洿鎺ョ渷鐣ヨ瀛楁锛夛紝涓嶈灏?`knowledge_base_id` 浣滀负 `folder_id` 浼犲叆
- `get_knowledge_list` 杩斿洖鐨?`current_path`锛坄FolderInfo[]`锛夎〃绀哄綋鍓嶆祻瑙堜綅缃殑瀹屾暣璺緞锛堥潰鍖呭睉锛?
#### 瀹氫綅鏂囦欢澶癸紙鐢ㄦ埛鎻愬埌鏂囦欢澶瑰悕鏃讹級

褰撶敤鎴疯銆屾坊鍔犲埌 XX 鏂囦欢澶广€嶄絾鍙粰浜嗘枃浠跺す鍚嶇О鏃讹紝闇€瑕佸厛鎵惧埌 `folder_id`锛?
```bash
# 鏂规硶 1锛氭悳绱㈢煡璇嗗簱鍐呭锛堟帹鑽愶紝鍙洿鎺ユ寜鍚嶇О鎼滅储鏂囦欢澶癸級
ima_api "openapi/wiki/v1/search_knowledge" '{
  "query": "鏂囦欢澶瑰悕绉?,
  "knowledge_base_id": "<kb_id>",
  "cursor": ""
}'
# 浠庤繑鍥炵殑 info_list 涓壘鍒板尮閰嶇殑鏂囦欢澶规潯鐩紝鍙栧叾 media_id 浣滀负 folder_id

# 鏂规硶 2锛氭祻瑙堟牴鐩綍鍒楄〃閫愮骇鏌ユ壘
ima_api "openapi/wiki/v1/get_knowledge_list" '{
  "knowledge_base_id": "<kb_id>",
  "cursor": "",
  "limit": 50
}'
# 浠庤繑鍥炵殑 knowledge_list 涓壘鍒扮洰鏍囨枃浠跺す锛屽彇鍏?media_id 浣滀负 folder_id
# 濡傛灉鏂囦欢澶瑰湪瀛愮洰褰曚腑锛岄渶瑕佺敤杩斿洖鐨?folder_id 閫愮骇娣卞叆
```

#### 娣诲姞鍐呭鍒版寚瀹氭枃浠跺す

鎵€鏈夊啓鍏ユ帴鍙ｏ紙`add_knowledge`銆乣import_urls`銆乣check_repeated_names`锛夐兘鏀寔 `folder_id` 鍙傛暟锛?
```bash
# 涓婁紶鏂囦欢鍒版寚瀹氭枃浠跺す
ima_api "openapi/wiki/v1/add_knowledge" '{
  "media_type": 1,
  "media_id": "<media_id>",
  "title": "report.pdf",
  "knowledge_base_id": "<kb_id>",
  "folder_id": "<folder_id>",
  "file_info": { "cos_key": "...", "file_size": 12345, "file_name": "report.pdf" }
}'

# 瀵煎叆缃戦〉鍒版寚瀹氭枃浠跺す
ima_api "openapi/wiki/v1/import_urls" '{
  "knowledge_base_id": "<kb_id>",
  "folder_id": "<folder_id>",
  "urls": ["https://example.com/article"]
}'

# 娣诲姞鍒版牴鐩綍鏃讹紝鐩存帴鐪佺暐 folder_id
ima_api "openapi/wiki/v1/add_knowledge" '{
  "media_type": 1,
  "media_id": "<media_id>",
  "title": "report.pdf",
  "knowledge_base_id": "<kb_id>",
  "file_info": { "cos_key": "...", "file_size": 12345, "file_name": "report.pdf" }
}'
```

### 鑾峰彇鐭ヨ瘑搴撲俊鎭?
```bash
ima_api "openapi/wiki/v1/get_knowledge_base" '{"ids": ["<kb_id>"]}'
# 杩斿洖 infos 鏄犲皠锛歿 "<kb_id>": { id, name, cover_url, description, recommended_questions } }
```

### 娴忚鐭ヨ瘑搴撳唴瀹?
```bash
# 娴忚鏍圭洰褰?ima_api "openapi/wiki/v1/get_knowledge_list" '{"knowledge_base_id": "<kb_id>", "cursor": "", "limit": 20}'

# 娴忚鎸囧畾鏂囦欢澶?ima_api "openapi/wiki/v1/get_knowledge_list" '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "cursor": "", "limit": 20}'
# 缈婚〉锛氱敤 next_cursor锛宨s_end=true 鏃跺仠姝?```

### 鍦ㄧ煡璇嗗簱涓悳绱?
```bash
ima_api "openapi/wiki/v1/search_knowledge" '{"query": "鎼滅储鍏抽敭璇?, "knowledge_base_id": "<kb_id>", "cursor": ""}'
```

### 鎼滅储鐭ヨ瘑搴撳垪琛?
```bash
# 鎸夊叧閿瘝鎼滅储
ima_api "openapi/wiki/v1/search_knowledge_base" '{"query": "鎼滅储鍏抽敭璇?, "cursor": "", "limit": 20}'

# 鏌ョ湅鎵€鏈夌煡璇嗗簱锛堢┖ query锛?ima_api "openapi/wiki/v1/search_knowledge_base" '{"query": "", "cursor": "", "limit": 20}'
```

### 鑾峰彇鍙坊鍔犵殑鐭ヨ瘑搴撳垪琛?
**浠呭綋鐢ㄦ埛瑕佹坊鍔犲唴瀹逛絾鏈寚瀹氱洰鏍囩煡璇嗗簱鏃朵娇鐢?*銆傚鏋滅敤鎴峰凡缁欏嚭鐭ヨ瘑搴撳悕绉帮紝搴斾娇鐢?`search_knowledge_base` 鎸夊悕绉版悳绱紝鑰岄潪姝ゆ帴鍙ｃ€?
```bash
# 棣栨璇锋眰
ima_api "openapi/wiki/v1/get_addable_knowledge_base_list" '{"cursor": "", "limit": 20}'
# 缈婚〉锛氱敤 next_cursor锛宨s_end=true 鏃跺仠姝?```

## 鏍稿績鍝嶅簲瀛楁

鐭ヨ瘑鏉＄洰锛坄KnowledgeInfo`锛夊叧閿瓧娈碉細`media_id`锛堝獟浣揑D锛夈€乣title`銆乣parent_folder_id`銆?
鎼滅储鍒扮殑鐭ヨ瘑鏉＄洰锛坄SearchedKnowledgeInfo`锛夊叧閿瓧娈碉細`media_id`銆乣title`銆乣parent_folder_id`銆乣highlight_content`锛堥珮浜唴瀹癸紝鍐呭鍖归厤鏃惰繑鍥烇級銆?
鐭ヨ瘑搴撲俊鎭紙`KnowledgeBaseInfo`锛夊叧閿瓧娈碉細`id`銆乣name`銆乣cover_url`銆乣description`銆乣recommended_questions`銆?
鏂囦欢澶规潯鐩紙`FolderInfo`锛夊叧閿瓧娈碉細`folder_id`銆乣name`銆乣file_number`銆乣folder_number`銆乣parent_folder_id`銆乣is_top`銆?
瀹屾暣瀛楁瀹氫箟瑙?`references/api.md`銆?
## 鍒嗛〉

鎵€鏈夊垪琛ㄥ拰鎼滅储鎺ュ彛浣跨敤**娓告爣鍒嗛〉**锛?
1. 棣栨璇锋眰锛歚cursor: ""`
2. 妫€鏌ヨ繑鍥炵殑 `is_end`锛歚false` 琛ㄧず杩樻湁鏇村鏁版嵁
3. 灏嗚繑鍥炵殑 `next_cursor` 浣滀负涓嬫璇锋眰鐨?`cursor`
4. `is_end = true` 鏃跺仠姝㈢炕椤?
## 鍝嶅簲澶勭悊

鎵€鏈?API 杩斿洖缁熶竴缁撴瀯 `{ "retcode": 0, "errmsg": "...", "data": { ... } }`锛?
- `retcode=0`锛氭垚鍔燂紝浠?`data` 鎻愬彇涓氬姟瀛楁
- `retcode鈮?`锛氬け璐ワ紝**鐩存帴灏?`errmsg` 灞曠ず缁欑敤鎴?*鍗冲彲锛屼笉闇€瑕佽嚜琛岀炕璇戦敊璇爜

## 鐢ㄦ埛浣撻獙

- **闅愯棌鍐呴儴 ID**锛氶潰鍚戠敤鎴风殑灞曠ず涓?*姘歌繙涓嶈鏆撮湶 `knowledge_base_id`銆乣media_id`銆乣folder_id` 绛夊唴閮?ID**銆傚缁堜娇鐢ㄧ煡璇嗗簱鍚嶇О銆佹枃浠舵爣棰樸€佹枃浠跺す鍚嶇О绛夌敤鎴峰彲璇讳俊鎭€侷D 浠呯敤浜庡悗缁?API 璋冪敤锛屼笉灞曠ず缁欑敤鎴枫€?  - 鉁?`"宸叉坊鍔犲埌鐭ヨ瘑搴撱€屼骇鍝佹枃妗ｅ簱銆嶁湏"`
  - 鉂?`"宸叉坊鍔犲埌鐭ヨ瘑搴?abc123def456 鉁?`
  - 闇€瑕佸紩鐢ㄧ煡璇嗗簱鏃讹紝鍏堥€氳繃 `get_knowledge_base` 鑾峰彇鍚嶇О锛屽啀灞曠ず
- **绮剧畝杩涘害**锛氫笉瑕侀€愭鏆撮湶鍐呴儴鎿嶄綔锛堝"姝ｅ湪鍒涘缓濯掍綋鈥︽鍦ㄤ笂浼?COS鈥?锛夈€傚彧鎶ュ憡鐢ㄦ埛鍏冲績鐨勪俊鎭細
  - 涓婁紶鏂囦欢锛歚"姝ｅ湪涓婁紶 report.pdf鈥?` 鈫?`"宸叉坊鍔犲埌鐭ヨ瘑搴撱€屼骇鍝佹枃妗ｅ簱銆嶁湏"`
  - 娣诲姞缃戦〉锛歚"姝ｅ湪娣诲姞鈥?` 鈫?`"宸叉坊鍔犲埌銆屼骇鍝佹枃妗ｅ簱銆嶁湏"`
  - 澶辫触鏃跺睍绀?`errmsg` 鍗冲彲
- **鎵归噺鎿嶄綔**锛氭眹鎬荤粨鏋滐紝濡?`"3 涓枃浠跺凡娣诲姞鍒般€屼骇鍝佹枃妗ｅ簱銆嶏紝1 涓け璐ワ紙data.xlsx: 鏂囦欢澶у皬瓒呴檺锛?`
- **鏍煎紡鍖栧睍绀?*锛氳鍙栫被鎿嶄綔鐨勭粨鏋滃簲浠ョ粨鏋勫寲鏍煎紡灞曠ず缁欑敤鎴凤紝鑰岄潪鍘熷 JSON锛?
  **鐭ヨ瘑搴撳垪琛?*锛坄search_knowledge_base` / `get_addable_knowledge_base_list`锛夛細

  > 鎼滅储鐭ヨ瘑搴撳悗锛岀敤杩斿洖鐨?ID 鍒楄〃璋冪敤 `get_knowledge_base` 鑾峰彇鎻忚堪淇℃伅锛屼竴骞跺睍绀恒€?
  ```
  馃摎 鎼滅储缁撴灉锛堝叡 3 涓煡璇嗗簱锛夛細
  1. **浜у搧鏂囨。搴?* 鈥?瀛樻斁浜у搧鐩稿叧鐨勬墍鏈夋枃妗ｈ祫鏂?  2. **鎶€鏈柟妗堝簱** 鈥?鍚勯」鐩妧鏈柟妗堟眹鎬?  3. **绔炲搧鍒嗘瀽搴?*
  ```

  **鐭ヨ瘑搴撳唴瀹瑰垪琛?*锛坄get_knowledge_list`锛夛細

  ```
  馃搨 鐭ヨ瘑搴撱€屼骇鍝佹枃妗ｅ簱銆嶅唴瀹癸細
  馃搧 璁捐鏂囨。/          (3 涓枃浠? 1 涓瓙鏂囦欢澶?
  馃搧 浼氳绾/          (12 涓枃浠?
  馃搫 浜у搧闇€姹傛枃妗?pdf
  馃搫 鎶€鏈柟妗?docx
  馃搫 鏁版嵁鍒嗘瀽.xlsx
  --- 绗?1 椤碉紝杩樻湁鏇村鍐呭 ---
  ```

  **鎼滅储缁撴灉**锛坄search_knowledge`锛夛細

  > `search_knowledge` 杩斿洖鐨勬潯鐩寘鍚?`media_id`銆乣title`銆乣parent_folder_id`銆乣highlight_content`锛堝唴瀹瑰尮閰嶆椂杩斿洖楂樹寒鐗囨锛夛紝

  ```
  馃攳 鍦ㄧ煡璇嗗簱銆屼骇鍝佹枃妗ｅ簱銆嶄腑鎼滅储銆屾帓鏈熴€嶇殑缁撴灉锛?
  1. 馃搫 Q1鎺掓湡琛?xlsx (鏂囦欢澶? 椤圭洰绠＄悊/)
     > ...鍖呭惈**鎺掓湡**璁″垝鐨勮缁嗕俊鎭?..
  2. 馃搫 寮€鍙戞帓鏈熻璁?pdf (鏂囦欢澶? 浼氳绾/)
  3. 馃搧 鎺掓湡妯℃澘/ (鏂囦欢澶? 鏍圭洰褰?
  ```

  **鐭ヨ瘑搴撹鎯?*锛坄get_knowledge_base`锛夛細

  ```
  馃摎 浜у搧鏂囨。搴?  馃摑 鎻忚堪锛氬瓨鏀句骇鍝佺浉鍏崇殑鎵€鏈夋枃妗ｈ祫鏂?  馃挕 鎺ㄨ崘闂锛?     - 鏈€鏂扮殑浜у搧闇€姹傛槸浠€涔堬紵
     - 鎶€鏈柟妗堟湁鍝簺锛?  ```

## 娉ㄦ剰浜嬮」

- `get_knowledge_base` 鎺ュ彈 1-20 涓?ID锛涘崟涓?ID 涔熼渶鍖呰涓烘暟缁?- `get_knowledge_list` 鐨?`limit` 鑼冨洿涓?1~50
- **鏂囦欢澶规槸鐭ヨ瘑鏉＄洰鐨勪竴绉?*锛歚get_knowledge_list` 鍜?`search_knowledge` 鐨勮繑鍥炵粨鏋滀腑鍚屾椂鍖呭惈鏂囦欢鍜屾枃浠跺す锛岄渶閫氳繃瀛楁鍖哄垎锛堟枃浠跺す鏈?`folder_id`/`name`/`file_number`/`folder_number`锛屾枃浠舵湁 `media_id`/`title`锛?- **鐢ㄦ埛鎻愬埌鏂囦欢澶规椂**锛氬鏋滅敤鎴峰彧缁欎簡鏂囦欢澶瑰悕绉帮紙鑰岄潪 ID锛夛紝蹇呴』鍏堥€氳繃 `search_knowledge` 鎴?`get_knowledge_list` 鎵惧埌瀵瑰簲鐨?`folder_id`锛屽啀鎵ц鍚庣画鎿嶄綔
- `folder_id` 鍦?`add_knowledge`銆乣import_urls`銆乣get_knowledge_list`銆乣check_repeated_names` 涓潎涓哄彲閫夊瓧娈碉紝**鎿嶄綔鏍圭洰褰曟椂鐩存帴鐪佺暐 `folder_id`锛屼笉瑕佷紶璇ュ弬鏁?*銆俙folder_id` 鐨勫€煎缁堜互 `folder_` 鍓嶇紑寮€澶达紙濡?`folder_abc123`锛夛紝**涓嶈灏?`knowledge_base_id` 浣滀负 `folder_id` 浼犲叆**
- **鏂囦欢涓婁紶鏃?`title` 蹇呴』绛変簬 `file_name`**锛氳皟鐢?`add_knowledge` 娣诲姞鏂囦欢鏃讹紝`title` 瀛楁**蹇呴』浣跨敤鏂囦欢鐨勫師濮嬪畬鏁存枃浠跺悕锛堝惈鎵╁睍鍚嶏級**锛屼笉瑕佽嚜琛屾嫙瀹氭爣棰樸€俙file_name` 鍜?`title` 浼犲悓涓€涓€笺€?*绂佹缂╃煭銆佺炕璇戙€侀噸鍛藉悕鎴栫渷鐣ヤ换浣曢儴鍒?*銆備緥濡傛枃浠跺悕涓?`闊抽.mp3`锛屽垯 `file_name` 鍜?`title` 閮藉繀椤讳紶 `闊抽.mp3`
- 鏂囦欢鎵╁睍鍚嶅繀椤绘纭彁鍙栵紝鐢ㄤ簬 `media_type` 妫€娴嬪拰 `file_ext` 瀛楁锛堟棤鐐瑰彿锛屽 `pdf`锛?- COS 涓婁紶鑴氭湰澶辫触锛堥潪闆堕€€鍑虹爜锛夋椂锛屼笉瑕佺户缁皟鐢?`add_knowledge`
- COS 涓婁紶鏃?`--content-type` 搴斾紶鍏ユ枃浠剁殑瀹為檯 MIME 绫诲瀷锛堝 `application/pdf`锛夛紝鑰岄潪閫氱敤鐨?`application/octet-stream`
- 褰撶敤鎴锋彁渚?URL 娣诲姞鍒扮煡璇嗗簱鏃讹紝蹇呴』鍏堟娴?URL 鏄惁鎸囧悜鏂囦欢锛堥€氳繃 URL 璺緞鎵╁睍鍚?+ HEAD 璇锋眰 Content-Type锛夛紝鏂囦欢鍨?URL 闇€涓嬭浇鍚庤蛋涓婁紶娴佺▼锛涚綉椤?寰俊鏂囩珷鍨?URL 浣跨敤 `import_urls`

<!-- AI-LINKS-BEGIN -->
## 🔗 AI 关联笔记（统一索引生成 · 2026-11-14）

> 由 `00-索引与导航/AI统一索引` 生成；可重跑覆盖，可用回滚脚本还原。

- [[09-技能库/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[09-技能库/ima-skills/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[09-技能库/ima-skills/ima-skills-1.1.2/ima-skill/knowledge-base/references/api]] — IMA知识库 API
- [[09-技能库/resources_LLM-Wiki 知识库建设]] — LLM Wiki 鐭ヨ瘑搴撳缓璁?- 鐭ヨ瘑瀛︿範鎶ュ憡
- [[09-技能库/resources_MECE 原则与金字塔原理]] — MECE 鍘熷垯涓庨噾瀛楀鍘熺悊 - 鐭ヨ瘑瀛︿範鎶ュ憡
- [[09-技能库/腾讯ima/knowledge-base/references/api]] — IMA知识库 API
- [[ψ技能体系/30-tools/ima-skill/notes/SKILL]] — Notes (绗旇)

<!-- AI-LINKS-END -->
