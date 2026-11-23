# 📲 Social Media Auto App (Gujarati)

Aa app **roj jate** aa badhu banave chhe:

- 📖 **Kahani**: navi, nani prerak varta, tamara business sathe jodayeli
- 📝 **Post caption** ane **hashtags**
- 📱 **Story** image (1080×1920)
- 🖼️ **Post** image (1080×1350, quote sathe)
- 🎥 **AI video prompt** ane **voice-over script** (Reels/Shorts mate)
- 🎬 **YouTube Shorts** nu title ane description

### 🏢 Ek app, 6 brand
Darek brand nu **potanu kaam, potana accounts, potanu content** chhe. `config.json` → `brands` ma:

| # | Brand | Kaam | Chalu? |
|---|-------|------|--------|
| 1 | Khedut Putra | Kheti, khedut ni mahiti ane kahani | ✅ |
| 2 | Chiron Enterprise | Construction | ✅ |
| 3–6 | Brand 3, 4, 5, 6 | (naam ane kaam bharo) | ❌ `"enabled": false` |

Navo brand chalu karva: `business_name`, `business_details`, `default.topic` bharo ane `"enabled": true` karo.
Darek brand ni keys `.env` ma alag prefix sathe hoy chhe (dakhla `KHEDUT_FB_PAGE_ID`, `CHIRON_FB_PAGE_ID`),
etle ek brand ni post bija brand na account par kyarey nahi jay.

Fakt ek brand chalavvo hoy to:
```
python main.py --now --brand khedut_putra
```

### 👥 Ghana accounts (11 Page, 10+ Instagram, Group...)

**1. Ek j Meta token:** `.env` ma `META_USER_TOKEN` bharo. Aa ek token thi tamara **badha Facebook Page ane tena sathe jodayela Instagram account** chale chhe. Darek Page no alag token jate mali jay chhe.

**2. Yadi kadho:**
```
python main.py --accounts
```
Aa command tamara badha Page ane Instagram ni yadi batave chhe ane `output/meta_accounts.json` ma save kare chhe.

**3. Brand ma muko:** `config.json` → je brand nu account hoy tena `"accounts"` ma umero:
```json
"accounts": [
  {"platform": "facebook",  "name": "Khedut Putra Saurashtra", "page_id": "1234567890", "topic": "kapas, magfali", "enabled": true},
  {"platform": "facebook",  "name": "Khedut Putra Uttar Gujarat", "page_id": "2345678901", "enabled": true},
  {"platform": "instagram", "name": "@khedutputra_reels", "ig_user_id": "17841400000000", "enabled": true},
  {"platform": "instagram", "name": "@khedutputra_2", "ig_user_id": "17841400000001", "copy_from": "instagram:khedutputra_reels", "enabled": true},
  {"platform": "facebook_group", "name": "Khedut Groups", "group_links": ["https://www.facebook.com/groups/..."], "enabled": true}
]
```
- Darek account ne **alag content, alag image ane alag likes no hisab** male chhe.
- `topic`, `tone`, `language`, `bg_top`, `bg_bottom`: aa account mate potanu.
- `copy_from`: bija account nu aaj nu content vapro. Aathi **AI kharch bache chhe**, pan e account pehla lakhvu joie.
- Bija platform (X, LinkedIn, YouTube...) na ghana account: `{"platform": "youtube", "name": "Chiron Shorts 2", "env_prefix": "CHIRON_YT2_"}`, ane `.env` ma `CHIRON_YT2_YOUTUBE_ACCESS_TOKEN=...`
- Ek post pachhi bija account par post karta pehla **20 second rah jove chhe** (`delay_between_posts_sec`), jethi Facebook ne spam na lage.

**⚠️ Facebook Group:** Meta e **22 April 2024 thi Group ma API thi post karvanu band** karyu chhe, etle koi pan app Group ma jate post nathi kari shakti.
Aa app Group mate content ane image taiyar kare chhe. `.env` ma `ADMIN_TELEGRAM_*` bharo to roj **tamara phone par Group ni link sathe** aavi jashe. Tyan thi copy kari ne muko.
Bijo saral raasto: Page ni post ne Facebook ma **"Share → Group"** thi share karo.

### ⭐ Darek platform mate ALAG content
Darek platform mate **alag kahani, alag caption, alag image (alag rang)** bane chhe.
Ek j divas ma be platform par ek j vishay nathi aavto.
`config.json` → `platforms` ma darek platform mate alag rakhi shako:

```json
"instagram": { "enabled": true, "topic": "yuvano mate motivation", "tone": "energetic", "language": "Gujarati", "bg_top": "#833ab4", "bg_bottom": "#fd1d1d" }
```
Je vaat na lakho (dakhla `language`), te `default` mathi levay chhe.

Roj nu content aa rite save thay chhe:
```
output/khedut_putra/2026-11-23/
   facebook/   content.txt  post.jpg  story.jpg  video_prompt.txt
   instagram/  ...
   youtube/    ...  (video.mp4 ahi muko)
   whatsapp/   ...
   posted.json   ← kya post thayu tenu report
```

Pachhi e content **12 jagya** par jate post kare chhe:

| # | Platform | Shu post thay | Auto? |
|---|----------|---------------|-------|
| 1 | Facebook Page | Photo post + kahani + Story | ✅ |
| 2 | Instagram | Post + Story + Reel (video hoy to) | ✅ |
| 3 | Threads | Nani text post | ✅ |
| 4 | X (Twitter) | Tweet | ✅ |
| 5 | LinkedIn | Professional post | ✅ |
| 6 | Pinterest | Pin (image) | ✅ |
| 7 | Telegram Channel | Photo + puri kahani | ✅ |
| 8 | YouTube Shorts | Video upload | ✅ (video.mp4 hoy to) |
| 9 | YouTube (lambo video) | Script + title tayyar | ✍️ jate upload |
| 10 | WhatsApp Status / Channel | Image + text tayyar | ✍️ jate mukvu (WhatsApp auto-post nathi aaptu) |
| 11 | Snapchat | Story image tayyar | ✍️ jate mukvu |
| 12 | Facebook Story | Page Story | ✅ (Facebook sathe) |
| 13 | Facebook Group | Content + image phone par | ✍️ Meta e Group auto-post band karyu chhe |

> WhatsApp, Snapchat ane lamba YouTube video mate content roj `output/<brand>/<tarikh>/` ma tayyar male chhe. Tya thi phone par copy karine muki shako.

---

## 📱 APP (sauthi saral rit)

**Windows:** `App_Chalu_Karo.bat` par double-click karo. **Mac/Linux:** `./app_chalu_karo.sh`
(athva: `python main.py --app --phone`)

Browser ma app khulshe. Mobile ma kholva: computer ane mobile **same WiFi** par rakho, screen par batavelo link (`http://192.168.x.x:8080`) mobile ma kholo ane **PIN** nakho.
Mobile ma "Add to Home screen" karo etle app jevu icon bani jashe. `.env` ma `APP_PIN=123456` rakho to PIN e j rahese.

App chalu hoy tyan sudhi **schedule pan jate chale chhe**. Computer chalu rakhvu padshe.

| Tab | Shu thay |
|---|---|
| 🏠 **Brands** | **18 box sudhi** — darek box ek brand. Box kholo ane 5 pagla bharo (niche juo) |
| 🔗 **Jodo** | **"Facebook sathe jodo" / "YouTube jodo" button**, accounts ne brand aapo, bija platform ni key + 🧪 Test, token ketla divas chalse |
| 📅 **Aaj** | Aaj ni darek post (image, caption, ⭐ marks), ✏️ Sudharo, ✅ Approve, 🚀 Post, 🧪 Test |
| ✍️ **Navi post** | Jate lakho ke **AI pase lakhavo**, photo/video muko, accounts pasand karo, samay nakki karo |
| 🗓️ **Calendar** | Aakha mahina ni post: thai gayeli (👍 likes sathe), queue ni, fail |
| ⏳ **Queue** | Aavnari jate lakheli post, kadhi pan shakay |
| 💬 **Comments** | Badha Page/Instagram na navo comments ek jagya e. **🤖 AI javab sujhave**, tame joi ne moklo |
| 📊 **Analytics** | 30 divas no chart, **kaya kalake post karvathi vadhare chale**, best post |
| 📜 **Kaam** | Hamna shu chale chhe tenu live lakhan |
| 🩺 **Doctor** | AI na sudhara: ✅ Ha / ✗ Na button |
| ⚙️ **Accounts** | Brand / platform / account chalu-band |
| ⏪ **Undo** | Juno version pachho lavo |

### 🏠 Brand box (12 sudhi) — 5 pagla
1. **Aa brand shu chhe?** — vigat thi lakho (dakhla: *"Aa khedut mate nu box chhe — dhan ugadvu, dhan vechvu, bajar bhav..."*)
2. **🤖 AI topic sujhave** — 20 topic aavshe → tick karo → **✅ Final karo**. Tamara potana topic pan umeri shako.
   Roj final topic mathi **vaaraphartee** ek-ek aave chhe, ane ek j divas e be account par ek j topic nathi aavto.
3. **Kaya social media par?** — tick karo (account 🔗 Jodo thi jodaya hoy te)
4. **Shu mukvu?** — 🖼️ Post · 📱 Story · 🎬 Reel · ▶️ Video
   Reel/Video **app jate banave chhe**: story image par dhimo zoom, 12 second, 9:16. `assets/music/` ma copyright-free .mp3 muko to pachhvade vaagshe.
   **🎬 Video kevo?** (brand ma pasand karo):
   - 🖼️ **Saadi** — photo par zoom, 12 second (jadapi, koi internet nahi)
   - 📖 **Kahani** — AI kahani ne 4–10 scene ma vahenche → darek scene nu **photo jevu chitra** → **Gujarati avaaj** → subtitle → video
   - 🧸 **Cartoon** — e j rite, pan **cartoon chitra**
   Avaaj: Gujarati (Dhwani 👩 / Niranjan 👨), Hindi, English. Chitra: Pollinations (free; `POLLINATIONS_API_KEY` hoy to jadapi ane watermark vagar). Avaaj: edge-tts (free).
   Ek video ne 2–4 minute lage chhe. **"🎬 Ek sample video banavo"** button thi pehla joi lo.
   Internet/AI na chale to app atakti nathi: chitra ni jagya e rang, avaaj vagar subtitle sathe video bane chhe.
   ⚠️ Chitra ma koi jaanita cartoon patra, celebrity ke logo nathi banavta — fakt navo, potano.
5. **Samay** — mul samay (8:00) + **roj variation** (30 minute): 8:00 → 8:24 → 8:10 ... manas jevu. Aavta 7 divas na samay screen par dekhay chhe.

### 🔗 Accounts jodvana (App → 🔗 Jodo)
**Facebook + Instagram (ek vaar setup, ~10 minute):**
1. developers.facebook.com/apps → Create App → **Business** → App ID ane App Secret App ma paste karo
2. "Facebook Login for Business" umero → Redirect URI: `http://localhost:8080/connect/meta/callback`
3. App ma **🔗 Facebook sathe jodo** → login → badha Page tick karo
4. Tamara badha Page + Instagram ni yadi aavshe → darek ne dropdown thi brand aapo → **Save**
Token ~60 divas chale chhe; App batave chhe ketla divas baki, ane 10 thi ochha hoy to laal thay — fari "jodo" dabavo.

**YouTube:** (video: brand ma ▶️ youtube tick + 🎬 Reel/Video tick — app jate video banavi Shorts tarike muke chhe; AI video par YouTube nu "AI" label jate)
⚠️ Google na niyam: navo Google Cloud project "unverified" hoy to YouTube video **private** rakhi shake — app tarat 🩺 Tapas ma batave chhe.
Tyare free **YouTube API audit** form bharo (support.google.com/youtube/contact/yt_api_form); tya sudhi YouTube Studio ma video jate Public karo.
Google Cloud ma OAuth Client (Web) banavo, Redirect URI `http://localhost:8080/connect/google/callback`, Client ID/Secret App ma muko, pachhi darek brand mate **🔗 YouTube jodo**. App ne Google ma **"In production"** karo, nahi to 7 divase jun thay chhe. Ek vaar jodya pachhi kyarey jun nathi thatu.

**Bija (Telegram, X, LinkedIn, Pinterest, Threads):** key paste karo → **🧪 Test** → Save.

> Login vala button computer par `http://localhost:8080` thi j chale chhe (mobile na link thi nahi).

### ✅ Approval (pehla joi lo, pachhi post)
`config.json` ma `"approval_required": true` karo. AI post samay thi 2 kalak pehla (`prepare_minutes`) content banavshe.
Tame App ma joi ne ✏️ sudhari ne ✅ Approve karo, pachhi j e samaye post thashe.

### ⏰ Darek account no alag samay
Platform ke account ma `"time": "19:00"` lakho. `"time": "auto"` lakho to **likes pramane best samay** jate pasand thashe (data aave pachhi).
App/computer modu chalu thay to `catch_up_minutes` (180) thi vadhare moda ni post aaje nathi thati; App ma 🚀 Post thi kari shako.

### 💬 Comments mate Meta permission
Meta token ma aa permission umero: `pages_read_user_content`, `pages_manage_engagement`, `instagram_manage_comments`.

## 🩺 Tapas — badhi bhul ek jagya e (laal button)
App → **🩺 Tapas**. App ni **badhi** vastu tapase chhe — fakt code nahi:

| Bhul | Sudharo button |
|---|---|
| Koi AI key nathi / free limit puri | 🔗 Key umero · 🔄 Fari try |
| Facebook/Instagram/YouTube... jodayu nathi, token jun, permission khute | 🔗 Jodo / Fari jodo |
| Gujarati font nathi | ⬇️ Font download |
| Video/avaaj nu program nathi | 📦 Install karo |
| Aaj ni post fail | 🔁 Fari post · 🤖 AI thi tapaso |
| Queue ni post fail | 🔁 Fari try |
| Brand ni vigat/topic nathi, koi social media chalu nathi | ✏️ Brand kholo |
| Instagram mate image link nathi | ⚡ Jate link chalu |
| Backup nathi | 💾 Hamna backup |
| Approval baki | ✅ Jovo |
| Ghana Page par copy content (spam jokham), phone khabar nathi, aavta varsh na tahevar nathi | salah |

Niche **🤖 AI na code-sudhara** (Ha/Na) pan e j screen par chhe. Laal number = ketli bhul baki.

## 🛡️ Bharosapatra
- **💾 Backup:** roj raatre 23:30 jate (settings + likes + topic + queue; keys nahi). Chhella 30 rahe chhe, ane Telegram (admin) par pan aave chhe. Hamna: `python main.py --backup`
- **⏳ Token yaad:** Facebook token 7 divas ma khatam thato hoy to phone par message.
- **🧹 Juni image/video** 30 divas pachhi jate nikli jay chhe (`keep_media_days`); content ane history rahe chhe.
- **🧪 Automatic tests:** `python -m unittest discover tests` — AI Doctor darek sudhara pachhi jate chalave chhe.
- **👥 Staff PIN:** `.env` ma `APP_APPROVER_PIN=...` → staff fakt post jovi, sudharvi, approve ane comments no javab aapi shake; keys/settings nahi.

## 🆕 Navi sagvad (customer, kamani, report)

### 📇 Lead / puchhparchh yadi
Comment ma "bhav?", "kaam joie", "scrap levo chhe", "number aapo" (ke koi e potano 10 ankda no number lakhyo) → **📇 Leads** screen ma umeray,
Telegram par khabar, ane brand box → 📇 ma **phone + javab** lakhyo hoy to e comment ma jate javab jay. Status: navo / vaat thai / puru / kaam nu nathi.
(Messenger/Instagram DM mate Meta ni alag parvangi joie — atyare comment.)

### 🗺️ Google Business (Google Maps) par post
Brand ni channel ma **Google Business** pasand karo ane Save, pachhi 🔗 Jodo ma **Google fari jodo** (have Business parvangi pan mangshe —
fakt je brand ma Google Business chalu hoy tya j) + 🔗 Jodo ma `GBP_ACCOUNT_ID` ane `GBP_LOCATION_ID`. Post ma photo + 📞 Call button.
Google e Business Profile API mate tamaro project **approve** karvo pade (Google Cloud → My Business API access request).

### 🛒 Product / offer post (Phone Zone vagere)
Brand box → 🛒 ma `Naam | Bhav | Vigat` (ek line ma ek). Roj / 2 divase / athvadiye ek product, kram thi.
**Bhav tame lakhyo e j** caption ma aave — AI potano bhav, offer ke EMI nahi lakhe.

### 🌾 Bija yard na bhav
Khedut Putra → 📊 ma Rajkot, Junagadh, Amreli, Jamnagar (ane biju koi pan yard naam lakhi ne). Bharat sarkar nu **AGMARKNET (data.gov.in)** —
data.gov.in par free sign up → API key → App → 🔗 Jodo ma `DATA_GOV_IN_API_KEY`. Bhav ₹/quintal aave chhe, ahi **₹ / 20 kilo** ma batavay;
fakt AAJ na bhav. Koi yard na aaj na bhav na hoy (ke API na chale) to e yard chhodi de — Gondal ni post atakti nathi; bhul 📊 ma dekhay.

### 🔁 Potana page vachche promotion
Brand box → 🔁: kaya potana page ni jaherat, ketli post e ek vaar (default 3), ane aa page ni link.
Shuru thi: Khedut Putra ↔ Gujarat Agri Business ↔ Our Gujarat News · Chiron ↔ Labour ↔ Scrap · Movie Hub ↔ Cartoon ↔ Cricket · Phone Zone ↔ Import Export ↔ Bhavesh Thummar.
**Darek page ni link 🔁 ma lakhjo** — link vagar fakt naam aave.

### 📺 Athvadiyik lambo cartoon video
Cartoon YouTube: dar **Ravivare 18:00** chhella 7 divas na nana video jodi ne aado (16:9) "Weekly Collection" video, chapter (00:00 Kahani 1 ...) sathe.
Ochha ma ochha 3 video joie. Hamna: `python main.py --weekly --brand cartoon_youtube --dry-run`.

### 📈 Athvadiyik report
Dar **Ravivare 20:00** Telegram par: darek brand ni post, likes/comment/share/views, gaya athvadiya karta vadharo-ghatado, saru chalelu,
saro samay ane navaa lead. Hamna: `python main.py --weekly-report`.

### 🏏 Cricket match divas
Cricket news ma "aaje no match" ane "parinam" ne pehla, din ma 4 vaar (10, 15, 19, 23 vage). Score/parinam fakt khabar ma lakhyu hoy e j —
AI anuman nahi kare; satta/fantasy ni vaat nahi. (Live ball-by-ball score mate paid service joie.)

## 🌾 Khedut Putra — content plan
- **Roj:** kheti-vadi ni vaato (18 final topic + season + havaman Gondal pramane), prakar farta (kahani, tips, sawal, quiz...).
- **📰 Kheti news + 🏛️ sarkari sahay:** din ma 2 vaar (09:30, 18:30), approval sathe. Yojana/sahay/MSP/pak vimo ni khabar pehla —
  fakt khabar ma lakhyu hoy e j, rakam/tarikh potani rite nahi; "i-Khedut / gram sevak par tapaso".
- **📊 Bajar bhav:** Gondal + Rajkot, Junagadh, Amreli, Jamnagar (1–4 vage).
- **🌱 Dar Budhvare:** ek fasal ni sampurn mahiti no 2-3 min video + 7 slide (kapas, magfali, ghau, jiru ... 24 pak kram thi).
  Brand box → 🌱 ma var ane pak ni yadi badlo.

## 📘 Badha brand — Khedut Putra jevo content plan
Darek brand ma: **final topic** (roj), **📘 athvadiye ek "sampurn mahiti" video** (2-3 min + 7 slide) ane jya jame tya **📰 news** (approval sathe, roj 12:30).
| Brand | 📘 Athvadiyik video (var) | 📰 News |
|---|---|---|
| Khedut Putra | 24 pak — Budhvar | kheti + sarkari sahay (9:30, 18:30) |
| Chiron | foundation, slab, waterproofing, 11/33 kV line, transformer, earthing, FRP — Somvar | construction, power line, infra |
| Bhavesh Thummar | vyavsay, paisa, marketing, team — Shukravar | — |
| Labour | site safety, mason, welder, operator, fraud thi bachav — Mangalvar | jobs, labour law, safety |
| Scrap | loha, tamba, aluminium, e-waste, vehicle, battery — Guruvar | recycling, scrappage policy (rate nahi) |
| Saitica | sciatica, kamar, gardan, ghunta, posture, yoga — Shanivar | — (arogya ni khabar ma bhul nu jokham) |
| Gujarat Agri Business | FPO, cold storage, dal mill, masala unit, export — Mangalvar | agri business, processing |
| Import Export | IEC, documents, Incoterms, LC, customs — Budhvar | exports, DGFT, ports |
| Khodal Dham | Khodal Dham, Dwarka, Somnath, Bet Dwarka, yatra — Shukravar | 3 dham ni official khabar |
| Phone Zone | battery, navo phone, camera, fraud thi suraksha — Guruvar | phone launch, fraud alert |
| Cricket | LBW, DRS, powerplay, formats, DLS — Budhvar | match divas, parinam |
| Our Gujarat News | Gujarat na 33 jilla — Shanivar | Gujarat ni khabar |
| Cartoon YouTube | — (Ravivare lambo collection video) | — |
| Movie Hub | — (movie na bhag) | — |
Brand box → 📘/🌱 ma var ane vishay ni yadi badlo.

## 🤝 Instagram Collab (sathe post)
Brand box → 🤝 ma bija Instagram account na username (ek line ma ek). Post, reel ane carousel par e account **collaborator** tarike umeray
(story ma nahi; Instagram ni maryada: ek post ma 3 sudhi). **Auto (default):** darek post ma alag account — badha ek vaar vaprai jay pachhi j fari.
E account ne Instagram ma invite jay; e Accept kare pachhi post ena profile par pan dekhay. Instagram na swikare to post atakti nathi (collab vagar thay).
Facebook ma API thi collab nathi.

## 📍 Post par location
Brand box → 📍 ma **Location ID** (e jagya nu Facebook page nu ID, dakhla "Gondal, Gujarat") ane caption ma lakhvanu lakhan (dakhla "Gondal, Gujarat").
**➕ Biju location** athva **ek sathe ghana** (ek line ma ek: `Kolithad, Gondal` athva `Kolithad, Gondal | 1234567890`), 200 sudhi.
**🔄 Auto (default chalu):** darek post ma alag location — badha ek vaar vaprai jay pachhi j fari aave, darek round no kram alag,
joda joda e j vistar nahi (vistar = comma pachhi nu, dakhla "Gondal"). E j post fari chale (retry) to e j location rahe.
ID khabar na hoy to khali rakho: app naam thi Facebook par shodhe (Meta "Pages Search" parvangi aape to); na male to fakt caption ma "📍 naam".
- Facebook post/carousel ane Instagram post/reel/carousel par location tag thay; caption ma "📍 Gondal, Gujarat". Story ma nahi.
- ID kya thi (Facebook nu sachu "📍 Check-in" tag mate): Facebook Search ma gam nu naam → Places/Pages ma e jagya nu page kholo →
  Share → Copy link → app ma `Kolithad, Gondal | <link>` paste karo. App link mathi ID jate kadhe (ID sidhu pan chale).
- ID khotu hoy ke Facebook na swikare to post atakti nathi — location vagar thai jay chhe.
- Ek account nu alag location: config.json ma e account ma `"location_id": "...", "location_text": "..."`.

## 🗣️ Bhasha (darek brand box ma 5 option)
| Option | Dakhlo |
|---|---|
| Gujarati | આજની ટીપ: પાણી બચાવો! |
| Gujarati (English akshar) | Aaje no tip: pani bachavo! |
| Hindi | आज की टिप: पानी बचाओ! |
| Hindi (English akshar) | Aaj ka tip: paani bachao! |
| English | Today's tip: save water! |

Atyare: **Khedut Putra = Gujarati**, baki badha = **Hindi (English akshar)**, **Movie = English**.
Brand box → Bhasha thi badlo — **video no avaaj pan jate e bhasha no thai jay** (Gujarati → Gujarati avaaj, Hindi / Hindi English akshar → Hindi avaaj, English / Gujarati English akshar → English avaaj; stri/purush e j rahe). Pachhi Avaaj ma jate pan badli shakay.

## 🎬 Movie / Web series — bhag ma roj (copyright vagar nu j) — badhu ENGLISH ma
Brand box → 🎬 ma chalu karo. Folder `movies/<brand>/` ma muko:
- **Movie:** `Sintel.mp4` + `Sintel.info.txt`
- **Series:** folder `Mari Series/` ma `01.mp4, 02.mp4 ...` + `info.txt`

info.txt:
```
naam: Sintel
varsh: 2010
license: CC BY 3.0
credit: (c) Blender Foundation | durian.blender.org
link: https://studio.blender.org/films/sintel/
varta: A girl sets out to find her lost baby dragon... (optional — na lakho to AI lakhe)
prakar: Animation, Fantasy        (optional)
hashtag: sintel, dragonmovie      (optional)
```
- **Hashtag ane varnan:** darek movie mate AI ek vaar movie ne lagta 18 hashtag, ek aakarshak line ane nani varta (spoiler vagar) banave (badhu English ma: title card "Part 2/5", caption, varta, hashtag).
  Ek movie/series na **badha bhag ma hashtag sarkha j** (movie nu naam vado pehlo + 4 lagta). Caption: naam, Episode/Bhag, prakar, line, varta, Follow/Share line (farti), credit.
- **license farajiyat:** public domain / CC0 / CC BY / CC BY-SA / potanu / permission. Na hoy, ke **ND** hoy, to app e video **nahi** muke.
  NC hoy to chetavani (page par kamani chalu hoy to na mukvu). Public domain ma `varsh` lakho: Bharat ma film no copyright release pachhi 60 varsh.
- App video ne saman bhag ma kape (default 3 minute), darek bhag ni sharuat ma 3 second nu title card (naam, "Episode 2 · Part 3/10"),
  upar khune page nu naam, niche bhag no label, caption ma credit + license. Ubhu (Reel/Shorts) ke aadu (Facebook video).
- Samay: dakhla `13:00, 20:00` = roj 2 bhag. Kram: pehli movie na badha bhag, pachhi biji... Post thayelo bhag PC mathi kadhi nakhe (jagya bache).
- Jya maltu hoy: archive.org (Public Domain Feature Films), Blender open movies (Sintel, Tears of Steel, Spring — CC BY).
  Gaana, navu restore karelu version ke dubbing alag copyright hoy shake — pakku karine j muko.
- Hamna: `python main.py --movie --brand <slug>` (`--dry-run` = fakt banavo, post nahi).

## ⏰ Aagal thi time set (PC band hoy topan post jay)
App chalu hoy tyare darek 30 minute e **aaj ni baki ane kaal ni** post banavi ne, je platform par aa sagvad chhe tyan
pehla thi time set kari de chhe. Pachhi e samaye PC band hoy topan platform pote post muki de chhe.
- **Facebook Page:** post, carousel, video/reel — haa (Facebook: 10 minute thi 30 divas aagal).
- **YouTube:** haa (video private chadhe, samaye jate public thay).
- **Facebook story, Instagram, Threads, X, LinkedIn, Pinterest, Telegram:** e platform aa sagvad nathi aapta — e samaye PC chalu hoy to j jashe.
- Bajar bhav ane news: bapore/e divase j aave, etle aagal thi na thay.
- Approval chalu hoy to: tame aaj ni post approve karo etle tarat time set thai jay (kaal nu nahi).
- Time set thaya pachhi App ma lakhan badlo to Facebook/YouTube par na badlay — tyan Meta Business Suite / YouTube Studio ma badlo ke kadhi nakho.
- Band karvu: config.json ma `"advance_schedule": false`. Ketla divas aagal: `"advance_days": 1` (7 sudhi).
- Hamna j karvu: `python main.py --advance`

## 🏷️ Post par page/account nu naam
Badhi post (image, story, carousel, bajar bhav, news, kahani/cartoon video) ma **upar dabe khune, akshar ni unchai post na 2% (100 cm post → 2 cm akshar), 60% dekhay** e rite
e page/account nu naam — jem ke "Khedut Putra Saurashtra" ke "@khedutputra_reels" (ek-account vala platform par brand nu naam).
Pachhal ajvalu hoy to kala akshar, andharu hoy to safed — jate. Brand box → 🏷️ ma: chalu/band, ketlu dekhay (%), kad, kayo khuno (upar/niche, dabe/jamne/vachche), bijū naam.
(HeyGen vala video ma naam nathi umeratu.)

## 🔄 Darek divas navo concept (loko kantale nahi)
Ek account par **7 divas sudhi e j prakar ane e j design fari nathi aavta**, ane topic/hashtag pan badlay chhe.

**Post na prakar** (brand box → 🔄 ma chalu/band): 📖 Kahani · 💡 5 Tips (carousel) · ❓ Sawal · 🤔 Maanyata vs Sachai ·
🏆 Prerak udaharan · 🧠 Shu tame jano chho? · ⚠️ 5 saamanya bhulo · ✅ Checklist (carousel) · ⚖️ Sarkhamni · 🎯 Quiz ·
🌦️ Havaman salah (shaher set hoy to) · 🏗️ Pehla/Pachhi. Brand box ma **aavta 7 divas** na prakar dekhay chhe.

**Image:** 6 design (photo niche lakhan · card · split · vachche lakhan · minimal · rang) — **logo ke phone number nathi mukatu**.
Pachhal: 🤖 AI chitra (post ne lagtu) · 📸 tamara photo · 🔀 mix · 🎨 saado rang.

**📸 Mara photo:** brand box ma photo umero (vigat lakho to saru). AI photo joi ne post lakhe chhe (Gemini key joie);
photo emno em mukay chhe (lakhan vagar) — sauthi lamba samay thi na vaparelo photo pehla.

**🎠 Carousel:** Tips/Checklist prakar → ek post ma 6 slide (pehli: sheershak + photo, pachhi 5 slide) — Facebook ane Instagram banne.

**🌦️ Havaman:** brand ma shaher lakho → AI aavta 3 divas nu **sachu** havaman (Open-Meteo) vapre chhe, potana aankda nahi.
Open-Meteo nu free API bin-vyaparik upyog mate chhe; vyaparik upyog mate emni shart jovo.

**✍️ Mari style:** tamari 3–5 juni post paste karo → AI tamara jevu lakhe chhe.

## 📰 News channel (koi pan brand box ma)
Navo box banavo (dakhla "Khedut News") athva koi pan brand → **📰 News channel** → Chalu.
1. **Source umero:** Google News ma shabd (dakhla `ખેડૂત OR ખેતી OR કૃષિ`, Gujarati/Hindi/English) · 🏛️ PIB (Bharat sarkar ni press release) · koi pan RSS link.
2. **Filter:** "aa shabd hoy e j", "aa shabd hoy e nahi". **Band vishay** (default): Rajkaran, Dharm, Gunah — AI aavi khabar chhodi de chhe.
3. **Samay:** roj 7:30 e khabar shodhe; "post samay" jetla (dakhla 09:00, 13:00, 18:00) etli khabar, thoda variation sathe.
4. AI **fakt source ma hoy etlu j**, **potana shabdo ma** Gujarati saransh lakhe chhe; apni design nu news card (photo + sheershak + saransh + "સ્રોત") ane caption ma source + link.
5. **✅ Approval (default chalu):** khabar **⏳ Queue → "Approval baki"** ma aave chhe (phone par Telegram khabar pan). Tame vanchi, sudhari, **✅ Approve** karo pachhi j post thay. "✗ Na mukvi" thi kadho.
6. Ek vaar aavi gayeli khabar fari nathi aavti.

⚠️ Bija news channel na lekh/photo/video copy **nathi** karatu — fakt potana shabdo ma saransh + source nu naam. AI kyarek bhul kari shake, etle approval chalu rakho.
Hamna: `python main.py --news --brand <brand>` (draft banave).

## 📊 Bajar bhav — Gondal APMC (roj jate)
Khedut Putra box → **📊 Bajar bhav** (chalu chhe). Source: Gondal APMC ni website (`apmcgondal.scmsolution.in`):
🌾 Jansi (`/Daily_Rate.aspx`) · 🥬 Shakbhaji (`/Daily_Rates_Veg.aspx`) · 🍎 Fal (`/Daily_Rates_Fruits.aspx`).

**Kem kaam kare chhe:**
- Roj **1:00–4:00** darmiyan darek 15 minute website tapase chhe.
- Website par **tarikh nathi lakhti**, etle bhav **kaal karta badlaya** hoy tyare j "aaj na bhav" mani ne **ek j vaar** post kare chhe.
  4 vage sudhi na badlaya (Ravivar / raja / update nathi) → **post nahi** (juna bhav aaj na tarike na jay).
- **Pehli vaar** app post nathi karti (sarkhamni mate kaal no hisab nathi): App → 📊 → "🔍 Aaj na bhav jovo" → saru lage to "🚀 Hamna post karo".
- **Aankda website jeva j** — AI kai badaltu nathi. Image apni design ma (brand rang), "સ્રોત: APMC ગોંડલ વેબસાઈટ · ભાવ માં ફેરફાર શક્ય". Logo/number nahi.
- Ghana bhav hoy to **carousel** (dar image ma sarkha bhav), story ma pehla 8, caption ma yadi; 5 hashtag (5 divas repeat nahi).
- "Fakt aa jansi" ma lakho (dakhla `કપાસ, મગફળી, ઘઉં, જીરૂ`) to fakt e j aave. **Unit** website par nathi — khabar hoy to lakho (dakhla `₹ પ્રતિ 20 કિલો`).
- Hamna: `python main.py --apmc --brand khedut_putra --dry-run` (fakt image).
⚠️ Website nu design badlay to bhav vanchata atki shake — tyare 🩺 Tapas ma laal dekhashe.

## #️⃣ Hashtag
- Darek post ma **post ne lagta 5 hashtag** (brand box → #️⃣ Hashtag ma sankhya badli shako).
- **Chhella 5 divas ma vaparelo hashtag e j account par fari nahi** — roj alag alag.
  "aakha brand ma kyay nahi" pasand karo to Facebook/Instagram/YouTube koi par pan 5 divas repeat nahi.
- AI ne pehla thi juna hashtag kahevay chhe; chhata repeat aave to app jate kadhi navo mangave chhe.
- ✏️ Sudharo thi tame jate badlo to e pan yaad rahe chhe.

## 💬 Comments no jate javab
Brand box → "💬 Comments no jate javab" chalu karo ane **FAQ** lakho (saranamu, phone, samay...).
AI fakt saada comment (aabhar, 👍, FAQ vala sawal) no j javab aape chhe. Fariyad, bhav, davai no doz ke na samjay evu — **tamne phone par khabar** aape chhe ane 💬 Comments ma rahe chhe.

## 🧑 Bolto chahero (HeyGen, paid)
Brand → Video kevo? → **🧑 Bolto chahero**. 🔗 Jodo ma `HEYGEN_API_KEY` umero → "🔄 HeyGen mathi yadi" → avatar ane avaaj pasand karo.
Kharch aashre $1–4 / minute (heygen.com). **Fakt HeyGen na avatar athva tamaro potano chahero** — bija sacha manas no nahi. Caption ma "🤖 AI ni madad thi banavelu" jate umeray chhe.

## 📤 WhatsApp / bija app ma share
📅 Aaj ma darek post par **📤** button: mobile ma image + text sidha WhatsApp Status/Channel ma share thay chhe.

## 🔒 Surakhsha

### ✅ Tamari rit: fakt PC + khabar fakt mara mobile par (default)
- `config.json` → `"access": "pc"` — app **fakt aa PC** (`http://localhost:8080`) par khule chhe. Mobile/WiFi/internet na raasta **band** — `--phone` lakho topan nahi khule.
- **PC par pan PIN (salah, PC bija vapre to):** 🔗 Jodo → "🔒 PC par pan PIN" (8+ akshar). **30 minute kai na karo to jate bahar** (`pc_idle_minutes`).
- **Khabar fakt tamari private Telegram chat ma** — chat id group/channel nu hoy to app message **mokle j nahi** ane 🩺 Tapas laal batave. (@userinfobot thi tamaro id lo, bot ne `/start` mokalo.)
- Roj nu backup Telegram par mokalvu ke nahi — 🔗 Jodo ma tick.
- Mobile/server pachhal thi joie to `"access": "phone"` / `"server"` — niche juo.

| Shu | Kem |
|---|---|
| **Computer par** `http://localhost:8080` | fakt e j computer thi khule chhe (PIN vagar) |
| **Mobile** `https://GHAR-NU-IP:8443` | **HTTPS** (potanu certificate — pehli vaar "Advanced → aagal vadho") + **PIN** |
| **PIN guess** | ek jagya thi **5 khota PIN → 15 minute lock**; ghani jagya thi 30 → badhu lock; Telegram par khabar |
| **Navo login** | dar navo login (phone/staff) → Telegram par khabar (IP, phone). Header ma **⏻ Bahar** |
| **Bijī website na chhupa hukam** (CSRF / DNS-rebinding) | Host + Origin + khas header tapas — bahar ni site hukam mokli nathi shakti |
| **Keys taalu** | `python main.py --lock` athva 🩺 Tapas → "🔐 Taalu maro". Keys **master password** thi encrypt (`.env.enc`); app chalu karta password puchhe chhe. `--unlock` thi pachhi kholo. **Password bhuli jao to keys nahi male.** |
| **Staff** | `APP_APPROVER_PIN` — fakt jovu/approve/comments; keys ane settings nahi |
| **Comments / News ma chhupa hukam** (prompt injection) | bahar nu lakhan AI ne "fakt data" tarike apay chhe; AI javab ma FAQ bahar nu link/phone/OTP/bank → javab **rokay**. Comments: ⛔ band · 👀 AI taiyar kare, tame moklo (salah) · ⚡ jate |
| **Online server** | `--server`: PIN 10+ akshar farjiyat; Docker ma app **fakt 127.0.0.1** par — internet par fakt **Cloudflare Tunnel** (HTTPS) thi |

**Tamare karvanu:** Facebook ane Google par **2-step verification** chalu karo · app fakt ghar/office na WiFi par · computer par password · shanka thay to Facebook → Settings → *Business integrations* ma app nu access band karo ane `APP_PIN` badlo.

## 🌐 24 kalak chalavo (computer band hoy topan)
**A) Online server (VPS, aashre ₹300–500/mahine — Hostinger, DigitalOcean, AWS Lightsail...):**
```
# server par: folder copy karo, .env bharo (APP_PIN 10+ akshar, APP_HOSTS=app.tamari-site.in, TUNNEL_TOKEN=...)
docker compose --profile tunnel up -d
```
App server ni bahar **sidhi nathi khulti** (fakt 127.0.0.1). Cloudflare (free) → Zero Trust → Tunnels → navo tunnel → token `.env` ma `TUNNEL_TOKEN` →
Public hostname: `app.tamari-site.in` → Service `http://social-app:8080`. Have `https://app.tamari-site.in` thi PIN sathe khulshe.
Facebook/Google "jodo" button mate pehli vaar computer par localhost thi jodi ne `.env` server par copy karo.

**B) Juno Android phone (free):** F-Droid mathi Termux → `bash android_termux_setup.sh` → `python main.py --app --phone`. Phone charger par rakho.

## 💸 FREE AI (koi kharch nahi)

App **pehla free AI vapre chhe**. Ek AI ni aaj ni free limit puri thay to e jate bija AI par jay chhe (`config.json` → `ai_providers`, upar thi niche na kram ma):

| Kram | AI | Kharch | Key kya thi |
|---|---|---|---|
| 1 | Google Gemini Flash-Lite | **Free** (divas ni limit) | https://aistudio.google.com → Get API key → `GEMINI_API_KEY` |
| 2 | Google Gemini Flash | **Free** (ochhi limit) | e j key |
| 3 | Groq (gpt-oss-120b) | **Free** (divas ni limit) | https://console.groq.com → `GROQ_API_KEY` |
| 4 | Ollama (tamara computer par) | **Sampurn free, koi limit nahi** | https://ollama.com install → `ollama pull gemma3:12b` |
| 5 | Claude Haiku | Paid (sasto) — key na hoy to chhodi de chhe | optional |

**Dhyan rakho:**
- Free limit kampani game tyare badli shake chhe. Tamari limit Google AI Studio ane Groq console ma joi shakay chhe.
- **Google na free plan ma tamaro data AI ne shikhavva vapari shakay chhe** (EU/UK bahar). Groq kahe chhe ke e tamara data thi shikhavtu nathi.
- Ghana account hoy to free limit ochhi padi shake. Tyare **Ollama** (computer par) ke `copy_from` vapro.
- Model na naam badlay to `config.json` ma `"model"` badlo. Ollama mate computer ma aashre 16 GB RAM saru.
- Kharch bachavva quality check hamna 1 vaar (`"max_rounds": 1`) rakhyo chhe.

## 1️⃣ Setup (ek j vaar)

1. **Python 3.10+** install karo: https://www.python.org/downloads/ (install vakhte "Add to PATH" tick karo).
2. Aa folder ma terminal kholo ane chalavo:
   ```
   pip install -r requirements.txt
   ```
3. **Gujarati font**: *Noto Sans Gujarati Bold* download karo (https://fonts.google.com/noto/specimen/Noto+Sans+Gujarati).
   `NotoSansGujarati-Bold.ttf` file ne `fonts/` folder ma muko. Font vagar image par Gujarati akshar sacha nahi dekhay.
4. `.env.example` ni copy banavi ne naam `.env` rakho. Ema tamari keys bharo (niche juo).
5. `config.json` kholo ane bharo:
   - `business_name`, `business_details` (shu vecho chho, shaher, phone, offer)
   - `topic`, `language`, `post_time` (dakhla: `"07:00"`)
   - `platforms` ma je vaparo chho tema `"enabled": true`, baki ma `false`
   - darek platform no alag `topic`, `tone`, `language` ane rang (`bg_top`, `bg_bottom`)

## 2️⃣ Test karo

```
python main.py --dry-run --sample   # AI key vagar, fakt image test
python main.py --dry-run            # sachu AI content bane (free AI), post nahi
```
Parinam `output/<brand>/<aaj-ni-tarikh>/<platform>/content.txt` ma juo.

## 3️⃣ Chalu karo

```
python main.py --now        # hamna j post karo
python main.py --schedule   # chalu rakho: roj post_time par jate post
```

**Computer band hoy topan chale e mate (free):** aa folder ne private GitHub repo ma muko.
Repo → Settings → Secrets and variables → Actions ma `ENV_FILE` naam nu ek Secret banavo ane ema aakhi `.env` file paste karo.
`.github/workflows/daily.yml` roj savare 7 vage (IST) jate chalshe.

## 🎥 Video (Reels / YouTube Shorts)

1. Roj `output/<brand>/<tarikh>/youtube/video_prompt.txt` kholo (Instagram mate `instagram/video_prompt.txt`).
2. Prompt ne AI video tool ma copy karo (Google Veo, Runway, Kling, Pika, CapCut AI).
3. Banelo video e j platform na folder ma `video.mp4` naam thi muko (dakhla `output/khedut_putra/<tarikh>/youtube/video.mp4`).
4. Chalavo:
   ```
   python main.py --brand khedut_putra --only youtube
   python main.py --brand khedut_putra --only instagram   # Reel mate
   ```

---

## 🔑 Keys kya thi malse?

Darek key ni aagal brand nu prefix lagado (`KHEDUT_`, `CHIRON_`, `BRAND3_` ...).

| Key | Kya thi |
|-----|---------|
| `GEMINI_API_KEY` (free) | https://aistudio.google.com → Get API key |
| `GROQ_API_KEY` (free) | https://console.groq.com → API Keys |
| `ANTHROPIC_API_KEY` (paid, optional) | https://console.anthropic.com → API Keys |
| `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN` | https://developers.facebook.com → App banavo → Graph API Explorer → Page token (`pages_manage_posts`, `pages_read_engagement`). Long-lived token banavo. |
| `IG_USER_ID`, `IG_ACCESS_TOKEN` | Instagram ne **Business/Creator** account banavi Facebook Page sathe jodo. Same Meta app ma `instagram_basic`, `instagram_content_publish` permission. |
| `PUBLIC_IMAGE_BASE_URL` | Instagram/Pinterest ne image no public link joie. `output/` folder ne tamari website/hosting par muko (dakhla `https://mysite.com/output`). GitHub vaparo to repo public kari GitHub Pages pan chale. |
| `THREADS_*` | https://developers.facebook.com → Threads API use case |
| `X_*` | https://developer.x.com → Project/App → Keys and tokens (Read and Write) |
| `LINKEDIN_*` | https://www.linkedin.com/developers → App → `w_member_social` (ke company page mate `w_organization_social`) |
| `PINTEREST_*` | https://developers.pinterest.com → App → token (`pins:write`, `boards:read`) |
| `TELEGRAM_*` | Telegram ma @BotFather thi bot banavo; bot ne channel ma admin banavo; chat id `@tamaro_channel` |
| YouTube | App → 🔗 Jodo → "YouTube jodo" (refresh token jate save thay chhe) |

> ⚠️ `.env` file koi ne na aapo ane public repo ma na muko. Ema tamara password jevi keys chhe.

## 🧠 Advance AI

### 1. Post nu quality check
AI pote lakheli post ne **10 mathi marks** aape chhe: hook, kahani, bhasha, CTA ane sachi mahiti.
**8 thi ochha** aave to bhul sudhari ne fari lakhe chhe (2 vaar sudhi), ane sauthi sari post j muke chhe.
`config.json` → `"quality": {"min_score": 8, "max_rounds": 2}`

### 2. Tahevar ane sizan
- Aaje tahevar hoy (Diwali, Uttarayan, Kisan Diwas...) to e divas ni **shubhechha post** bane chhe.
- 3 divas ma aavta tahevar ni pan vaat kare chhe.
- **Khedut Putra:** mahina pramane kheti ni sizan (vavani, piyat, lanni).
- **Chiron:** construction ni sizan (chomasa pehla waterproofing, garmi ma curing...).
- Tahevar ni yadi `festivals.json` ma chhe (2027 ni tarikh: Drik Panchang). **Dar varshe navi tarikh umero**. October pachhi app jate yaad karavshe.

### 3. Likes thi shikhe (hamesha mate)
- Darek post nu ID yaad rakhe chhe ane roj Facebook, Instagram, YouTube mathi likes, comments ane shares laave chhe.
- Aa data **kyarey kadhato nathi**. AI aa 3 vaat joi ne navi post banave chhe:
  - **badha samay ni** best ane nabdi post
  - **chhella 30 divas** no trend
  - **gaya varshe aa j mahine** shu chalyu (dakhla: gaya November ma rabi vavani ni post saari chali)
- Report jova:
  ```
  python main.py --report
  ```

## 🩺 Smart AI Doctor (bhul jate shodhe, tamne puchhi ne sudhare)

- **Badhi bhul ek sathe** tapase chhe. Ek j kaaran hoy to ek j sudharo kare chhe, bhale e ghani file ma hoy.
- **Juna sudhara hamesha yaad** rakhe chhe (`output/fixes_log.json`). Je sudharo pehla fail thayo ke tame na kahyo, te fari nathi sujhavto.
- Sudharo karya pachhi **app ne jate test** kare chhe. Test fail thay to badhu jate pachhu muki de chhe.
- Darek sudhara sathe **"AI ne vishvas: 8/10"** batave chhe.


App ma koi bhul aave to AI Doctor:
1. Bhul nu **kaaran saral Gujarati ma** samjave chhe.
2. **Sudharo sujhave** chhe ane juno/navo code batave chhe.
3. **Tamne puchhe chhe: "Aa sudharo karu? (ha/na)"**. Tame `ha` kaho to j sudharo kare chhe.
4. Sudharya pachhi file tapase chhe. Navi bhul aave to **juni file jate pachhi muki de chhe**.
5. Sudharo thay pachhi puchhe chhe: "fari try karu?"

Token jun thai gayo hoy ke permission khute, tevi bhul code ni nathi hoti. Tyare Doctor fakt **tamare shu karvanu** e kahe chhe.

**Computer par koi na hoy tyare** (schedule / GitHub): sudharo `output/fixes_pending.json` ma save thay chhe.
`.env` ma `ADMIN_TELEGRAM_*` bharo to phone par khabar pan aave chhe. Pachhi computer par chalavo:
```
python main.py --fix
```
(GitHub vaparta ho to pehla `git pull` karo.)

### ⏪ Juno version pachho lavvo (30 divas sudhi)
Darek sudhara pehla juni file `backups/` ma save thay chhe ane **1 mahina (30 divas) sudhi yaad rahe chhe**.
Hamesha rakhva hoy to `config.json` ma `"backup_keep_days": 0` karo.
```
python main.py --undo
```
Aa command chhella 30 divas na badha sudhara (tarikh + karan) ni yadi batave chhe. Number pasand karo ane `ha` kaho, etle e file juna version ma pachhi aavi jashe.
Undo pehla nu version pan save thay chhe, etle undo pan pachhu undo kari shakay.

> 🔒 `.env` (tamari keys) AI ne kyarey mokalati nathi, ane AI e file badli shaktu nathi. Error ma token aave to e pan chhupavi ne j mokle chhe.

## ❓ Takleef

- Koi platform `✗` batave to message vancho; mostly token jun (expire) thayo hoy ke permission khute.
- Ek j divas ma be vaar chalavo topan e ja platform par duplicate post nathi thatu (`posted.json`).
- AI content ne badalva `app/generator.py` ma `PROMPT` ane `PLATFORM_STYLE` sudharo.
- AI: free AI pehla vaparay chhe (upar "FREE AI" juo). Darek post mate 2–4 AI call thay chhe.
