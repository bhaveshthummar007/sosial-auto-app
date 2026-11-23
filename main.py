"""
Social Media Auto App
---------------------
Roj AI thi kahani, post, story, video prompt banave ane badha platforms par post kare.

Upayog:
  python main.py --now              aaje nu content banavi ne turant post karo
  python main.py --dry-run          fakt content + image banavo, post nahi
  python main.py --dry-run --sample API key vagar test
  python main.py --only youtube     aaje nu content fakt ek platform par (dakhla: video mukya pachhi)
  python main.py --brand khedut_putra --only youtube   fakt ek brand + ek platform
  python main.py --fix              AI Doctor e sujhavela sudhara juo ane ha/na kaho
  python main.py --undo             chhella 30 divas no koi sudharo pachho lo (juno version)
  python main.py --accounts         ek Meta token thi tamara BADHA Facebook Page + Instagram ni yadi
  python main.py --report           kai post ne ketla likes/comments malya (badha samay no)
  python main.py --app              📱 APP SCREEN kholo (browser ma) + schedule sathe chalu
  python main.py --app --phone      mobile thi pan kholi shakay (same WiFi, PIN sathe)
  python main.py --apmc --brand khedut_putra --dry-run   aaj na bajar bhav ni image (post vagar)
  python main.py --schedule         chalu rakho: roj config.json na post_time par jate chalshe
"""
import argparse
import datetime as dt
import json
import os
import sys
import time
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, ROOT)

from app import generator, image_maker  # noqa: E402
import importlib  # noqa: E402
from app import posters, doctor, insights, calendar_in, accounts, hashtags, concepts, photos, weather  # noqa: E402



def load_env(path=".env"):
    from app import vault
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            text = f.read()
    elif vault.locked():
        text = vault.open_text(interactive=sys.stdin.isatty())   # 🔐 taalu: password thi memory ma
    else:
        return
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load_cfg():
    with open("config.json", encoding="utf-8") as f:
        return json.load(f)


def now_local(cfg):
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(cfg.get("timezone", "Asia/Kolkata")))
    except Exception:  # Windows ma tzdata na hoy to Bharat no samay (+05:30)
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=5, minutes=30)))


def save_readable(c, day_dir):
    txt = f"""===== AAJ NU CONTENT ({os.path.basename(day_dir)}) =====

📖 KAHANI: {c['kahani_title']}
{c['kahani']}

📝 POST CAPTION:
{c['post_caption']}

🐦 SHORT POST (X/Threads):
{c['short_post']}

💼 LINKEDIN:
{c['linkedin_post']}

📱 STORY TEXT:
{c['story_text']}

🖼️ IMAGE QUOTE: {c['image_quote']}

#️⃣ HASHTAGS: {' '.join('#' + h for h in c['hashtags'])}

🎬 YOUTUBE TITLE: {c['youtube_title']}

🎙️ VIDEO VOICE-OVER SCRIPT:
{c['video_script']}

🎥 AI VIDEO PROMPT (Veo / Runway / Kling / Pika ma copy karo):
{c['video_prompt']}
"""
    with open(os.path.join(day_dir, "content.txt"), "w", encoding="utf-8") as f:
        f.write(txt)
    with open(os.path.join(day_dir, "video_prompt.txt"), "w", encoding="utf-8") as f:
        f.write(c["video_prompt"] + "\n\n--- Voice-over ---\n" + c["video_script"] + "\n")


def _load(path, default):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def _dump(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def run_brand(cfg, dry=False, sample=False, only=None, errors=None, day=None, schedule_at=None):
    """day: kaya divas ni post (default aaje). schedule_at: unix samay — Facebook/YouTube par aagal thi time set."""
    errors = [] if errors is None else errors
    posters.PREFIX = cfg.get("env_prefix", "")
    posters.FORMATS = accounts.formats_of(cfg)
    HISTORY = os.path.join("output", cfg["slug"], "history.json")
    the_day = day or now_local(cfg).date()
    today = the_day.isoformat()
    day_dir = os.path.join("output", cfg["slug"], today)
    os.makedirs(day_dir, exist_ok=True)

    try:
        jobs = accounts.build_jobs(cfg, only)
    except Exception as e:
        errors.append({"brand": cfg["slug"], "platform": "accounts", "message": str(e),
                       "traceback": traceback.format_exc()})
        print(f"✗ Accounts ni yadi na bani: {e}")
        return errors
    status_path = os.path.join(day_dir, "posted.json")
    status = _load(status_path, {})
    hist = _load(HISTORY, [])
    today_used = [h["theme"] for h in hist if h.get("date") == today]

    # Sachu havaman (brand ma shaher hoy to)
    wfacts = weather.facts_text(cfg.get("location")) if cfg.get("location") and not sample else ""
    if wfacts:
        print("🌦️ " + wfacts[:140] + "...")
    mode = cfg.get("post_image", "ai")  # ai / own / mix / plain

    # Tahevar + sizan
    cal = calendar_in.context_text(the_day, cfg)
    if cal != "No special occasion today.":
        print("📅 " + cal.replace("\n", "\n📅 "))
    # Likes thi shikhe: juni post na aankda update (hamesha mate save), darek account na potana token thi
    if cfg.get("learn_from_likes", True) and not sample:
        def getter(ov):
            return lambda n: (ov.get(n) or os.getenv((ov.get("_prefix") or posters.PREFIX) + n, "")).strip()
        hist = insights.refresh(hist, posters.PREFIX, getters={j["key"]: getter(j["overrides"]) for j in jobs})
        _dump(HISTORY, hist)

    delay = cfg.get("delay_between_posts_sec", 20)
    posted_any = False
    for job in jobs:
        key, name = job["key"], job["platform"]
        posters.OVERRIDES = job["overrides"]
        posters.set_location(cfg, job, today=today)  # 📍
        posters.set_collab(cfg, job, today=today)  # 🤝
        posters.GROUP_LINKS = job["extra"].get("group_links", [])
        jcfg = accounts.job_cfg(cfg, job)
        print(f"\n===== {cfg['business_name']} · {name.upper()}" + (f" · {job['name']}" if key != name else "") + " =====")
        pdir = os.path.join(day_dir, accounts.folder_name(job))
        os.makedirs(pdir, exist_ok=True)
        cpath = os.path.join(pdir, "content.json")
        try:
            # 1) Aa account mate alag content (aaje banelu hoy to fari vapro)
            if os.path.exists(cpath):
                content = _load(cpath, {})
                print("✓ Aaje nu content pehla thi chhe")
            elif job["extra"].get("copy_from"):
                src = os.path.join(day_dir, job["extra"]["copy_from"].replace(":", "__"), "content.json")
                if not os.path.exists(src):
                    raise RuntimeError(f"copy_from '{job['extra']['copy_from']}' nu content aaje nathi banyu (e account pehla aavvu joie)")
                content = _load(src, {})
                _dump(cpath, content)
                save_readable(content, pdir)
                print(f"✓ Content '{job['extra']['copy_from']}' mathi copy karyu (AI kharch bachyo)")
            else:
                topic = pick_topic(cfg, hist, today, key)
                if topic:
                    jcfg = dict(jcfg, platforms={**jcfg.get("platforms", {}),
                                                 name: {**jcfg.get("platforms", {}).get(name, {}), "topic": topic}})
                    print(f"🎯 Aaj no topic: {topic}")
                # 🔄 aaj no navo concept: prakar (7 divas repeat nahi)
                ptype = concepts.pick_type(cfg, hist, key, today, bool(wfacts))
                gtopic, gtype = guide_of_week(cfg, the_day)
                if gtopic:  # 📘 athvadiye ek vaar: ek vishay ni sampurn mahiti (lambo video)
                    ptype, topic = gtype, gtopic
                    vstyle = "cartoon" if cfg.get("video_style") == "cartoon" else "story"
                    jcfg = dict(jcfg, video_style=vstyle,
                                video_scenes=(cfg.get("crop_guide") or cfg.get("weekly_guide") or {}).get("scenes", 12),
                                platforms={**jcfg.get("platforms", {}),
                                           name: {**jcfg.get("platforms", {}).get(name, {}), "topic": topic}})
                    print(f"📘 Aaje athvadiyik sampurn mahiti video: {gtopic}")
                print(f"🔄 Aaj no prakar: {concepts.POST_TYPES[ptype][0]}")
                facts = wfacts
                from app import products
                prod = None if sample else products.pick(cfg, key, today)
                if prod:  # 🛒 aaje aa product ni post (bhav tamaro j)
                    facts = (facts + "\n" if facts else "") + products.facts_for(prod)
                    print(f"🛒 Aaj no product: {prod['name']} {prod.get('price', '')}")
                photo_path, photo_entry = None, None
                if mode in ("own", "mix") and (mode == "own" or int(today[-2:]) % 2 == 0):
                    photo_path, photo_entry = photos.pick(cfg["slug"], today)
                    if photo_entry:
                        desc = " ".join(x for x in (photo_entry.get("note", ""),
                                                    "" if sample else photos.describe(cfg, cfg["slug"], photo_entry)) if x)
                        facts = (facts + "\n" if facts else "") + \
                            f"Today's post uses OUR REAL PHOTO — write the post about/around it: {desc or 'a real photo from our work'}"
                        print(f"📸 Tamaro photo: {photo_entry['file']}")
                print("… AI thi aa account mate alag content bane chhe")
                content = (generator.sample_content(jcfg, name) if sample
                           else generator.generate(jcfg, name, HISTORY, today_used, calendar=cal,
                                                   learning=insights.learning_text(hist, key),
                                                   avoid_tags=hashtags.recent_list(hist, key, today, cfg),
                                                   post_type=concepts.type_instruction(ptype), facts=facts))
                content["_post_type"] = ptype
                if prod:
                    products.stamp(content, prod)
                if ptype not in concepts.CAROUSEL_TYPES:
                    content["slides"] = []
                if photo_entry:
                    content["_photo"] = photo_path
                    photos.mark_used(cfg["slug"], photo_entry["file"], today)
                hashtags.enforce(cfg, content, hist, key, today, allow_ai=not sample)
                print(f"#️⃣  {' '.join('#' + t for t in content['hashtags'])}")
                _dump(cpath, content)
                save_readable(content, pdir)
                today_used.append(content.get("theme", ""))
                if topic:
                    content["_topic"] = topic
                    _dump(cpath, content)
                hist.append({"date": today, "platform": key, "base": name, "account": job["name"],
                             "theme": content.get("theme", ""), "topic": topic, "hashtags": content.get("hashtags", []),
                             "post_type": content.get("_post_type")})
                _dump(HISTORY, hist)  # hamesha mate yaad
                print(f"✓ Content: {os.path.join(pdir, 'content.txt')}")

            # 2) Image: design (6 mathi, 7 divas ma badlay) + pachhal AI chitra / tamaro photo
            files = {}
            if cfg["image"].get("make_image", True):
                colors = generator.settings_for(jcfg, name)
                if "_template" not in content:
                    bg = content.get("_photo")
                    if not bg and mode in ("ai", "mix") and not sample and content.get("image_prompt"):
                        from app import story_video
                        bgp = os.path.join(pdir, "bg.jpg")
                        if story_video.gen_image(content["image_prompt"] + ". Realistic photograph, natural light, "
                                                 "high detail, no text, no watermark.", bgp,
                                                 __import__('zlib').crc32((today + key).encode()) % 10 ** 6, 1080, 1350):
                            bg = bgp
                    content["_template"] = concepts.pick_template(hist, key, today, has_photo=bool(bg))
                    content["_bg"] = bg
                    _dump(cpath, content)
                    for h in reversed(hist):
                        if h.get("date") == today and h.get("platform") == key:
                            h["template"] = content["_template"]
                            break
                    _dump(HISTORY, hist)
                raw = bool(content.get("_photo")) and not cfg.get("own_photo_text", False)
                files["post"], files["story"] = image_maker.make_images(
                    content, cfg, pdir, colors, content["_template"], content.get("_bg"), raw_photo=raw)
                print("✓ Image: " + ("tamaro photo (emno em)" if raw else f"design '{content['_template']}'"
                                         + (" + pachhal chitra" if content.get("_bg") else "")))
                if content.get("slides") and "carousel" in posters.FORMATS:
                    files["slides"] = image_maker.make_slides(content["slides"], cfg, pdir, colors, content.get("_bg"),
                                                              content.get("cover_title") or content.get("kahani_title", ""))
                    print(f"🎠 Carousel: {len(files['slides'])} slide")
                # 🏷️ upar page/account nu naam (60% dekhay)
                nm = image_maker.display_name(cfg, job)
                if nm and (cfg.get("name_on_post") or {}).get("enabled", True):
                    files["post"] = image_maker.stamp_name(files["post"], nm, cfg)
                    files["story"] = image_maker.stamp_name(files["story"], nm, cfg)
                    if files.get("slides"):
                        files["slides"] = [image_maker.stamp_name(s, nm, cfg) for s in files["slides"]]
                    print(f"🏷️  Naam: {nm}")
            vid = os.path.join(pdir, "video.mp4")
            if (not os.path.exists(vid) and files.get("story") and cfg.get("auto_video", True)
                    and posters.FORMATS & {"reel", "video"} and name in ("facebook", "instagram", "youtube")):
                try:
                    from app import video_maker
                    vs = jcfg.get("video_style", cfg.get("video_style", "simple"))
                    if vs == "avatar" and not sample:
                        from app import heygen
                        script = content.get("video_script") or content.get("post_caption", "")
                        heygen.make(script, vid, cfg.get("heygen_avatar_id", ""), cfg.get("heygen_voice_id", ""))
                    elif vs in ("story", "cartoon") and not sample:
                        from app import story_video
                        print(f"🎬 {'Cartoon' if vs == 'cartoon' else 'Kahani'} video bane chhe (thodi minute lagshe)...")
                        story_video.make(cfg, content, vid, name, vs, jcfg.get("video_scenes", cfg.get("video_scenes", 6)),
                                         cfg.get("voice", "female"), today + key,
                                         stamp=image_maker.display_name(cfg, job))
                    else:
                        video_maker.make_reel(files["story"], vid, cfg.get("video_seconds", 12),
                                              video_maker.pick_music(today + key))
                    print("🎬 Reel/Video jate banyo: video.mp4")
                except Exception as e:
                    print(f"  ! Video na banyo ({e}) — image post thashe")
            if os.path.exists(vid):
                files["video"] = vid
                print("✓ Video: video.mp4")

            # AI label: sacha dekhata AI chitra/video hoy to caption ma lakho (Meta/YouTube niyam)
            if cfg.get("ai_label", True) and (cfg.get("video_style") in ("story", "cartoon", "avatar")) \
                    and files.get("video") and "#AIgenerated" not in content.get("post_caption", ""):
                content = dict(content, post_caption=content.get("post_caption", "") + "\n\n🤖 AI ni madad thi banavelu #AIgenerated",
                               _ai_video=True)

            if dry:
                continue

            # 3) Post
            if status.get(key, {}).get("ok"):
                print("• aaje pehla j post thai gayu chhe")
                continue
            if cfg.get("approval_required") and not content.get("_approved"):
                print("⏸  Approval baki — App ma joi ne ✅ Approve karo, pachhi j post thashe")
                continue
            if name not in posters.POSTERS:
                ok, msg = False, "aa platform app ma nathi"
            else:
                if posted_any and delay:
                    time.sleep(delay)  # ek sathe ghani post thi spam na lage
                if schedule_at and name not in posters.ADVANCE_OK:
                    ok, msg = False, "aa platform aagal thi time set nathi aaptu"
                else:
                    posters.SCHEDULE_AT = schedule_at
                    from app import promo
                    to_post = promo.apply(cfg, key, hist, content)  # 🔁 kyarek biju potanu page pan
                    try:
                        ok, msg = posters.POSTERS[name](to_post, files)
                    finally:
                        posters.SCHEDULE_AT = None
                    if ok and schedule_at and name == "facebook" and "story" in posters.FORMATS and files.get("story"):
                        # Facebook story aagal thi set nathi thati → e samaye Queue mathi (PC chalu hoy to)
                        from app import queue_mgr
                        when = dt.datetime.fromtimestamp(schedule_at, now_local(cfg).tzinfo).strftime("%Y-%m-%dT%H:%M")
                        queue_mgr.add_item(cfg["slug"], [key], when, dict(content, _story_only=True),
                                           story=files["story"], note="fb-story")
                posted_any = True
        except Exception as e:
            ok, msg = False, str(e)
            body = getattr(getattr(e, "response", None), "text", "")
            if body:
                msg += " | " + body[:300]
            errors.append({"brand": cfg["slug"], "platform": key, "message": msg,
                           "traceback": traceback.format_exc()})
            if dry:
                print(f"✗ Bhul: {msg}")
        if dry:
            continue
        status[key] = {"ok": ok, "msg": msg, "time": now_local(cfg).isoformat()}
        if schedule_at and ok:
            status[key]["scheduled_for"] = dt.datetime.fromtimestamp(schedule_at, now_local(cfg).tzinfo).isoformat(timespec="minutes")
        print(f"{'✓' if ok else '✗'} POST: {msg}")
        pid = insights.extract_id(msg) if ok else None
        if pid:  # post id yaad rakho, jethi pachhi likes joi shakay
            for h in reversed(hist):
                if h.get("date") == today and h.get("platform") == key:
                    h["post_id"] = pid
                    h["posted_at"] = now_local(cfg).isoformat(timespec="minutes")
                    break
            _dump(HISTORY, hist)
        _dump(status_path, status)
    posters.OVERRIDES, posters.GROUP_LINKS, posters.LOCATION, posters.COLLAB = {}, [], {}, []
    return errors


def guide_of_week(cfg, day):
    """📘 Athvadiyik 'sampurn mahiti' video: (vishay, prakar) athva (None, None).
    Kheti brand: 'crop_guide' (fasal_guide) · baki: 'weekly_guide' (sampurn_guide)."""
    crop = crop_of_week(cfg, day)
    if crop:
        return f"{crop} ni kheti ni sampurn mahiti — vavni thi vechan sudhi", "fasal_guide"
    subj = crop_of_week({"crop_guide": cfg.get("weekly_guide") or {}}, day)
    return (f"{subj} — sampurn mahiti", "sampurn_guide") if subj else (None, None)


def crop_of_week(cfg, day):
    """🌱 'crop_guide' chalu hoy ane aaje e var hoy to aa athvadiya no pak (yadi mathi kram thi), nahi to None."""
    cg = cfg.get("crop_guide") or {}
    crops = [c for c in cg.get("crops", []) if str(c).strip()]
    if not cg.get("enabled") or not crops or day.weekday() != int(cg.get("weekday", 2)):
        return None
    return crops[(day.toordinal() // 7) % len(crops)]


def pick_topic(cfg, hist, today, key):
    """Brand na FINAL topic mathi aaj no: sauthi lamba samay thi na vaparelo, ane aaje bija account par na hoy te."""
    topics = [t for t in cfg.get("topics", []) if t.strip()]
    if not topics:
        return None
    last = {}
    for i, h in enumerate(hist):
        if h.get("topic"):
            last[h["topic"]] = i
    used_today = {h.get("topic") for h in hist if h.get("date") == today}
    pool = [t for t in topics if t not in used_today] or topics
    import random as _r
    rnd = _r.Random(today + key)
    return min(pool, key=lambda t: (last.get(t, -1), rnd.random()))


def _reload():
    """AI Doctor e code sudharyo hoy to navo code load karo."""
    for mod in (generator, image_maker, posters):
        importlib.reload(mod)


def retry(fixed, dry=False, sample=False):
    """Sudharo thaya pachhi, puchhi ne, e j platform fari chalavo."""
    if not fixed or not sys.stdin.isatty():
        return
    if not doctor._ask("\n🔁 Sudharo thayo. Je bhul aavi hati te have fari try karu?"):
        return
    _reload()
    cfg = load_cfg()
    base = {k: v for k, v in cfg.items() if k != "brands"}
    for err in fixed:
        b = next((x for x in cfg["brands"] if x["slug"] == err.get("brand")), None)
        if b:
            print(f"\n🔁 Fari try: {b['business_name']} · {err.get('platform')}")
            errs = run_brand({**base, **b}, dry=dry, sample=sample, only=err.get("platform"))
            print("❌ Haju bhul chhe — 'python main.py --fix' athva --now fari chalavo." if errs else "✅ Have barabar chale chhe!")


def festival_warning():
    """Aavta varsh na tahevar ni tarikh festivals.json ma nathi to yaad karavo."""
    try:
        data = _load("festivals.json", {})
        nxt = dt.date.today().year + 1
        if dt.date.today().month >= 10 and not any(f["date"].startswith(str(nxt)) for f in data.get("dated", [])):
            print(f"⚠️  festivals.json ma {nxt} na tahevar (Diwali, Holi...) ni tarikh nathi — umero.")
    except Exception:
        pass


def show_report(cfg):
    for b in cfg["brands"]:
        if not b.get("enabled", True):
            continue
        print(f"\n################ {b['business_name']} ################")
        print(insights.report(_load(os.path.join("output", b["slug"], "history.json"), [])))


def run_once(cfg, dry=False, sample=False, only=None, brand=None, use_doctor=True):
    base = {k: v for k, v in cfg.items() if k != "brands"}
    errors = []
    festival_warning()
    try:
        for b in cfg["brands"]:
            if brand and brand not in (b["slug"], b["business_name"]):
                continue
            if not brand and not b.get("enabled", True):
                continue
            print(f"\n################ {b['business_name']} ################")
            run_brand({**base, **b}, dry=dry, sample=sample, only=only, errors=errors)
    except Exception as e:
        errors.append({"brand": "-", "platform": "-", "message": str(e), "traceback": traceback.format_exc()})
        print(f"✗ App ma bhul: {e}")
    if dry:
        print("\n(Dry-run: koi post karyu nathi.)")
    if errors and not use_doctor:
        sys.exit(1)
    if errors:
        print(f"\n🩺 {len(errors)} bhul malyi — AI Doctor tapase chhe...")
        retry(doctor.handle(errors, base), dry=dry, sample=sample)


def _due_jobs(cfg, now, done):
    """Aa ghadi e kaya (brand, account) no samay thayo chhe."""
    out = []
    base = {k: v for k, v in cfg.items() if k != "brands"}
    today = now.date().isoformat()
    hhmm = now.strftime("%H:%M")
    for b in cfg["brands"]:
        if not b.get("enabled", True):
            continue
        bc = {**base, **b}
        from app import free_video
        if free_video.skip_regular(bc):
            continue  # 🎬 aa brand fakt movie/series muke chhe
        hist = _load(os.path.join("output", b["slug"], "history.json"), [])
        day = os.path.join("output", b["slug"], today)
        posted = _load(os.path.join(day, "posted.json"), {})
        try:
            jobs = accounts.build_jobs(bc)
        except Exception:
            continue
        for j in jobs:
            t = accounts.job_time(bc, j, insights.best_hour(hist, j["key"]), now.date())
            if posted.get(j["key"], {}).get("ok"):
                continue
            tag = (today, b["slug"], j["key"])
            if bc.get("approval_required"):
                # pehla content taiyar (samay thi 'prepare_minutes' pehla), approve thay etle post
                prep = (dt.datetime.combine(now.date(), dt.time.fromisoformat(t))
                        - dt.timedelta(minutes=bc.get("prepare_minutes", 120))).strftime("%H:%M")
                c = _load(os.path.join(day, accounts.folder_name(j), "content.json"), None)
                if hhmm >= prep and c is None and tag + ("prep",) not in done:
                    out.append((b["slug"], j["key"], True, tag + ("prep",)))
                elif hhmm >= t and c and c.get("_approved") and tag not in done:
                    out.append((b["slug"], j["key"], False, tag))
            elif hhmm >= t and tag not in done:
                # computer/app modu chalu thayu: 'catch_up_minutes' thi vadhare modu hoy to aaje chhodi do
                late = (now.replace(tzinfo=None) - dt.datetime.combine(now.date(), dt.time.fromisoformat(t))).total_seconds() / 60
                if late <= bc.get("catch_up_minutes", 180):
                    out.append((b["slug"], j["key"], False, tag))
                else:
                    done.add(tag)
                    print(f"⏭  {b['slug']} · {j['key']}: samay {t} hato, {int(late)} minute modu — aaje chhodyu "
                          f"(App ma 🚀 Post thi hamna kari shako)")
    return out


def advance_jobs(cfg, now):
    """⏰ Je platform par aagal thi time set thai shake (Facebook Page, YouTube), te post pehla thi j mukvi —
    pachhi e samaye PC band hoy topan post thai jay. Return [(slug, key, date, unix)]."""
    out = []
    if not cfg.get("advance_schedule", True):
        return out
    base = {k: v for k, v in cfg.items() if k != "brands"}
    days = max(1, min(7, int(cfg.get("advance_days", 1))))
    for b in cfg["brands"]:
        if not b.get("enabled", True):
            continue
        bc = {**base, **b}
        from app import free_video
        if free_video.skip_regular(bc):
            continue
        hist = _load(os.path.join("output", b["slug"], "history.json"), [])
        try:
            jobs = [j for j in accounts.build_jobs(bc) if j["platform"] in posters.ADVANCE_OK]
        except Exception:
            continue
        for i in range(days + 1):  # aaje (baki hoy to) + aavta divas
            d = now.date() + dt.timedelta(days=i)
            if i and bc.get("approval_required"):
                continue  # approval vala: aaj nu approve thay pachhi j (kaal nu content App ma dekhatu nathi)
            ddir = os.path.join("output", b["slug"], d.isoformat())
            posted = _load(os.path.join(ddir, "posted.json"), {})
            for j in jobs:
                if posted.get(j["key"], {}).get("ok"):
                    continue
                t = accounts.job_time(bc, j, insights.best_hour(hist, j["key"]), d)
                when = dt.datetime.combine(d, dt.time.fromisoformat(t), tzinfo=now.tzinfo)
                mins = (when - now).total_seconds() / 60
                if mins < cfg.get("advance_min_minutes", 20) or mins > 29 * 24 * 60:
                    continue  # Facebook: 10 minute thi 30 divas vachche j
                if bc.get("approval_required"):
                    c = _load(os.path.join(ddir, accounts.folder_name(j), "content.json"), None)
                    if not (c and c.get("_approved")):
                        continue
                out.append((b["slug"], j["key"], d, int(when.timestamp())))
    return out


def run_advance(cfg, now):
    """Aagal thi time set karo; je thayu tenu Telegram par ek sandesh."""
    from app import maintenance
    base = {k: v for k, v in cfg.items() if k != "brands"}
    done = []
    for slug, key, d, ts in advance_jobs(cfg, now):
        b = next(x for x in cfg["brands"] if x["slug"] == slug)
        print(f"\n⏰ Aagal thi time set — {slug} · {key} · {d} {dt.datetime.fromtimestamp(ts, now.tzinfo):%H:%M}")
        errs = []
        run_brand({**base, **b}, only=key, errors=errs, day=d, schedule_at=ts)
        st = _load(os.path.join("output", slug, d.isoformat(), "posted.json"), {}).get(key, {})
        if st.get("ok"):
            done.append(f"{b['business_name']} · {key}: {d:%d-%m} {dt.datetime.fromtimestamp(ts, now.tzinfo):%H:%M}")
        elif errs:
            print(f"  ! na thayu: {errs[-1]['message'][:200]} — e samaye PC chalu hoy to sadharan rite post thashe")
    if done:
        maintenance.notify("⏰ Aagal thi time set thai (PC band hoy topan jashe):\n" + "\n".join(done))
    return done


def schedule_loop(cfg=None):
    from app import queue_mgr
    print("⏰ Schedule chalu chhe — darek account potana samaye, ane Queue ni post samay thay tyare. Band karva Ctrl+C.")
    from app import maintenance
    done = set()
    last_reply = 0.0
    last_leads = 0.0
    last_adv = 0.0
    while True:
        try:
            cfg = load_cfg()
            now = now_local(cfg)
            queue_mgr.process_due(cfg, now)
            # ⏰ Facebook/YouTube: aaj-kaal ni post aagal thi time set (darek 30 min tapase)
            if time.time() - last_adv > 1800:
                last_adv = time.time()
                try:
                    run_advance(cfg, now)
                except Exception:
                    traceback.print_exc()
            # raat ni sambhal (backup, token yaad, juni media)
            ntag = (now.date().isoformat(), "nightly")
            if now.strftime("%H:%M") >= cfg.get("maintenance_time", "23:30") and ntag not in done:
                done.add(ntag)
                try:
                    maintenance.nightly(cfg)
                except Exception:
                    traceback.print_exc()
            # 📇 Lead: comment ma "bhav/kaam/number" → yadi + number sathe javab (darek 30 min)
            if time.time() - last_leads > 1800:
                last_leads = time.time()
                try:
                    from app import leads
                    nl, ns = leads.run(cfg, now)
                    if nl:
                        print(f"📇 {nl} navo lead ({ns} ne javab)")
                except Exception:
                    traceback.print_exc()
            # comments no jate javab (darek 30 min)
            if any(b.get("auto_reply") or b.get("auto_reply_mode", "off") != "off" for b in cfg["brands"]) \
                    and time.time() - last_reply > 1800:
                last_reply = time.time()
                try:
                    s, k = maintenance.auto_reply(cfg)
                    if s or k:
                        print(f"💬 Jate javab: {s}, tamara mate: {k}")
                except Exception:
                    traceback.print_exc()
            # 📰 News: roj 'prepare_time' e khabar shodhi draft/queue banavo
            from app import news as newsmod
            for b in cfg["brands"]:
                nc = {**newsmod.DEFAULT, **(b.get("news") or {})}
                ntag = (now.date().isoformat(), b["slug"], "news")
                if b.get("enabled", True) and nc.get("enabled") and ntag not in done \
                        and now.strftime("%H:%M") >= nc["prepare_time"]:
                    done.add(ntag)
                    try:
                        n, msg = newsmod.prepare({**{k: v for k, v in cfg.items() if k != "brands"}, **b}, now)
                        print(f"📰 {b['business_name']}: {msg}")
                        if n and nc.get("approval", True):
                            maintenance.notify(f"📰 {b['business_name']}: {n} khabar approval mate taiyar — App → ⏳ Queue")
                    except Exception as e:
                        print(f"📰 News bhul: {e}")
            # 📊 Bajar bhav (APMC): window ma darek 15 min tapaso
            from app import apmc
            base = {k: v for k, v in cfg.items() if k != "brands"}
            for b in cfg["brands"]:
                bc = {**base, **b}
                if b.get("enabled", True) and apmc.due(bc, now):
                    try:
                        ok, msg = apmc.run(bc, now)
                        print(f"📊 {now:%H:%M} {b['business_name']} bajar bhav: {msg}")
                        if ok:
                            maintenance.notify(f"📊 {b['business_name']}: aaj na bajar bhav post thaya ✓")
                    except Exception as e:
                        print(f"📊 Bajar bhav bhul: {e}")
                        st = apmc._load(apmc.state_path(b["slug"]), {})
                        st["last_check"] = now.isoformat(timespec="minutes")
                        st["last_error"] = str(e)[:200]
                        apmc._dump(apmc.state_path(b["slug"]), st)
            # 📈 Athvadiyik report Telegram par (Ravivare 20:00)
            from app import weekly_report
            if weekly_report.due(cfg, now):
                try:
                    weekly_report.run(cfg, now)
                    print("📈 Athvadiyik report mokalyo")
                except Exception:
                    traceback.print_exc()
            # 📺 Athvadiyik lambo cartoon video (Ravivare)
            from app import compilation
            for b in cfg["brands"]:
                bc = {**base, **b}
                if b.get("enabled", True) and compilation.due(bc, now):
                    print(f"\n📺 {b['business_name']}: athvadiya no lambo video bane chhe...")
                    try:
                        ok, msg = compilation.run(bc, now)
                    except Exception as e:
                        ok, msg = False, str(e)[:300]
                    print(("✓ " if ok else "✗ ") + msg)
                    maintenance.notify(f"📺 {b['business_name']} athvadiyik video: " + msg[:300])
            # 🎬 Movie / series: darek nakki samaye aagal no bhag
            from app import free_video
            for b in cfg["brands"]:
                bc = {**base, **b}
                slot = free_video.due_slot(bc, now) if b.get("enabled", True) else None
                if slot:
                    print(f"\n🎬 {now:%H:%M} {b['business_name']}: aagal no bhag bane chhe (thodi minute lagshe)...")
                    try:
                        ok, msg = free_video.run(bc, now, slot=slot)
                        print(("✓ " if ok else "✗ ") + msg)
                        maintenance.notify(f"🎬 {b['business_name']}: " + msg[:300])
                    except Exception as e:
                        free_video.mark_slot(b["slug"], now, slot, str(e))
                        print(f"🎬 Movie bhul: {e}")
            for brand, key, dry, tag in _due_jobs(cfg, now, done):
                done.add(tag)
                print(f"\n⏰ {now:%H:%M} — {brand} · {key}" + (" (content taiyar, approval mate)" if dry else ""))
                run_once(cfg, dry=dry, only=key, brand=brand)
            # approve thayela pachhi post thay e mate 'done' ma approval vala ne fari tapasva do
            done = {t for t in done if t[0] == now.date().isoformat()}
        except Exception:
            traceback.print_exc()
        time.sleep(30)


def main():
    ap = argparse.ArgumentParser(description="Social Media Auto App")
    ap.add_argument("--now", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--brand", help="khedut_putra athva chiron_enterprise")
    ap.add_argument("--schedule", action="store_true")
    ap.add_argument("--advance", action="store_true", help="Facebook/YouTube ni aaj-kaal ni post hamna aagal thi time set karo")
    ap.add_argument("--app", action="store_true", help="App screen kholo (browser ma)")
    ap.add_argument("--phone", action="store_true", help="--app sathe: mobile thi pan kholi shakay (PIN sathe)")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--server", action="store_true", help="online server (Cloudflare Tunnel pachhal)")
    ap.add_argument("--no-https", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--backup", action="store_true", help="hamna backup banavo")
    ap.add_argument("--lock", action="store_true", help="keys ne master password thi taalu")
    ap.add_argument("--unlock", action="store_true", help="taalu kholi .env pachhi banavo")
    ap.add_argument("--weekly-report", action="store_true", help="athvadiyik report hamna banavo ane Telegram par moklo")
    ap.add_argument("--weekly", action="store_true", help="--brand sathe: athvadiya no lambo cartoon video hamna (--dry-run = fakt banavo)")
    ap.add_argument("--movie", action="store_true", help="--brand sathe: aagal no movie/series bhag hamna (--dry-run = fakt banavo)")
    ap.add_argument("--apmc", action="store_true", help="--brand sathe: bajar bhav hamna (--dry-run = fakt image)")
    ap.add_argument("--force", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--news", action="store_true", help="--brand sathe: hamna news shodhi draft banavo")
    ap.add_argument("--sample-video", action="store_true", help="--brand sathe: ek sample kahani/cartoon video banavo")
    ap.add_argument("--fix", action="store_true", help="AI Doctor na baki sudhara juo")
    ap.add_argument("--undo", action="store_true", help="chhella 30 divas no koi sudharo pachho lo")
    ap.add_argument("--report", action="store_true", help="kai post ne ketla likes malya")
    ap.add_argument("--accounts", action="store_true", help="META_USER_TOKEN thi badha Page/Instagram ni yadi")
    ap.add_argument("--no-doctor", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()

    if a.lock or a.unlock:
        import getpass
        from app import vault
        if a.lock:
            if not os.path.exists(".env"):
                print(".env nathi (pehla thi taalu hoy to --unlock)")
                return
            p1 = getpass.getpass("🔐 Navo master password (8+ akshar): ")
            if p1 != getpass.getpass("Fari lakho: "):
                print("✗ Banne password sarkha nathi")
                return
            vault.lock(p1)
            print("✅ Keys taalu mari didhi (.env.enc). Password yaad rakho — bhuli jao to keys pachhi nahi male.")
        else:
            vault.unlock_to_file(getpass.getpass("🔐 Master password: "))
            print("✅ .env pachhi bani. Sudharya pachhi fari: python main.py --lock")
        return
    load_env()
    cfg = load_cfg()
    try:  # pehli vaar: Gujarati font jate
        from app import fonts
        if fonts.missing():
            fonts.ensure()
    except Exception:
        pass
    if a.news:
        from app import news as newsmod
        base = {k: v for k, v in cfg.items() if k != "brands"}
        b = next(x for x in cfg["brands"] if x["slug"] == a.brand)
        try:
            n, msg = newsmod.prepare({**base, **b}, now_local(cfg))
        except Exception as e:
            n, msg = 0, f"News na bani: {str(e)[:200]}"
        print(("✅ " if n else "⚠️ ") + msg)
        return
    if a.weekly_report:
        from app import weekly_report
        sent, text = weekly_report.run(cfg, now_local(cfg))
        print(text + ("\n\n✅ Telegram par mokalyo" if sent else "\n\n(Telegram set nathi — fakt ahi batavyo)"))
        return
    if a.weekly:
        from app import compilation
        base = {k: v for k, v in cfg.items() if k != "brands"}
        b = next(x for x in cfg["brands"] if x["slug"] == a.brand)
        try:
            ok, msg = compilation.run({**base, **b}, now_local(cfg), dry=a.dry_run)
        except Exception as e:
            ok, msg = False, str(e)[:300]
        print(("✅ " if ok else "⚠️ ") + msg)
        return
    if a.movie:
        from app import free_video
        base = {k: v for k, v in cfg.items() if k != "brands"}
        b = next(x for x in cfg["brands"] if x["slug"] == a.brand)
        try:
            ok, msg = free_video.run({**base, **b}, now_local(cfg), dry=a.dry_run)
        except Exception as e:
            ok, msg = False, str(e)[:300]
        print(("✅ " if ok else "⚠️ ") + msg)
        return
    if a.apmc:
        from app import apmc
        base = {k: v for k, v in cfg.items() if k != "brands"}
        b = next(x for x in cfg["brands"] if x["slug"] == a.brand)
        try:
            ok, msg = apmc.run({**base, **b}, now_local(cfg), force=a.force or a.dry_run, dry=a.dry_run)
        except Exception as e:
            ok, msg = False, f"Website na khuli — internet tapaso athva thodi var pachhi try karo ({str(e)[:120]})"
            st = apmc._load(apmc.state_path(b["slug"]), {})
            st["last_error"] = msg
            apmc._dump(apmc.state_path(b["slug"]), st)
        print(("✅ " if ok else "⚠️ ") + msg)
        return
    if a.backup:
        from app import maintenance
        print("💾", maintenance.backup())
        return
    if a.sample_video:
        from app import story_video
        base = {k: v for k, v in cfg.items() if k != "brands"}
        b = next(x for x in cfg["brands"] if x["slug"] == a.brand)
        bc = {**base, **b}
        topic = (b.get("topics") or [b.get("default", {}).get("topic", "")])[0]
        print(f"🎯 Topic: {topic}")
        jc = dict(bc, platforms={**bc.get("platforms", {}), "instagram": {**bc.get("platforms", {}).get("instagram", {}), "topic": topic}})
        try:
            content = generator.generate(dict(jc, quality={"enabled": False}), "instagram", os.path.join("output", b["slug"], "history.json"), [])
        except Exception as e:
            print(f"  ! AI na chalyu ({str(e)[:120]}) — sample kahani")
            content = generator.sample_content(bc, "instagram")
        out = os.path.join("output", b["slug"], "sample_video.mp4")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        story_video.make(bc, content, out, "instagram", b.get("video_style", "cartoon") if b.get("video_style") in ("story", "cartoon") else "cartoon",
                         b.get("video_scenes", 6), b.get("voice", "female"), str(time.time()))
        print(f"\n✅ Sample video taiyar: {out}")
    elif a.app:
        from app import dashboard
        access = os.getenv("APP_ACCESS") or cfg.get("access", "pc")
        if access == "pc" and (a.phone or a.server):
            print("🔒 PC-only mode chalu chhe — mobile/server raasta band. App fakt aa PC par khulshe.\n"
                  "   (badalvu hoy to config.json ma \"access\": \"phone\" athva \"server\")")
            a.phone = a.server = False
        if a.server and access != "server":
            raise SystemExit("🔒 Server mode mate config.json ma \"access\": \"server\" (athva APP_ACCESS=server) joie.")
        dashboard.serve(phone=a.phone, port=a.port, schedule=schedule_loop, server=a.server, https=not a.no_https)
    elif a.accounts:
        print(accounts.discover(cfg))
    elif a.report:
        show_report(cfg)
    elif a.undo:
        doctor.undo()
    elif a.fix:
        retry(doctor.review_pending(cfg))
    elif a.schedule:
        schedule_loop(cfg)
    elif a.advance:
        d = run_advance(cfg, now_local(cfg))
        print("\n⏰ " + (f"{len(d)} post aagal thi time set thai" if d else "Aagal thi set karva jevu kai baki nathi"))
    elif a.now or a.dry_run or a.only:
        run_once(cfg, dry=a.dry_run, sample=a.sample, only=a.only, brand=a.brand, use_doctor=not a.no_doctor)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
