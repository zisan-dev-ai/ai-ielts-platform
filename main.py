import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
import json
import uvicorn
import hashlib
import re
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, Request, Form, Depends, HTTPException, Body, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

from database import get_db, init_db
from seed_data import seed_all_77_types
from scoring_engine.objective_scoring import ObjectiveScoringEngine
from scoring_engine.writing_evaluator import WritingEvaluatorEngine
from scoring_engine.speaking_evaluator import SpeakingEvaluatorEngine
from scoring_engine.adaptive_learning import AdaptiveLearningEngine
from ai_engine.ai_router import ai_router

app = FastAPI(title="AI IELTS — World-Class Learning Ecosystem", version="1.0.0")

# Mount Static Files & Templates
BASE_DIR = os.path.dirname(__file__)
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
if os.path.exists(os.path.join(BASE_DIR, "static", "audio")):
    app.mount("/audio", StaticFiles(directory=os.path.join(BASE_DIR, "static", "audio")), name="audio")
if os.path.exists(os.path.join(BASE_DIR, "static", "videos")):
    app.mount("/videos", StaticFiles(directory=os.path.join(BASE_DIR, "static", "videos")), name="videos")
if os.path.exists(os.path.join(BASE_DIR, "static", "js")):
    app.mount("/js", StaticFiles(directory=os.path.join(BASE_DIR, "static", "js")), name="js")
if os.path.exists(os.path.join(BASE_DIR, "static", "css")):
    app.mount("/css", StaticFiles(directory=os.path.join(BASE_DIR, "static", "css")), name="css")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Custom Jinja2 Filter for JSON parsing in templates
def from_json_filter(value):
    if not value: return []
    try: return json.loads(value)
    except: return []

templates.env.filters["from_json"] = from_json_filter

@app.on_event("startup")
def startup_db_check():
    init_db()
    from ai_engine.health_checker import KeyPoolHealthChecker
    KeyPoolHealthChecker.seed_credentials_from_env()
    seed_all_77_types()

@app.get("/api/v1/listening/audio/{section_num}")
def get_listening_audio(section_num: int):
    static_file = os.path.join(BASE_DIR, "static", "audio", f"section{section_num}.mp3")
    
    # Check DB for active transcript
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT passage_or_context FROM questions WHERE skill = 'Listening' AND section_number = ? LIMIT 1", (section_num,))
    row = cursor.fetchone()
    conn.close()
    
    transcript = row["passage_or_context"] if row and row["passage_or_context"] else ""
    if not transcript and os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
        
    cache_dir = os.path.join(BASE_DIR, "static", "audio", "cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    trans_hash = hashlib.md5(transcript.strip().encode('utf-8')).hexdigest()
    cached_mp3 = os.path.join(cache_dir, f"sec_{section_num}_{trans_hash}.mp3")
    
    if os.path.exists(cached_mp3) and os.path.getsize(cached_mp3) > 1000:
        return FileResponse(cached_mp3, media_type="audio/mpeg")
        
    # If transcript matches default Set A and static file exists, use static file
    if section_num == 1 and "Bayview Eco-Lodge" in transcript and os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
    elif section_num == 2 and "Maritime Heritage Museum" in transcript and os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
    elif section_num == 3 and "Smart Microgrids" in transcript and os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
    elif section_num == 4 and "Marine Bioluminescence" in transcript and os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
        
    # Dynamically synthesize multi-speaker neural audio with distinct realistic voices
    try:
        from ai_engine.audio_synthesizer import generate_multi_speaker_listening_audio
        combined_audio = generate_multi_speaker_listening_audio(transcript, section_num)
        if combined_audio and len(combined_audio) > 500:
            with open(cached_mp3, 'wb') as f:
                f.write(combined_audio)
            return FileResponse(cached_mp3, media_type="audio/mpeg")
    except Exception as e:
        print(f"Multi-speaker neural TTS synthesis failed for Section {section_num}:", e)
        
    if os.path.exists(static_file):
        return FileResponse(static_file, media_type="audio/mpeg")
    return Response(status_code=404)

@app.post("/api/v1/listening/switch-set")
def api_listening_switch_set(payload: dict = Body(...)):
    set_name = payload.get("set_name", "A").upper()
    from seed_authentic_cambridge_listening_multiset import seed_full_cambridge_listening_set, seed_random_listening_set
    if set_name in ["A", "B", "C", "D"]:
        res = seed_full_cambridge_listening_set(set_name)
    else:
        res = seed_random_listening_set()
    return JSONResponse(content={"status": "success", "set_name": res.get("set_id", set_name), "name": res.get("name")})

@app.post("/api/v1/listening/generate-practice")
def api_listening_generate_practice(payload: dict = Body(...)):
    provider = payload.get("provider", None)
    theme = payload.get("theme", None)
    from ai_engine.listening_question_generator import listening_question_generator
    res = listening_question_generator.generate_practice_set(preferred_provider=provider, topic_theme=theme)
    return JSONResponse(content={"status": "success", "set_name": res.get("set_id", "AI_CUSTOM"), "name": res.get("name")})

@app.get("/api/v1/listening/sets")
def api_listening_list_sets():
    return JSONResponse(content={
        "sets": [
            {"id": "A", "name": "Cambridge 19 - Test 1 (Eco-Lodge, Farley Estate Map, Microgrids, Bioluminescence)"},
            {"id": "B", "name": "Cambridge 18 - Test 2 (Greenwood Sports Club, Nature Trail Map, Wave Energy, Language Evolution)"},
            {"id": "C", "name": "Cambridge 17 - Test 3 (City Car Hire, Riverfront Arts Festival Map, Microplastics Ecology, Roman Concrete)"},
            {"id": "D", "name": "Cambridge 16 - Test 4 (International Homestay, Royal Botanic Gardens Map, AI Medical Ethics, Lighthouses)"}
        ]
    })

@app.get("/api/tts")
def proxy_tts(q: str, tl: str = "en-GB"):
    if not q or not q.strip():
        return Response(status_code=400)
    
    clean_q = q.strip()
    # Cache key based on language and text
    cache_dir = os.path.join(BASE_DIR, "static", "audio", "tts_cache")
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_hash = hashlib.md5(f"{tl}_{clean_q}".encode("utf-8")).hexdigest()
    cached_file = os.path.join(cache_dir, f"tts_{tl}_{cache_hash}.mp3")
    
    if os.path.exists(cached_file) and os.path.getsize(cached_file) > 500:
        return FileResponse(cached_file, media_type="audio/mpeg", headers={"Cache-Control": "public, max-age=86400"})
    
    # 1. Try gTTS with British / UK accent first
    try:
        from gtts import gTTS
        tld_code = "co.uk" if "gb" in tl.lower() or "uk" in tl.lower() else "com"
        lang_code = "en" if tl.startswith("en") else tl
        tts_obj = gTTS(text=clean_q, lang=lang_code, tld=tld_code, slow=False)
        tts_obj.save(cached_file)
        if os.path.exists(cached_file) and os.path.getsize(cached_file) > 500:
            return FileResponse(cached_file, media_type="audio/mpeg", headers={"Cache-Control": "public, max-age=86400"})
    except Exception as e:
        print("gTTS generation error, falling back to Google translate TTS:", e)
    
    # 2. Fallback to Google Translate TTS chunks
    try:
        words = clean_q.split(' ')
        chunks = []
        curr = []
        curr_len = 0
        for w in words:
            if curr_len + len(w) + 1 > 140:
                if curr: chunks.append(' '.join(curr))
                curr = [w]
                curr_len = len(w)
            else:
                curr.append(w)
                curr_len += len(w) + 1
        if curr:
            chunks.append(' '.join(curr))
        
        combined = b''
        for chunk in chunks:
            if not chunk.strip(): continue
            url = f"https://translate.googleapis.com/translate_tts?ie=UTF-8&q={requests.utils.quote(chunk)}&tl={tl}&client=tw-ob"
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=8)
            if r.status_code == 200:
                combined += r.content
        
        if combined and len(combined) > 500:
            with open(cached_file, "wb") as f:
                f.write(combined)
            return FileResponse(cached_file, media_type="audio/mpeg", headers={"Cache-Control": "public, max-age=86400"})
    except Exception as e2:
        print("Google TTS fallback error:", e2)
    
    return Response(status_code=500)

# --- AUTHENTICATION & USER HELPERS ---

def get_current_user(request: Request) -> Optional[dict]:
    uid_cookie = request.cookies.get("user_id")
    if not uid_cookie:
        return None
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, role FROM users WHERE id = ?", (int(uid_cookie),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception:
        return None

# --- AUTH GUARD MIDDLEWARE ---
@app.middleware("http")
async def auth_guard_middleware(request: Request, call_next):
    path = request.url.path
    
    # Public routes that anyone can access without login
    public_paths = {"/", "/auth/login", "/auth/register", "/auth/logout", "/favicon.ico"}
    public_prefixes = ("/static", "/audio", "/videos", "/js", "/css", "/docs", "/openapi.json", "/api/tts")
    
    if path in public_paths or path.startswith(public_prefixes):
        return await call_next(request)
    
    # Allow internal health checks
    if path.startswith("/api/ping"):
        return await call_next(request)
        
    # Check authentication cookie
    uid = request.cookies.get("user_id")
    if not uid:
        # If API call, return 401 Unauthorized
        if path.startswith("/api/"):
            return JSONResponse({"detail": "Authentication required. Please sign in."}, status_code=401)
        # If browser page visit, redirect to home page with login modal prompt
        return RedirectResponse(url=f"/?auth=login&redirect={path}", status_code=303)
        
    return await call_next(request)


# --- FRONTEND ROUTING ---

@app.get("/", response_class=HTMLResponse)
def page_home(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=303)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "user": None
    })

@app.post("/auth/login")
def auth_login(payload: dict = Body(...)):
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, role, password_hash FROM users WHERE LOWER(email) = ?", (email,))
    user_row = cursor.fetchone()

    if not user_row:
        # If user doesn't exist yet, auto-create for seamless onboarding or demo
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", 
                       ("Student", email, hashlib.sha256(password.encode()).hexdigest()))
        user_id = cursor.lastrowid
        cursor.execute("INSERT OR IGNORE INTO profiles (user_id, ielts_type, target_band, current_level) VALUES (?, 'Academic', 7.5, 6.0)", (user_id,))
        conn.commit()
    else:
        user_id = user_row["id"]
    conn.close()

    resp = JSONResponse({"success": True, "redirect": "/dashboard", "user_id": user_id})
    resp.set_cookie(key="user_id", value=str(user_id), max_age=86400*30, httponly=False, path="/")
    return resp

@app.post("/auth/register")
def auth_register(payload: dict = Body(...)):
    name = payload.get("name", "Student").strip()
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "").strip()
    target_band = float(payload.get("target_band") or 7.5)

    if not email or not password:
        return JSONResponse({"success": False, "message": "Email and password are required."}, status_code=400)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE LOWER(email) = ?", (email,))
    existing = cursor.fetchone()

    if existing:
        user_id = existing["id"]
        cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    else:
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)", 
                       (name, email, hashlib.sha256(password.encode()).hexdigest()))
        user_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO profiles (user_id, ielts_type, target_band, current_level)
        VALUES (?, 'Academic', ?, 6.0)
        ON CONFLICT(user_id) DO UPDATE SET target_band = excluded.target_band
    """, (user_id, target_band))
    conn.commit()
    conn.close()

    resp = JSONResponse({"success": True, "redirect": "/dashboard", "user_id": user_id})
    resp.set_cookie(key="user_id", value=str(user_id), max_age=86400*30, httponly=False, path="/")
    return resp

@app.get("/auth/logout")
@app.post("/auth/logout")
def auth_logout():
    resp = RedirectResponse(url="/", status_code=303)
    resp.delete_cookie(key="user_id", path="/")
    return resp


@app.get("/dashboard", response_class=HTMLResponse)
def page_dashboard(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM profiles WHERE user_id = 1")
    profile_row = cursor.fetchone()
    
    # Skill Mastery for user 1
    cursor.execute("""
        SELECT skill, 
               AVG(mastery_percentage) as avg_mastery, 
               SUM(total_attempted) as total_q,
               SUM(total_correct) as total_c,
               SUM(independent_correct) as ind_corr,
               SUM(assisted_correct) as ass_corr
        FROM skill_mastery WHERE user_id = 1 GROUP BY skill
    """)
    mastery_rows = cursor.fetchall()
    mastery_by_skill = {r["skill"]: dict(r) for r in mastery_rows}

    # Reading & Listening Bands (IELTS Scale, 0.0 if not attempted)
    def calc_skill_band(skill_name: str) -> float:
        if skill_name not in mastery_by_skill:
            return 0.0
        m = mastery_by_skill[skill_name]
        total_q = m.get("total_q", 0) or 0
        total_c = m.get("total_c", 0) or 0
        if total_q == 0:
            return 0.0
        acc = (total_c / total_q)
        raw = acc * 40
        if raw >= 39: return 9.0
        elif raw >= 37: return 8.5
        elif raw >= 35: return 8.0
        elif raw >= 32: return 7.5
        elif raw >= 30: return 7.0
        elif raw >= 27: return 6.5
        elif raw >= 23: return 6.0
        elif raw >= 19: return 5.5
        elif raw >= 15: return 5.0
        elif raw >= 13: return 4.5
        elif raw >= 10: return 4.0
        else: return round(max(1.0, raw / 10 * 3.5), 1)

    reading_band = calc_skill_band("Reading")
    listening_band = calc_skill_band("Listening")

    # Recent Writing Evaluations for user 1
    cursor.execute("""
        SELECT COUNT(we.id) 
        FROM writing_evaluations we
        JOIN writing_submissions ws ON we.submission_id = ws.id
        WHERE ws.user_id = 1
    """)
    wrt_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT we.grammatical_range, we.lexical_resource, we.overall_band 
        FROM writing_evaluations we
        JOIN writing_submissions ws ON we.submission_id = ws.id
        WHERE ws.user_id = 1
        ORDER BY we.id DESC LIMIT 1
    """)
    wrt_row = cursor.fetchone()
    writing_scores = dict(wrt_row) if wrt_row else {"grammatical_range": 0.0, "lexical_resource": 0.0, "overall_band": 0.0}
    writing_band = float(writing_scores.get("overall_band", 0.0))

    # Recent Speaking Evaluations for user 1
    cursor.execute("""
        SELECT COUNT(se.id) 
        FROM speaking_evaluations se
        JOIN speaking_sessions ss ON se.session_id = ss.id
        WHERE ss.user_id = 1
    """)
    spk_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT se.fluency_coherence, se.pronunciation, se.overall_band 
        FROM speaking_evaluations se
        JOIN speaking_sessions ss ON se.session_id = ss.id
        WHERE ss.user_id = 1
        ORDER BY se.id DESC LIMIT 1
    """)
    spk_row = cursor.fetchone()
    speaking_scores = dict(spk_row) if spk_row else {"fluency_coherence": 0.0, "pronunciation": 0.0, "overall_band": 0.0}
    speaking_band = float(speaking_scores.get("overall_band", 0.0))

    # Overall Estimated Band (Cambridge Average of Assessed Skills, 0.0 if none)
    assessed_bands = [b for b in [reading_band, listening_band, writing_band, speaking_band] if b > 0]
    if assessed_bands:
        raw_avg = sum(assessed_bands) / len(assessed_bands)
        rem = raw_avg - int(raw_avg)
        if rem < 0.25: overall_estimated_band = float(int(raw_avg))
        elif rem < 0.75: overall_estimated_band = float(int(raw_avg)) + 0.5
        else: overall_estimated_band = float(int(raw_avg) + 1)
    else:
        overall_estimated_band = 0.0

    # Total questions solved & accuracy across skills
    total_q_solved = sum(m.get("total_q", 0) for m in mastery_by_skill.values())
    total_c_solved = sum(m.get("total_c", 0) for m in mastery_by_skill.values())
    overall_accuracy = round((total_c_solved / total_q_solved * 100), 1) if total_q_solved > 0 else 0.0

    # Mistake Notebook & Priority Weakness
    cursor.execute("SELECT COUNT(*) FROM mistake_notebook WHERE user_id = 1")
    mistake_count = cursor.fetchone()[0]
    cursor.execute("SELECT question_type FROM mistake_notebook WHERE user_id = 1 ORDER BY id DESC LIMIT 1")
    weak_row = cursor.fetchone()
    priority_weakness = weak_row["question_type"] if weak_row else None

    # Real Daily Study Streak Calculation
    import datetime
    cursor.execute("""
        SELECT DISTINCT date(created_at) FROM (
            SELECT created_at FROM practice_results WHERE user_id = 1
            UNION
            SELECT created_at FROM writing_submissions WHERE user_id = 1
            UNION
            SELECT created_at FROM speaking_sessions WHERE user_id = 1
            UNION
            SELECT last_updated as created_at FROM skill_mastery WHERE user_id = 1
        ) ORDER BY date(created_at) DESC
    """)
    activity_dates = [r[0] for r in cursor.fetchall() if r[0]]
    today = datetime.date.today()
    study_streak_days = 0
    cur_day = today
    for d_str in activity_dates:
        try:
            d = datetime.date.fromisoformat(d_str)
            if d == cur_day or d == cur_day - datetime.timedelta(days=1):
                study_streak_days += 1
                cur_day = d
            else:
                break
        except Exception:
            pass

    # Daily Motivational Quotes (Stable per day)
    import random
    motivational_quotes = [
        {
            "quote": "Small daily disciplines repeated consistently lead to massive Band 8.0 breakthroughs.",
            "bengali": "প্রতিদিনের নিয়মিত ছোট ছোট অনুশীলনই আপনাকে Band 8.0 এর চূড়ায় নিয়ে যাবে।",
            "author": "IELTS Master Principle"
        },
        {
            "quote": "Don't practice until you get it right. Practice until you cannot get it wrong.",
            "bengali": "শুধু একবার সঠিক করার জন্য নয়, যাতে কখনো ভুল না হয় সেভাবে নিজেকে প্রস্তুত করুন।",
            "author": "Cambridge Examiner Advice"
        },
        {
            "quote": "Your target band is not an impossible dream; it's simply a set of habits executed daily.",
            "bengali": "আপনার টার্গেট স্কোর কোনো অবাস্তব স্বপ্ন নয়; এটি প্রতিদিনের সুশৃঙ্খল অভ্যাসের ফসল।",
            "author": "ARIA AI Mentor"
        },
        {
            "quote": "Accuracy comes from understanding traps, not rushing passages. Read smart, score high!",
            "bengali": "দ্রুত পড়ার চেয়ে প্রশ্নকর্তার ফাঁদগুলো বুঝে পড়াই বেশি গুরুত্বপূর্ণ। বুদ্ধিমত্তার সাথে পড়ুন!",
            "author": "Academic Reading Strategy"
        }
    ]
    day_of_year = datetime.date.today().timetuple().tm_yday
    today_quote = motivational_quotes[day_of_year % len(motivational_quotes)]

    # Comprehensive Examiner Daily Pro Tips Library
    from ai_engine.examiner_tips_data import get_all_examiner_tips
    examiner_tips = get_all_examiner_tips()

    # Total questions in system bank
    cursor.execute("SELECT COUNT(*) FROM questions")
    total_bank_questions = cursor.fetchone()[0]
    conn.close()

    profile = dict(profile_row) if profile_row else {"name": "IELTS Scholar", "target_band": 7.5, "current_level": 0.0, "daily_study_mins": 45}

    from scoring_engine.adaptive_learning import AdaptiveLearningEngine
    study_plan = AdaptiveLearningEngine.generate_daily_study_plan(1)

    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "profile": profile,
        "mastery_by_skill": mastery_by_skill,
        "reading_band": reading_band,
        "listening_band": listening_band,
        "writing_band": writing_band,
        "speaking_band": speaking_band,
        "writing_scores": writing_scores,
        "speaking_scores": speaking_scores,
        "overall_estimated_band": overall_estimated_band,
        "priority_weakness": priority_weakness,
        "total_q_solved": total_q_solved,
        "total_c_solved": total_c_solved,
        "overall_accuracy": overall_accuracy,
        "mistake_count": mistake_count,
        "wrt_count": wrt_count,
        "spk_count": spk_count,
        "study_streak_days": study_streak_days,
        "total_bank_questions": total_bank_questions,
        "today_quote": today_quote,
        "examiner_tips": examiner_tips,
        "study_plan": study_plan
    })

@app.get("/onboarding", response_class=HTMLResponse)
def page_onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@app.get("/practice", response_class=HTMLResponse)
def page_practice(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions ORDER BY id ASC")
    rows = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT question_type FROM questions ORDER BY question_type ASC")
    types_rows = cursor.fetchall()
    conn.close()
    
    questions = [dict(r) for r in rows]
    q_types = [r["question_type"] for r in types_rows]
    return templates.TemplateResponse("practice.html", {"request": request, "questions": questions, "q_types": q_types})

@app.get("/quick-practice")
def quick_practice():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, skill FROM questions ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return RedirectResponse(url="/practice")
    q_id = row["id"]
    skill = row["skill"]
    if skill == "Reading":
        return RedirectResponse(url=f"/reading-cbt?id={q_id}")
    elif skill == "Listening":
        return RedirectResponse(url=f"/listening-cbt?id={q_id}")
    elif skill == "Writing":
        return RedirectResponse(url=f"/writing-practice?id={q_id}")
    elif skill == "Speaking":
        return RedirectResponse(url=f"/speaking-practice?id={q_id}")
    return RedirectResponse(url="/practice")

@app.get("/reading-cbt", response_class=HTMLResponse)
def page_reading_cbt(
    request: Request, 
    id: Optional[int] = None, 
    title: Optional[str] = None,
    passage: Optional[int] = None,
    drill: Optional[str] = None,
    mode: Optional[str] = None,
    full_mock: Optional[str] = None
):
    is_exam_mode = (mode == "exam" or bool(full_mock))
    
    # ═══════════════════════════════════════════════════════════════
    # 🏛️ REAL EXAM MODE: AI-Generated Fresh Questions (100% New Every Time)
    # ═══════════════════════════════════════════════════════════════
    if is_exam_mode:
        try:
            from ai_engine.reading_question_generator import ReadingQuestionGenerator
            gen = ReadingQuestionGenerator()
            ai_result = gen.generate_practice_set(api_key="", api_key_pool=[])
            
            if ai_result and "passages" in ai_result and len(ai_result["passages"]) >= 1:
                # Convert AI generator format to template-compatible format
                ai_passages = []
                ai_all_qs = []
                q_global_index = 1
                
                for p_idx, p_data in enumerate(ai_result["passages"], start=1):
                    p_questions = p_data.get("questions", [])
                    groups_dict = {}
                    formatted_qs = []
                    
                    for q in p_questions:
                        q_dict = {
                            "id": q_global_index * 10000 + q.get("num", q_global_index),
                            "index": q_global_index,
                            "title": p_data.get("title", f"AI Passage {p_idx}"),
                            "skill": "Reading",
                            "test_type": "Academic",
                            "section_number": p_idx,
                            "question_type": q.get("type", "Multiple Choice"),
                            "passage_or_context": p_data.get("text", ""),
                            "question_text": q.get("text", ""),
                            "options_json": json.dumps(q.get("options", [])),
                            "answer_key": q.get("answer", ""),
                            "explanation": q.get("explanation", ""),
                            "difficulty": q.get("difficulty", "medium"),
                            "cambridge_book": "AI",
                            "test_number": 1,
                            "passage_or_section": f"Passage {p_idx}",
                            "difficulty_band": "7.0",
                            "group_id": q.get("group_id", f"P{p_idx}_G1"),
                            "group_instructions": q.get("group_instructions", "")
                        }
                        formatted_qs.append(q_dict)
                        ai_all_qs.append(q_dict)
                        
                        gid = q_dict["group_id"]
                        if gid not in groups_dict:
                            groups_dict[gid] = {
                                "group_id": gid,
                                "question_type": q_dict["question_type"],
                                "group_instructions": q_dict["group_instructions"],
                                "questions": [],
                                "first_index": q_global_index,
                                "last_index": q_global_index
                            }
                        groups_dict[gid]["questions"].append(q_dict)
                        groups_dict[gid]["last_index"] = q_global_index
                        q_global_index += 1
                    
                    ai_passages.append({
                        "passage_index": p_idx,
                        "title": p_data.get("title", f"AI Generated Passage {p_idx}"),
                        "passage_text": p_data.get("text", ""),
                        "questions": formatted_qs,
                        "question_groups": list(groups_dict.values())
                    })
                
                return templates.TemplateResponse("reading_cbt.html", {
                    "request": request,
                    "question": ai_all_qs[0] if ai_all_qs else None,
                    "questions": ai_all_qs,
                    "passages": ai_passages,
                    "active_passage": 1,
                    "is_solo_passage": False,
                    "drill": "",
                    "drill_title": "",
                    "solo_qtype": "",
                    "mode": mode or "",
                    "is_exam_mode": True,
                    "is_full_mock": bool(full_mock)
                })
        except Exception as e:
            print(f"[EXAM MODE] Reading AI generation failed, falling back to DB Set B: {e}")
            # Fallback: swap to alternate DB set
            try:
                from seed_authentic_cambridge_reading_full import seed_cambridge_reading_set_b
                seed_cambridge_reading_set_b()
            except Exception:
                pass
    
    # ═══════════════════════════════════════════════════════════════
    # 💡 PRACTICE MODE: Static DB Questions (normal flow)
    # ═══════════════════════════════════════════════════════════════
    conn = get_db()
    cursor = conn.cursor()
    
    if title:
        cursor.execute("SELECT * FROM questions WHERE skill = 'Reading' AND title = ? ORDER BY id ASC", (title,))
    else:
        cursor.execute("SELECT * FROM questions WHERE skill = 'Reading' ORDER BY section_number ASC, id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    # Group questions by passage
    passages_dict = {}
    for r in rows:
        q = dict(r)
        p_title = q.get("title", "Academic Reading Passage")
        p_text = q.get("passage_or_context", "")
        key = (p_title, p_text)
        if key not in passages_dict:
            passages_dict[key] = []
        passages_dict[key].append(q)

    drill_title = ""
    target_passage = passage or 1
    solo_qtype = None

    if drill:
        if drill.startswith("p1_"):
            target_passage = 1
            if drill == "p1_tf": drill_title, solo_qtype = "Passage 1: True / False / Not Given Drill", "True / False / Not Given"
            elif drill == "p1_note": drill_title, solo_qtype = "Passage 1: Note Completion Drill", "Note Completion"
            elif drill == "p1_table": drill_title, solo_qtype = "Passage 1: Table Completion Drill", "Table Completion"
            elif drill == "p1_sentence": drill_title, solo_qtype = "Passage 1: Sentence Completion Drill", "Sentence Completion"
            elif drill == "p1_short": drill_title, solo_qtype = "Passage 1: Short Answer Questions Drill", "Short Answer Questions"
            elif drill == "p1_flowchart": drill_title, solo_qtype = "Passage 1: Flow-chart Completion Drill", "Flow-chart Completion"
            elif drill == "p1_mcq": drill_title, solo_qtype = "Passage 1: Multiple Choice Drill", "Multiple Choice"
        elif drill.startswith("p2_"):
            target_passage = 2
            if drill == "p2_headings": drill_title, solo_qtype = "Passage 2: Matching Headings Drill", "Matching Headings"
            elif drill == "p2_info": drill_title, solo_qtype = "Passage 2: Matching Information Drill", "Matching Information"
            elif drill == "p2_features": drill_title, solo_qtype = "Passage 2: Matching Features Drill", "Matching Features"
            elif drill == "p2_summary": drill_title, solo_qtype = "Passage 2: Summary Completion Drill", "Summary Completion"
            elif drill == "p2_sentence": drill_title, solo_qtype = "Passage 2: Sentence Completion Drill", "Sentence Completion"
            elif drill == "p2_tf": drill_title, solo_qtype = "Passage 2: True / False / Not Given Drill", "True / False / Not Given"
            elif drill == "p2_mcq": drill_title, solo_qtype = "Passage 2: Multiple Choice Drill", "Multiple Choice"
        elif drill.startswith("p3_"):
            target_passage = 3
            if drill == "p3_yn": drill_title, solo_qtype = "Passage 3: Yes / No / Not Given Drill", "Yes / No / Not Given"
            elif drill == "p3_sentence_endings": drill_title, solo_qtype = "Passage 3: Matching Sentence Endings Drill", "Matching Sentence Endings"
            elif drill == "p3_features": drill_title, solo_qtype = "Passage 3: Matching Features Drill", "Matching Features"
            elif drill == "p3_summary_bank": drill_title, solo_qtype = "Passage 3: Summary Completion with Word Bank Drill", "Summary Completion"
            elif drill == "p3_mcq": drill_title, solo_qtype = "Passage 3: Multiple Choice Drill", "Multiple Choice"
            elif drill == "p3_table": drill_title, solo_qtype = "Passage 3: Table Completion Drill", "Table Completion"
            elif drill == "p3_short": drill_title, solo_qtype = "Passage 3: Short Answer Questions Drill", "Short Answer Questions"

    is_solo_passage = bool(drill or passage is not None)

    passages = []
    all_qs = []
    q_index = 1
    for p_idx, ((p_title, p_text), q_list) in enumerate(passages_dict.items(), start=1):
        groups_dict = {}
        p_filtered_qs = []
        for q in q_list:
            q["index"] = q_index
            q_index += 1
            gid = q.get("group_id") or f"P{p_idx}_AUTO"
            qtype_val = q.get("question_type", "Unknown")

            if is_solo_passage and p_idx == target_passage and solo_qtype:
                if solo_qtype.lower() in qtype_val.lower():
                    p_filtered_qs.append(q)
            else:
                p_filtered_qs.append(q)

            if gid not in groups_dict:
                groups_dict[gid] = {
                    "group_id": gid,
                    "question_type": qtype_val,
                    "group_instructions": q.get("group_instructions", ""),
                    "questions": [],
                    "first_index": q["index"],
                    "last_index": q["index"]
                }
            groups_dict[gid]["questions"].append(q)
            groups_dict[gid]["last_index"] = q["index"]

        question_groups = list(groups_dict.values())
        if is_solo_passage and p_idx == target_passage and solo_qtype:
            question_groups = [g for g in question_groups if solo_qtype.lower() in g["question_type"].lower()]

        passages.append({
            "passage_index": p_idx,
            "title": p_title,
            "passage_text": p_text,
            "questions": p_filtered_qs,
            "question_groups": question_groups
        })

    if is_solo_passage:
        active_p = passages[target_passage - 1] if len(passages) >= target_passage else (passages[0] if passages else {"questions": []})
        all_qs = active_p["questions"]
    else:
        for p in passages:
            all_qs.extend(p["questions"])

    target_q = all_qs[0] if all_qs else None
    if id is not None:
        for q in all_qs:
            if q["id"] == id:
                target_q = q
                break

    return templates.TemplateResponse("reading_cbt.html", {
        "request": request,
        "question": target_q,
        "questions": all_qs,
        "passages": passages,
        "active_passage": target_passage,
        "is_solo_passage": is_solo_passage,
        "drill": drill or "",
        "drill_title": drill_title,
        "solo_qtype": solo_qtype or "",
        "mode": mode or "",
        "is_exam_mode": is_exam_mode,
        "is_full_mock": bool(full_mock)
    })

@app.get("/listening-cbt", response_class=HTMLResponse)
def page_listening_cbt(
    request: Request, 
    id: Optional[int] = None, 
    section: Optional[int] = None,
    drill: Optional[str] = None,
    set: Optional[str] = None,
    book: Optional[str] = None,
    test: Optional[int] = None,
    random: Optional[int] = None,
    mode: Optional[str] = None,
    full_mock: Optional[str] = None
):
    from seed_authentic_cambridge_listening_multiset import seed_full_cambridge_listening_set, seed_random_listening_set, ALL_SETS

    is_exam_mode = (mode == "exam" or bool(full_mock))

    # ═══════════════════════════════════════════════════════════════
    # 🏛️ REAL EXAM MODE: AI-Generated Fresh Listening Set (100% New)
    # ═══════════════════════════════════════════════════════════════
    if is_exam_mode:
        try:
            from ai_engine.listening_question_generator import ListeningQuestionGenerator
            gen = ListeningQuestionGenerator()
            ai_result = gen.generate_practice_set()
            # generate_practice_set() saves to DB automatically, so we just continue
            # loading from DB below — but the data is now fresh AI-generated
            print("[EXAM MODE] Listening: Fresh AI-generated 4-section test loaded!")
        except Exception as e:
            print(f"[EXAM MODE] Listening AI generation failed, using random DB set: {e}")
            # Fallback: swap to a random alternate DB set
            import random as rng
            fallback_sets = list(ALL_SETS.keys())
            rng.shuffle(fallback_sets)
            seed_full_cambridge_listening_set(fallback_sets[0])
    else:
        # Handle requested set switching (Practice Mode only)
        if random or set == "random" or set == "ai_fresh" or set == "full_random":
            seed_random_listening_set()
        elif set and str(set).upper() in ALL_SETS:
            seed_full_cambridge_listening_set(str(set).upper())
        elif book:
            book_map = {"19": "A", "18": "B", "17": "C", "16": "D", "15": "E", "14": "F"}
            target_set = book_map.get(str(book), "A")
            seed_full_cambridge_listening_set(target_set)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE skill = 'Listening' ORDER BY section_number ASC, id ASC")
    rows = cursor.fetchall()
    conn.close()

    # Determine active book and test
    current_book = 19
    current_test = 1
    if rows:
        current_book = rows[0]["cambridge_book"] or 19
        current_test = rows[0]["test_number"] or 1

    # Group questions by section
    sections_raw = {1: [], 2: [], 3: [], 4: []}
    for r in rows:
        q = dict(r)
        sec_num = q.get("section_number") or 1
        if sec_num in sections_raw:
            sections_raw[sec_num].append(q)

    drill_title = ""
    target_section = section or 1
    solo_subpart = None

    if drill:
        if drill.startswith("lis_s1_"):
            target_section = 1
            if drill == "lis_s1_form": drill_title, solo_subpart = "Section 1: Form Completion Drill (নাম, ঠিকানা ও নম্বর)", "form"
            elif drill == "lis_s1_note": drill_title, solo_subpart = "Section 1: Note Completion Drill", "note"
            elif drill == "lis_s1_table": drill_title, solo_subpart = "Section 1: Table Completion Drill", "table"
            elif drill == "lis_s1_short": drill_title, solo_subpart = "Section 1: Short Answer Questions Drill", "short"
        elif drill.startswith("lis_s2_"):
            target_section = 2
            if drill == "lis_s2_map": drill_title, solo_subpart = "Section 2: Interactive Map Labelling Drill", "map"
            elif drill == "lis_s2_plan": drill_title, solo_subpart = "Section 2: Plan & Diagram Labelling Drill", "plan"
            elif drill == "lis_s2_mcq": drill_title, solo_subpart = "Section 2: Multiple Choice Single Drill", "mcq"
            elif drill == "lis_s2_matching": drill_title, solo_subpart = "Section 2: Matching Information Drill", "matching"
            elif drill == "lis_s2_flowchart": drill_title, solo_subpart = "Section 2: Flow-chart Completion Drill", "flowchart"
        elif drill.startswith("lis_s3_"):
            target_section = 3
            if drill == "lis_s3_mcq_single": drill_title, solo_subpart = "Section 3: Multiple Choice Single Drill", "mcq_single"
            elif drill == "lis_s3_mcq_multi": drill_title, solo_subpart = "Section 3: Multiple Choice Multi Drill", "mcq_multi"
            elif drill == "lis_s3_matching": drill_title, solo_subpart = "Section 3: Matching Opinions & Research Drill", "matching"
            elif drill == "lis_s3_flowchart": drill_title, solo_subpart = "Section 3: Flow-chart Completion Drill", "flowchart"
            elif drill == "lis_s3_sentence": drill_title, solo_subpart = "Section 3: Sentence Completion Drill", "sentence"
        elif drill.startswith("lis_s4_"):
            target_section = 4
            if drill == "lis_s4_lecture_note": drill_title, solo_subpart = "Section 4: Lecture Notes Completion Drill", "lecture_note"
            elif drill == "lis_s4_summary": drill_title, solo_subpart = "Section 4: Summary Completion Drill", "summary"
            elif drill == "lis_s4_table": drill_title, solo_subpart = "Section 4: Table Completion Drill", "table"
            elif drill == "lis_s4_flowchart": drill_title, solo_subpart = "Section 4: Flow-chart Completion Drill", "flowchart"
            elif drill == "lis_s4_sentence": drill_title, solo_subpart = "Section 4: Sentence Completion Drill", "sentence"
        elif drill == "section_1": target_section, drill_title = 1, "Section 1: Full Drill (Q1–10)"
        elif drill == "section_2": target_section, drill_title = 2, "Section 2: Full Drill (Q11–20)"
        elif drill == "section_3": target_section, drill_title = 3, "Section 3: Full Drill (Q21–30)"
        elif drill == "section_4": target_section, drill_title = 4, "Section 4: Full Drill (Q31–40)"

    is_solo_drill = bool(drill or section is not None)

    sections = []
    q_index = 1
    for sec_num in [1, 2, 3, 4]:
        q_list = sections_raw[sec_num]
        sec_title = q_list[0].get("title", f"Section {sec_num}") if q_list else f"Section {sec_num}"
        sec_context = q_list[0].get("passage_or_context", "") if q_list else ""
        sec_inst = q_list[0].get("group_instructions", "") if q_list else ""

        filtered_q_list = []
        for q in q_list:
            q["index"] = q_index
            q_index += 1
            filtered_q_list.append(q)

        sections.append({
            "section_number": sec_num,
            "title": sec_title,
            "transcript": sec_context,
            "instructions": sec_inst,
            "questions": filtered_q_list
        })

    all_qs = []
    if is_solo_drill:
        active_sec_data = sections[target_section - 1]
        if solo_subpart in ["map", "plan"]:
            all_qs = active_sec_data["questions"][5:10] if len(active_sec_data["questions"]) >= 10 else active_sec_data["questions"]
        elif solo_subpart == "mcq":
            all_qs = active_sec_data["questions"][:5]
        elif solo_subpart in ["mcq_single", "mcq_multi"]:
            all_qs = active_sec_data["questions"][:5]
        elif solo_subpart == "sentence" and target_section == 3:
            all_qs = active_sec_data["questions"][5:10] if len(active_sec_data["questions"]) >= 10 else active_sec_data["questions"]
        else:
            all_qs = active_sec_data["questions"]
    else:
        for s in sections:
            all_qs.extend(s["questions"])

    target_q = all_qs[0] if all_qs else None
    if id is not None:
        for q in all_qs:
            if q["id"] == id:
                target_q = q
                break

    sec2_title = sections[1]["title"] if len(sections) > 1 else ""
    try:
        from ai_engine.map_generator import generate_dynamic_cambridge_svg_map
        map_svg = generate_dynamic_cambridge_svg_map(theme_hint=sec2_title, book_number=current_book)
    except Exception:
        map_svg = ""

    return templates.TemplateResponse("listening_cbt.html", {
        "request": request,
        "question": target_q,
        "questions": all_qs,
        "sections": sections,
        "active_section": target_section,
        "is_solo_section": is_solo_drill,
        "is_solo_drill": is_solo_drill,
        "drill": drill or "",
        "drill_title": drill_title,
        "active_book": str(current_book),
        "active_test": current_test,
        "solo_subpart": solo_subpart or "",
        "section_2_map_svg": map_svg,
        "mode": mode or "",
        "is_exam_mode": is_exam_mode,
        "is_full_mock": bool(full_mock)
    })

@app.get("/writing-practice", response_class=HTMLResponse)
def page_writing_practice(
    request: Request, 
    id: Optional[int] = None, 
    t1_id: Optional[int] = None, 
    t2_id: Optional[int] = None,
    task_type: Optional[str] = None,
    task: Optional[int] = None,
    drill: Optional[str] = None,
    mode: Optional[str] = None,
    full_mock: Optional[str] = None
):
    is_exam_mode = (mode == "exam" or bool(full_mock))
    
    # ═══════════════════════════════════════════════════════════════
    # 🏛️ REAL EXAM MODE: AI-Generated Fresh Writing Prompts (100% New)
    # ═══════════════════════════════════════════════════════════════
    if is_exam_mode:
        try:
            from ai_engine.writing_question_generator import WritingQuestionGenerator
            import random as rng
            gen = WritingQuestionGenerator()
            
            # Random Task 1 visual type
            task1_types = [
                "Task 1 - Line Graph", "Task 1 - Bar Chart", "Task 1 - Pie Chart",
                "Task 1 - Table", "Task 1 - Process Diagram", "Task 1 - Map / Layout"
            ]
            # Random Task 2 essay type
            task2_types = [
                "Task 2 - Agree or Disagree", "Task 2 - Discuss Both Views",
                "Task 2 - Advantages vs Disadvantages", "Task 2 - Problem and Solution",
                "Task 2 - Two-Part Question"
            ]
            
            t1_type = rng.choice(task1_types)
            t2_type = rng.choice(task2_types)
            
            ai_task1 = gen.generate_custom_topic_prompt(t1_type)
            ai_task2 = gen.generate_custom_topic_prompt(t2_type)
            
            # Build template-compatible dicts
            exam_q1 = None
            exam_q2 = None
            
            if ai_task1 and ai_task1.get("success"):
                exam_q1 = {
                    "id": 90001,
                    "title": ai_task1.get("title", "AI Task 1"),
                    "question_type": ai_task1.get("question_type", t1_type),
                    "test_type": "Task 1",
                    "section_number": 1,
                    "skill": "Writing",
                    "question_text": ai_task1.get("full_prompt", ai_task1.get("prompt_intro", "")),
                    "passage_or_context": ai_task1.get("svg_chart", ai_task1.get("visual_data", "")),
                    "options_json": "[]",
                    "answer_key": "",
                    "explanation": "",
                    "cambridge_book": "AI",
                    "test_number": 1
                }
            
            if ai_task2 and ai_task2.get("success"):
                exam_q2 = {
                    "id": 90002,
                    "title": ai_task2.get("title", "AI Task 2"),
                    "question_type": ai_task2.get("question_type", t2_type),
                    "test_type": "Task 2",
                    "section_number": 2,
                    "skill": "Writing",
                    "question_text": ai_task2.get("full_prompt", ai_task2.get("prompt_intro", "")),
                    "passage_or_context": "",
                    "options_json": "[]",
                    "answer_key": "",
                    "explanation": "",
                    "cambridge_book": "AI",
                    "test_number": 1
                }
            
            if exam_q1 or exam_q2:
                print(f"[EXAM MODE] Writing: Fresh AI Task 1 ({t1_type}) + Task 2 ({t2_type}) generated!")
                return templates.TemplateResponse("writing_practice.html", {
                    "request": request,
                    "task1": exam_q1,
                    "task2": exam_q2,
                    "task1_list": [],
                    "task2_list": [],
                    "is_single_task": False,
                    "active_task_num": 1,
                    "default_timer_seconds": 3600,
                    "mode": mode or "",
                    "is_exam_mode": True,
                    "is_full_mock": bool(full_mock)
                })
        except Exception as e:
            print(f"[EXAM MODE] Writing AI generation failed, falling back to DB: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # 💡 PRACTICE MODE: Static DB Questions (normal flow)
    # ═══════════════════════════════════════════════════════════════
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, question_type, test_type, section_number, cambridge_book FROM questions WHERE skill = 'Writing' ORDER BY section_number ASC, id ASC")
    all_writing_questions = [dict(r) for r in cursor.fetchall()]
    
    task1_questions = [q for q in all_writing_questions if q.get("section_number") == 1 or "Task 1" in q.get("test_type", "")]
    task2_questions = [q for q in all_writing_questions if q.get("section_number") == 2 or "Task 2" in q.get("test_type", "")]
    
    current_q1 = None
    current_q2 = None
    
    is_single_task = False
    active_task_num = 1
    default_timer_seconds = 3600
    
    # Check if task_type / drill / task was passed
    if (task_type or drill) and not id:
        search_type = task_type or drill
        cursor.execute("SELECT * FROM questions WHERE skill = 'Writing' AND (question_type LIKE ? OR title LIKE ?) ORDER BY id DESC LIMIT 1", (f"%{search_type}%", f"%{search_type}%"))
        row = cursor.fetchone()
        if row:
            id = row['id']

    if task and not id:
        if task == 1 and task1_questions:
            id = task1_questions[0]["id"]
        elif task == 2 and task2_questions:
            id = task2_questions[0]["id"]

    if id is not None and not (t1_id and t2_id):
        # Single Task Mode (user selected a specific Task 1 or Task 2 prompt)
        cursor.execute("SELECT * FROM questions WHERE id = ?", (id,))
        row = cursor.fetchone()
        if not row:
            # Question not found (deleted or invalid) — redirect to default
            conn.close()
            return RedirectResponse(url="/writing-practice", status_code=302)
        is_single_task = True
        q_dict = dict(row)
        if q_dict.get("section_number") == 2 or "Task 2" in q_dict.get("test_type", "") or "Task 2" in q_dict.get("question_type", ""):
            current_q2 = q_dict
            active_task_num = 2
            default_timer_seconds = 2400  # 40 Mins
        else:
            current_q1 = q_dict
            active_task_num = 1
            default_timer_seconds = 1200  # 20 Mins
    else:
        # Full Test Set Mode (both Task 1 & Task 2)
        target_t1_id = t1_id
        if not target_t1_id and task1_questions:
            target_t1_id = task1_questions[0]["id"]
            
        if target_t1_id:
            cursor.execute("SELECT * FROM questions WHERE id = ?", (target_t1_id,))
            r1 = cursor.fetchone()
            if r1: current_q1 = dict(r1)
            
        target_t2_id = t2_id
        if not target_t2_id and task2_questions:
            target_t2_id = task2_questions[0]["id"]
            
        if target_t2_id:
            cursor.execute("SELECT * FROM questions WHERE id = ?", (target_t2_id,))
            r2 = cursor.fetchone()
            if r2: current_q2 = dict(r2)
            
        active_task_num = 1
        default_timer_seconds = 3600

    conn.close()
    return templates.TemplateResponse("writing_practice.html", {
        "request": request,
        "task1": current_q1,
        "task2": current_q2,
        "task1_list": task1_questions,
        "task2_list": task2_questions,
        "is_single_task": is_single_task,
        "active_task_num": active_task_num,
        "default_timer_seconds": default_timer_seconds,
        "mode": mode or "",
        "is_exam_mode": is_exam_mode,
        "is_full_mock": bool(full_mock)
    })

@app.get("/speaking-practice", response_class=HTMLResponse)
def page_speaking_practice(
    request: Request,
    id: Optional[int] = None,
    part: Optional[int] = None,
    book: Optional[int] = None,
    test: Optional[int] = None,
    theme: Optional[str] = None,
    timer: Optional[int] = None,
    topic_key: Optional[str] = None,
    mode: Optional[str] = None,
    full_mock: Optional[str] = None
):
    is_exam_mode = (mode == "exam" or bool(full_mock))
    
    # ═══════════════════════════════════════════════════════════════
    # 🏛️ REAL EXAM MODE: AI-Generated Fresh Speaking Set (100% New)
    # ═══════════════════════════════════════════════════════════════
    if is_exam_mode:
        try:
            from ai_engine.speaking_question_generator import SpeakingQuestionGenerator
            gen = SpeakingQuestionGenerator()
            ai_set = gen.generate_full_speaking_set()
            if ai_set and "part1" in ai_set:
                print(f"[EXAM MODE] Speaking: Fresh AI 3-part interview generated! Theme: {ai_set.get('theme', 'Random')}")
                return templates.TemplateResponse("speaking_practice.html", {
                    "request": request,
                    "test_set": ai_set,
                    "all_tests_list": [],
                    "active_book": "AI",
                    "active_test": 1,
                    "active_part": 0,
                    "is_solo_part": False,
                    "topic_key": "",
                    "custom_timer_minutes": 14,
                    "mode": mode or "",
                    "is_exam_mode": True,
                    "is_full_mock": bool(full_mock)
                })
        except Exception as e:
            print(f"[EXAM MODE] Speaking AI generation failed, falling back to DB: {e}")
    
    # If dynamic theme requested (Practice Mode), generate fresh AI set on the fly
    if theme:
        from ai_engine.speaking_question_generator import SpeakingQuestionGenerator
        gen = SpeakingQuestionGenerator()
        ai_set = gen.generate_full_speaking_set(custom_theme=theme)
        if ai_set and "part1" in ai_set:
            return templates.TemplateResponse("speaking_practice.html", {
                "request": request,
                "test_set": ai_set,
                "all_tests_list": [],
                "active_book": "AI",
                "active_test": 1,
                "active_part": part or (1 if part else 0),
                "is_solo_part": (part is not None and part in [1, 2, 3]),
                "custom_timer_minutes": timer if timer is not None else (5 if part in [1,2,3] else 14)
            })

    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Fetch all distinct test sets for selector
    cursor.execute("SELECT DISTINCT cambridge_book, test_number FROM questions WHERE skill = 'Speaking' ORDER BY cambridge_book DESC, test_number ASC")
    distinct_tests = cursor.fetchall()
    
    TEST_METADATA = {
        (19, 1): {"emoji": "🤖", "theme": "AI, Automation & Smart Transport", "p1_label": "Hometown ➔ Tech", "p2_label": "Tech Problem Solved", "p3_label": "AI & Future Jobs"},
        (18, 2): {"emoji": "🌱", "theme": "Climate Change, Green Cities & Policy", "p1_label": "Work/Studies ➔ Environment", "p2_label": "Environmental Project", "p3_label": "Climate & Sustainable Policy"},
        (18, 1): {"emoji": "🌧️", "theme": "Weather, Seasons & Urban Living", "p1_label": "Home ➔ Weather", "p2_label": "Weather-Delayed Journey", "p3_label": "Weather Disruption & Infrastructure"},
        (17, 1): {"emoji": "🍱", "theme": "Food, Cooking & Global Nutrition", "p1_label": "Hometown ➔ Food", "p2_label": "Traditional Culinary Meal", "p3_label": "Food Security & Culture"},
        (17, 3): {"emoji": "📸", "theme": "Photography, Visual Arts & Media", "p1_label": "Work/Studies ➔ Photography", "p2_label": "Cherished Photograph", "p3_label": "Visual Arts & AI Media"},
        (16, 2): {"emoji": "🧸", "theme": "Childhood, Parenting & Education", "p1_label": "Home ➔ Childhood", "p2_label": "Childhood Valuable Skill", "p3_label": "Child Psychology & Education"},
        (16, 3): {"emoji": "👟", "theme": "Shopping, Fast Fashion & Ethics", "p1_label": "Hometown ➔ Shopping", "p2_label": "Satisfying Purchase", "p3_label": "Consumerism & Fast Fashion"},
        (15, 1): {"emoji": "🐅", "theme": "Wildlife, Animals & Conservation", "p1_label": "Work/Studies ➔ Animals", "p2_label": "Wild Animal Encounter", "p3_label": "Biodiversity Loss & Conservation"}
    }

    all_tests_list = []
    for dt in distinct_tests:
        b, t = dt['cambridge_book'], dt['test_number']
        meta = TEST_METADATA.get((b, t), {"emoji": "🎯", "theme": f"Cambridge {b} Test {t}", "p1_label": "Part 1", "p2_label": "Part 2", "p3_label": "Part 3"})
        all_tests_list.append({
            "book": str(b),
            "test": t,
            "title": f"{meta['emoji']} {meta['theme']}",
            "theme": meta['theme'],
            "p1_label": meta['p1_label'],
            "p2_label": meta['p2_label'],
            "p3_label": meta['p3_label']
        })

    # 2. Identify target test set by book/test or id or random/default
    target_book = book
    target_test = test
    
    if id is not None:
        cursor.execute("SELECT cambridge_book, test_number FROM questions WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            target_book = row['cambridge_book']
            target_test = row['test_number']

    if not target_book or not target_test:
        if request.query_params.get("random") == "1" and all_tests_list:
            import random
            picked = random.choice(all_tests_list)
            target_book = picked["book"]
            target_test = picked["test"]
        elif all_tests_list:
            target_book = all_tests_list[0]["book"]
            target_test = all_tests_list[0]["test"]

    # 3. Fetch Part 1, Part 2, Part 3 for this set
    cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 1", (target_book, target_test))
    p1_row = cursor.fetchone()
    
    cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 2", (target_book, target_test))
    p2_row = cursor.fetchone()
    
    cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 3", (target_book, target_test))
    p3_row = cursor.fetchone()
    
    conn.close()

    # 4. Assemble JSON-serializable test_set
    import json
    p1_data = {}
    p1_topic = "Hometown & Routine"
    if p1_row:
        p1_ctx = json.loads(p1_row['passage_or_context']) if p1_row['passage_or_context'] and p1_row['passage_or_context'].startswith('{') else {}
        p1_topic = p1_ctx.get("topic", "Hometown & Routine")
        p1_data = {
            "title": p1_row['title'],
            "topic": p1_topic,
            "mandatory_topic": p1_ctx.get("mandatory_topic", "Hometown & Neighbourhood"),
            "secondary_topic": p1_ctx.get("secondary_topic", p1_topic),
            "questions": json.loads(p1_row['options_json']) if p1_row['options_json'] else ["Tell me about yourself."],
            "model_answers": json.loads(p1_row['answer_key']) if p1_row['answer_key'] else ["Sample answer"]
        }

    p2_data = {}
    if p2_row:
        p2_data = {
            "title": p2_row['title'],
            "topic": "Cue Card",
            "cue_card_prompt": p2_row['passage_or_context'] or "",
            "model_answer": p2_row['answer_key'] or ""
        }

    p3_data = {}
    if p3_row:
        p3_ctx = json.loads(p3_row['passage_or_context']) if p3_row['passage_or_context'] and p3_row['passage_or_context'].startswith('{') else {}
        p3_data = {
            "title": p3_row['title'],
            "topic": p3_ctx.get("topic", "General Discussion"),
            "questions": json.loads(p3_row['options_json']) if p3_row['options_json'] else ["Discuss your opinion."],
            "model_answers": json.loads(p3_row['answer_key']) if p3_row['answer_key'] else ["Sample answer"]
        }

    meta = TEST_METADATA.get((int(target_book) if str(target_book).isdigit() else 19, int(target_test) if str(target_test).isdigit() else 1), {})
    theme_title = meta.get("theme", p1_topic)

    test_set = {
        "theme": theme_title,
        "book": target_book,
        "test": target_test,
        "part1": p1_data,
        "part2": p2_data,
        "part3": p3_data
    }

    is_solo = (part is not None and part in [1, 2, 3])
    default_timer = (5 if part in [1, 3] else (4 if part == 2 else 14))

    return templates.TemplateResponse("speaking_practice.html", {
        "request": request,
        "test_set": test_set,
        "all_tests_list": all_tests_list,
        "active_book": str(target_book),
        "active_test": target_test,
        "active_part": part if part is not None else 0,
        "is_solo_part": is_solo,
        "topic_key": topic_key,
        "custom_timer_minutes": timer if timer is not None else default_timer,
        "mode": mode or "",
        "is_exam_mode": is_exam_mode,
        "is_full_mock": bool(full_mock)
    })

@app.get("/ai-teacher", response_class=HTMLResponse)
@app.get("/ai_teacher", response_class=HTMLResponse)
def page_ai_teacher(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = 1")
    profile_row = cursor.fetchone()
    cursor.execute("SELECT * FROM questions ORDER BY skill ASC, test_type ASC, id ASC")
    q_rows = cursor.fetchall()
    conn.close()

    profile = dict(profile_row) if profile_row else {}
    all_questions = [dict(r) for r in q_rows]
    questions_by_skill = {
        "Reading": [q for q in all_questions if q["skill"] == "Reading"],
        "Listening": [q for q in all_questions if q["skill"] == "Listening"],
        "Writing": [q for q in all_questions if q["skill"] == "Writing"],
        "Speaking": [q for q in all_questions if q["skill"] == "Speaking"]
    }
    return templates.TemplateResponse("ai_teacher.html", {"request": request, "profile": profile, "questions_by_skill": questions_by_skill, "all_questions": all_questions})

@app.post("/api/v1/ai/classroom-teacher-session")
def api_classroom_teacher_session(payload: dict = Body(...)):
    action = payload.get("action", "ask_question")
    selected_option = payload.get("selected_option", "")
    user_message = payload.get("user_message", "")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = 1")
    profile_row = cursor.fetchone()
    conn.close()

    profile = dict(profile_row) if profile_row else {"target_band": 7.5, "mother_language": "Bengali"}
    mother_lang = profile.get("mother_language", "Bengali")

    if action == "submit_answer":
        if "Heading II" in selected_option:
            reply = (
                f"Excellent choice! Heading II is the correct answer. You successfully identified the overall main idea "
                f"rather than falling for the Detail Trap in Heading I. Notice how Paragraph A focuses on climate impact across predators.\n\n"
                f"({mother_lang} explanation: সাবাস! তুমি সঠিক উত্তর দিয়েছ। শুধু একটা ছোট detail দেখে ভুল না করে তুমি পুরো প্যারাগ্রাফের মূল বক্তব্য ধরেছ।)"
            )
            wb_notes = (
                "📌 TODAY'S LESSON: IELTS Reading — Matching Headings Mastery\n"
                "🎯 TARGET: Band 7.5 Precision\n\n"
                "[ CLASS SUCCESS ✅ ]\n"
                "- Paragraph A = Heading II (Environmental Impact on Arctic Predators)\n"
                "- Well done! Main idea identified accurately."
            )
        else:
            reply = (
                f"Let's evaluate your choice: You selected '{selected_option}'. Notice that while seals are mentioned in sentence 3, "
                f"the main focus of the entire paragraph is environmental impact on polar bear predators.\n\n"
                f"Why did that heading seem correct to you? ({mother_lang} explanation: এখানে সিল মাছের কথা বলা থাকলেও পুরো প্যারাগ্রাফের মূল বিষয় হল পরিবেশের প্রভাব।)"
            )
            wb_notes = (
                "📌 TODAY'S LESSON: IELTS Reading — Matching Headings Mastery\n"
                "🎯 TARGET: Band 7.5 Precision\n\n"
                "[ EXAMINER TRAP ANALYSIS ⚠️ ]\n"
                "- Detail Trap Identified in Option 1.\n"
                "- Strategy Rule: Avoid selecting headings based on a single sentence."
            )
        return JSONResponse(content={"reply": reply, "whiteboard_notes": wb_notes})

    # General Question in Classroom Session
    context = {"target_band": profile.get("target_band", 7.5), "mother_language": mother_lang, "teacher_language_pref": "English + Mother Language"}
    from ai_engine.ai_router import ai_router
    res = ai_router.teacher_chat(user_message, [], context)
    return JSONResponse(content={"reply": res.get("reply", "Let's focus on our classroom strategy.")})

@app.get("/mock-exam", response_class=HTMLResponse)
def page_mock_exam(request: Request):
    return templates.TemplateResponse("mock_exam.html", {"request": request})

@app.get("/mock-reading-cbt", response_class=HTMLResponse)
@app.get("/mock/reading-cbt", response_class=HTMLResponse)
def page_mock_reading_cbt(request: Request, title: Optional[str] = None):
    conn = get_db()
    cursor = conn.cursor()
    # Fetch all reading questions (simulating a full 40 question test, currently we have 12)
    # If title is provided, filter by title (used for AI generated passages)
    if title:
        cursor.execute("SELECT * FROM questions WHERE skill = 'Reading' AND title = ? ORDER BY id ASC", (title,))
    else:
        cursor.execute("SELECT * FROM questions WHERE skill = 'Reading' ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    # Group by passage
    passages_dict = {}
    for r in rows:
        q = dict(r)
        p_text = q.get("passage_or_context", "")
        if p_text not in passages_dict:
            passages_dict[p_text] = []
        passages_dict[p_text].append(q)
    
    passages = []
    q_index = 1
    for p_idx, (p_text, q_list) in enumerate(passages_dict.items(), start=1):
        for q in q_list:
            q["index"] = q_index
            q_index += 1
        passages.append({
            "passage_index": p_idx,
            "passage_text": p_text,
            "questions": q_list
        })
        
    return templates.TemplateResponse("mock_reading_cbt.html", {"request": request, "passages": passages})

@app.get("/mistake-notebook", response_class=HTMLResponse)
def page_mistake_notebook(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mistake_notebook WHERE user_id = 1 ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    mistakes = [dict(r) for r in rows]
    return templates.TemplateResponse("mistake_notebook.html", {"request": request, "mistakes": mistakes})

@app.get("/analytics", response_class=HTMLResponse)
def page_analytics(request: Request):
    from ai_engine.analytics_service import get_full_user_analytics
    analytics = get_full_user_analytics(user_id=1)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT skill, AVG(mastery_percentage) as avg_mastery, SUM(total_attempted) as total_q, SUM(total_correct) as total_c 
        FROM skill_mastery 
        WHERE user_id = ? 
        GROUP BY skill
    """, (1,))
    mastery_rows = cursor.fetchall()
    
    cursor.execute("SELECT * FROM profiles WHERE user_id = 1")
    p_row = cursor.fetchone()
    profile = dict(p_row) if p_row else {"target_band": 7.5, "current_level": 6.0}
    conn.close()

    mastery_by_skill = {r["skill"]: dict(r) for r in mastery_rows}
    
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "profile": profile,
        "analytics": analytics,
        "mastery_by_skill": mastery_by_skill
    })

@app.post("/api/v1/analytics/seed-benchmark")
def api_analytics_seed_benchmark():
    from ai_engine.analytics_service import seed_benchmark_data, get_full_user_analytics
    seed_benchmark_data(user_id=1)
    return JSONResponse(content={"status": "success", "analytics": get_full_user_analytics(user_id=1)})

@app.post("/api/v1/analytics/reset-data")
def api_analytics_reset_data():
    from ai_engine.analytics_service import reset_analytics_data, get_full_user_analytics
    reset_analytics_data(user_id=1)
    return JSONResponse(content={"status": "success", "analytics": get_full_user_analytics(user_id=1)})

@app.get("/diagnostic", response_class=HTMLResponse)
def page_diagnostic(request: Request):
    return templates.TemplateResponse("diagnostic.html", {"request": request})

@app.get("/grammar", response_class=HTMLResponse)
def page_grammar(request: Request):
    from ai_engine.grammar_data import get_all_grammar_topics
    return templates.TemplateResponse("grammar.html", {
        "request": request,
        "grammar_catalog": get_all_grammar_topics()
    })

@app.get("/vocabulary", response_class=HTMLResponse)
def page_vocabulary(request: Request):
    from ai_engine.vocabulary_data import get_all_vocabulary_topics
    from ai_engine.vocabulary_evaluator import get_user_vocab_srs_stats
    srs_stats = get_user_vocab_srs_stats(user_id=1)
    return templates.TemplateResponse("vocabulary.html", {
        "request": request,
        "vocab_catalog": get_all_vocabulary_topics(),
        "srs_stats": srs_stats
    })

@app.get("/grammar-vocab", response_class=HTMLResponse)
def page_grammar_vocab_redirect(request: Request):
    from starlette.responses import RedirectResponse
    return RedirectResponse(url="/grammar")

@app.get("/admin", response_class=HTMLResponse)
def page_admin(request: Request):
    conn = get_db()
    cursor = conn.cursor()
    
    provider_config = [
        {"id": "gemini", "name": "Google Gemini"},
        {"id": "openai", "name": "OpenAI (ChatGPT)"},
        {"id": "claude", "name": "Anthropic (Claude)"},
        {"id": "deepseek", "name": "DeepSeek"},
        {"id": "grok", "name": "Grok (xAI)"},
        {"id": "ollama", "name": "Local LLM (Ollama)"}
    ]
    
    providers = []
    for pc in provider_config:
        cursor.execute("SELECT id, api_key_masked, status, error_count, last_tested_at, COALESCE(label, '') as label FROM ai_credentials WHERE provider_id = ? ORDER BY id ASC", (pc["id"],))
        api_keys = [dict(r) for r in cursor.fetchall()]
        providers.append({"id": pc["id"], "name": pc["name"], "api_keys": api_keys})

    
    conn.close()
    return templates.TemplateResponse("admin.html", {"request": request, "providers": providers})

@app.post("/api/v1/admin/add-key")
def api_add_key(payload: dict = Body(...)):
    provider_id = payload.get("provider_id", "")
    api_key = payload.get("api_key", "").strip()
    label = payload.get("label", "").strip()
    if not provider_id or not api_key:
        raise HTTPException(status_code=400, detail="Provider ID and API key are required")
    masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ai_credentials (provider_id, api_key_masked, api_key, status, label) VALUES (?, ?, ?, 'Active', ?)", (provider_id, masked, api_key, label))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return JSONResponse(content={"status": "success", "id": new_id, "masked": masked, "label": label})

@app.post("/api/v1/admin/update-key-label/{key_id}")
def api_update_key_label(key_id: int, payload: dict = Body(...)):
    label = payload.get("label", "").strip()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE ai_credentials SET label = ? WHERE id = ?", (label, key_id))
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success", "id": key_id, "label": label})

@app.delete("/api/v1/admin/delete-key/{key_id}")
def api_delete_key(key_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ai_credentials WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success"})

@app.post("/api/v1/admin/toggle-key/{key_id}")
def api_toggle_key(key_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM ai_credentials WHERE id = ?", (key_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Key not found")
    new_status = "Disabled" if row["status"] == "Active" else "Active"
    cursor.execute("UPDATE ai_credentials SET status = ? WHERE id = ?", (new_status, key_id))
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success", "new_status": new_status})

@app.post("/api/v1/admin/test-key/{key_id}")
def api_test_key(key_id: int):
    import time as _time
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT provider_id, api_key FROM ai_credentials WHERE id = ?", (key_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Key not found")
    provider_id = row["provider_id"]
    api_key = row["api_key"].strip()
    start_time = _time.time()
    test_ok = False
    error_msg = ""
    status_code = 0
    try:
        if provider_id == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            resp = requests.post(url, json={"contents": [{"parts": [{"text": "Say hi"}]}]}, timeout=10)
            status_code = resp.status_code
            if status_code != 200:
                try: error_msg = resp.json().get("error", {}).get("message", f"HTTP {status_code}")
                except: error_msg = f"HTTP {status_code}"
        elif provider_id == "openai":
            resp = requests.post("https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5}, timeout=10)
            status_code = resp.status_code
            if status_code != 200:
                try: error_msg = resp.json().get("error", {}).get("message", f"HTTP {status_code}")
                except: error_msg = f"HTTP {status_code}"
        elif provider_id == "claude":
            resp = requests.post("https://api.anthropic.com/v1/messages",
                headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"},
                json={"model": "claude-3-haiku-20240307", "max_tokens": 5, "messages": [{"role": "user", "content": "Hi"}]}, timeout=10)
            status_code = resp.status_code
            if status_code != 200:
                try: error_msg = resp.json().get("error", {}).get("message", f"HTTP {status_code}")
                except: error_msg = f"HTTP {status_code}"
        elif provider_id == "deepseek":
            resp = requests.post("https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5}, timeout=10)
            status_code = resp.status_code
            if status_code != 200:
                try: error_msg = resp.json().get("error", {}).get("message", f"HTTP {status_code}: Invalid DeepSeek Key")
                except: error_msg = f"HTTP {status_code}"
        elif provider_id == "grok":
            for m in ["grok-2-1212", "grok-beta", "grok-3-mini"]:
                resp = requests.post("https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": m, "messages": [{"role": "user", "content": "Hi"}], "max_tokens": 5}, timeout=10)
                status_code = resp.status_code
                if status_code == 200: break
            if status_code != 200:
                try: error_msg = resp.json().get("error", {}).get("message", f"HTTP {status_code}")
                except: error_msg = f"HTTP {status_code}"
        elif provider_id == "ollama":
            url = api_key if api_key.startswith("http") else "http://localhost:11434"
            resp = requests.get(f"{url}/api/tags", timeout=5)
            status_code = resp.status_code
            if status_code != 200:
                error_msg = f"Ollama not running at {url}"
        else:
            error_msg = "Unknown provider"
    except Exception as e:
        error_msg = str(e)[:100]

    if status_code == 200:
        test_ok = True
        new_status = "Active"
        error_msg = ""
        error_cnt = 0
    elif status_code == 429:
        test_ok = True
        new_status = "Active"
        error_msg = "Quota / Rate Limit Exceeded (HTTP 429)"
        error_cnt = 0
    else:
        test_ok = False
        new_status = "Error"
        if not error_msg:
            error_msg = f"HTTP {status_code}"
        error_cnt = 1

    latency = int((_time.time() - start_time) * 1000)
    cursor.execute("UPDATE ai_credentials SET status = ?, latency_ms = ?, error_count = ? WHERE id = ?", (new_status, latency, error_cnt, key_id))
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success", "test_ok": test_ok, "latency_ms": latency, "error": error_msg, "new_status": new_status})

@app.post("/api/v1/diagnostic/evaluate")
def api_evaluate_diagnostic(payload: dict = Body(...)):
    r_ans = payload.get("r_ans", "")
    l_ans = payload.get("l_ans", "")
    w_ans = payload.get("w_ans", "").strip()
    
    r_correct = ObjectiveScoringEngine.is_answer_correct(r_ans, "True")
    l_correct = ObjectiveScoringEngine.is_answer_correct(l_ans, "950")

    r_band = 7.0 if r_correct else 4.5
    l_band = 7.5 if l_correct else 4.5

    # Dynamically assess writing sample
    w_words = len(w_ans.split()) if w_ans else 0
    if w_words == 0:
        w_band = 0.0
    elif w_words < 5:
        w_band = 2.0
    else:
        # Check academic keywords & sentence complexity
        w_lower = w_ans.lower()
        has_academic_words = any(w in w_lower for w in ["opinion", "artificial", "intelligence", "automate", "repetitive", "consequently", "furthermore", "significant", "crucial", "essential", "technology", "employment", "create", "impact"])
        has_complex_structure = any(w in w_lower for w in ["because", "although", "while", "which", "that", "in order to", "whereas", "if", "unless", "however"])
        
        score = 5.0
        if w_words >= 12: score += 0.5
        if has_academic_words: score += 0.5
        if has_complex_structure: score += 0.5
        w_band = min(8.0, max(2.5, score))

    s_band = w_band  # Align speaking diagnostic baseline with productive skill performance

    from ai_engine.ai_router import calculate_ielts_overall_band
    overall = calculate_ielts_overall_band([r_band, l_band, w_band, s_band])

    # Update profile current_level
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE profiles SET current_level = ? WHERE user_id = 1", (overall,))
    conn.commit()
    conn.close()

    return {
        "r_band": r_band,
        "l_band": l_band,
        "w_band": w_band,
        "s_band": s_band,
        "overall_band": overall
    }

@app.post("/api/v1/ai/teacher-tutor-step")
def api_teacher_tutor_step(payload: dict = Body(...)):
    user_message = payload.get("user_message", "")
    mode = payload.get("mode", "Teach")
    question_context = payload.get("question_context")
    student_reasoning = payload.get("student_reasoning")
    selected_option = payload.get("selected_option")
    teacher_language_pref = payload.get("teacher_language_pref")
    user_id = payload.get("user_id", 1)

    from ai_engine.ai_teacher_tutor import AITeacherTutorEngine
    result = AITeacherTutorEngine.process_tutor_step(
        user_message=user_message,
        mode=mode,
        question_context=question_context,
        student_reasoning=student_reasoning,
        selected_option=selected_option,
        user_id=user_id,
        teacher_language_pref=teacher_language_pref
    )
    return JSONResponse(content=result)

@app.get('/api/v1/ai/taxonomy-tree')
def api_taxonomy_tree():
    from ai_engine.ai_course_master import AICourseMasterEngine
    return JSONResponse(content=AICourseMasterEngine.get_taxonomy_tree())

@app.post('/api/v1/ai/human-teacher-lesson')
def api_human_teacher_lesson(payload: dict = Body(...)):
    topic_key = payload.get('topic_key', 'True / False / Not Given')
    sub_tag = payload.get('sub_tag')
    user_answer = payload.get('user_answer')
    teacher_language_pref = payload.get('teacher_language_pref', 'English + Mother Language')
    user_id = payload.get('user_id', 1)

    from ai_engine.ai_course_master import AICourseMasterEngine
    result = AICourseMasterEngine.process_teacher_lesson(
        topic_key=topic_key,
        sub_tag=sub_tag,
        user_answer=user_answer,
        lang_pref=teacher_language_pref,
        user_id=user_id
    )
    return JSONResponse(content=result)

# --- REST API ENDPOINTS ---

@app.post("/api/v1/user/onboarding")
def api_onboarding(
    name: str = Form(...),
    ielts_type: str = Form(...),
    target_band: float = Form(...),
    current_level: float = Form(...),
    daily_study_mins: int = Form(...),
    mother_language: str = Form(...),
    teacher_language_pref: str = Form(...)
):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = 1", (name,))
    cursor.execute("""
        UPDATE profiles SET 
        ielts_type = ?, target_band = ?, current_level = ?, daily_study_mins = ?,
        mother_language = ?, teacher_language_pref = ?, onboarding_completed = 1
        WHERE user_id = 1
    """, (ielts_type, target_band, current_level, daily_study_mins, mother_language, teacher_language_pref))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/api/v1/practice/submit-objective")
def api_submit_objective(payload: dict = Body(...)):
    q_id = payload.get("question_id")
    user_ans = payload.get("user_answer", "")
    time_taken = payload.get("time_taken_seconds", 30)

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Question not found")

    q = dict(row)
    test_type = q.get("test_type", q.get("ielts_type", "Academic"))
    is_correct = ObjectiveScoringEngine.is_answer_correct(user_ans, q["answer_key"])
    band_score = ObjectiveScoringEngine.calculate_raw_to_band(40 if is_correct else 20, 40, q["skill"], test_type)

    # Update Mastery & Mistake Notebook
    if is_correct:
        AdaptiveLearningEngine.record_correct_answer(1, q["skill"], q["question_type"])


@app.post("/api/v1/practice/evaluate-passage")
def api_evaluate_passage(payload: dict = Body(...)):
    answers = payload.get("answers", {}) # dict of question_id: user_answer
    
    conn = get_db()
    cursor = conn.cursor()
    
    results = {}
    correct_count = 0
    total_q = len(answers)
    
    for q_id_str, user_ans in answers.items():
        try:
            q_id = int(q_id_str)
        except ValueError:
            continue
            
        cursor.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
        row = cursor.fetchone()
        if not row: continue
        q = dict(row)
        
        is_correct = ObjectiveScoringEngine.is_answer_correct(user_ans, q["answer_key"])
        if is_correct:
            correct_count += 1
            AdaptiveLearningEngine.record_correct_answer(1, q["skill"], q["question_type"])
        else:
            AdaptiveLearningEngine.record_mistake(1, q["skill"], q["question_type"], q["title"], user_ans, q["answer_key"], q["explanation"])
            
        # Optional: We could call a real GenAI prompt here to explain WHY the user's specific answer is wrong.
        # For speed & reliability in this version, we use the rich DB explanation.
        results[q_id] = {
            "is_correct": is_correct,
            "user_answer": user_ans,
            "correct_answer": q["answer_key"],
            "explanation": q["explanation"]
        }
        
    conn.close()
    band_score = ObjectiveScoringEngine.calculate_raw_to_band(correct_count, total_q, "Reading", "Academic")
    
    return {
        "results": results,
        "band_score": band_score,
        "total_correct": correct_count,
        "total_questions": total_q
    }


@app.post("/api/v1/mock/submit-reading")
def api_mock_submit_reading(payload: dict = Body(...)):
    answers = payload.get("answers", {}) # dict of question_id: user_answer
    user_id = payload.get("user_id", 1)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, question_type, section_number, passage_or_section, answer_key, explanation FROM questions WHERE skill = 'Reading'")
    rows = cursor.fetchall()
    
    total_questions = len(rows) if rows else 40
    correct_count = 0
    detailed_results = []
    
    passage_scores = {"P1": {"correct": 0, "total": 0}, "P2": {"correct": 0, "total": 0}, "P3": {"correct": 0, "total": 0}}
    type_scores = {}

    for idx, row in enumerate(rows):
        q_id = row["id"]
        q_type = row["question_type"] or "General"
        p_sec = row["section_number"] or row["passage_or_section"] or 1
        ans_key = row["answer_key"]
        exp = row["explanation"]
        
        user_ans = answers.get(str(q_id), answers.get(q_id, answers.get(str(idx + 1), answers.get(idx + 1, ""))))
        is_corr = ObjectiveScoringEngine.is_answer_correct(str(user_ans), ans_key)
        
        if is_corr:
            correct_count += 1
            
        p_key = f"P{p_sec}" if f"P{p_sec}" in passage_scores else "P1"
        passage_scores[p_key]["total"] += 1
        if is_corr:
            passage_scores[p_key]["correct"] += 1
            
        if q_type not in type_scores:
            type_scores[q_type] = {"correct": 0, "total": 0}
        type_scores[q_type]["total"] += 1
        if is_corr:
            type_scores[q_type]["correct"] += 1
            
        detailed_results.append({
            "question_id": q_id,
            "passage_index": p_sec,
            "question_type": q_type,
            "user_answer": user_ans,
            "answer_key": ans_key,
            "explanation": exp,
            "is_correct": is_corr
        })

    # Calculate Official Cambridge Band Score based on Academic Reading
    band_score = ObjectiveScoringEngine.calculate_raw_to_band(correct_count, total_questions, "Reading", "Academic")
    desc_info = ObjectiveScoringEngine.get_band_descriptor_info(band_score)

    # Record into practice_results, skill_mastery, and mistake_notebook
    try:
        for r_item in detailed_results:
            cursor.execute("""
                INSERT INTO practice_results (user_id, skill, question_id, user_answer, is_correct, time_taken_seconds)
                VALUES (?, 'Reading', ?, ?, ?, ?)
            """, (user_id, r_item["question_id"], str(r_item["user_answer"]), 1 if r_item["is_correct"] else 0, 45))
            
            cursor.execute("""
                INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
                VALUES (?, 'Reading', ?, 1, ?, ?, 0, ?)
                ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
                    total_attempted = total_attempted + 1,
                    total_correct = total_correct + excluded.total_correct,
                    independent_correct = independent_correct + excluded.independent_correct,
                    mastery_percentage = ROUND((total_correct + excluded.total_correct) * 100.0 / (total_attempted + 1), 1),
                    last_updated = CURRENT_TIMESTAMP
            """, (user_id, r_item["question_type"], 1 if r_item["is_correct"] else 0, 1 if r_item["is_correct"] else 0, 100.0 if r_item["is_correct"] else 0.0))

            if not r_item["is_correct"] and r_item["user_answer"]:
                cursor.execute("""
                    INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
                    VALUES (?, 'Reading', ?, ?, ?, ?, ?, 'Needs Practice')
                """, (user_id, r_item["question_type"], f"Reading Q#{r_item['question_id']}", str(r_item["user_answer"]), str(r_item["answer_key"]), str(r_item["explanation"] or "")))
    except Exception as e_rec:
        print("Notice: reading practice_results record error:", e_rec)

    # Update profile reading level
    # Record into practice_results, skill_mastery, and mistake_notebook
    try:
        for l_item in detailed_results:
            cursor.execute("""
                INSERT INTO practice_results (user_id, skill, question_id, user_answer, is_correct, time_taken_seconds)
                VALUES (?, 'Listening', ?, ?, ?, ?)
            """, (user_id, l_item["question_id"], str(l_item["user_answer"]), 1 if l_item["is_correct"] else 0, 35))
            
            cursor.execute("""
                INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
                VALUES (?, 'Listening', ?, 1, ?, ?, 0, ?)
                ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
                    total_attempted = total_attempted + 1,
                    total_correct = total_correct + excluded.total_correct,
                    independent_correct = independent_correct + excluded.independent_correct,
                    mastery_percentage = ROUND((total_correct + excluded.total_correct) * 100.0 / (total_attempted + 1), 1),
                    last_updated = CURRENT_TIMESTAMP
            """, (user_id, l_item["question_type"], 1 if l_item["is_correct"] else 0, 1 if l_item["is_correct"] else 0, 100.0 if l_item["is_correct"] else 0.0))

            if not l_item["is_correct"] and l_item["user_answer"]:
                cursor.execute("""
                    INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
                    VALUES (?, 'Listening', ?, ?, ?, ?, ?, 'Needs Practice')
                """, (user_id, l_item["question_type"], f"Listening Q#{l_item['question_id']}", str(l_item["user_answer"]), str(l_item["answer_key"]), str(l_item["explanation"] or "")))
    except Exception as e_rec:
        print("Notice: listening practice_results record error:", e_rec)

    try:
        cursor.execute("UPDATE profiles SET current_level = ? WHERE user_id = ?", (band_score, user_id))
        conn.commit()
    except Exception:
        pass
    conn.close()
    
    return {
        "band_score": band_score,
        "descriptor": desc_info["descriptor"],
        "cefr": desc_info["cefr"],
        "cefr_label": f"Band {band_score:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})",
        "total_correct": correct_count,
        "total_questions": total_questions,
        "passage_scores": passage_scores,
        "type_scores": type_scores,
        "detailed_results": detailed_results
    }

@app.post("/api/v1/mock/submit-listening")
def api_mock_submit_listening(payload: dict = Body(...)):
    answers = payload.get("answers", {})  # dict of question_id / question_index: user_answer
    user_id = payload.get("user_id", 1)
    solo_section = payload.get("section_number", None)
    
    conn = get_db()
    cursor = conn.cursor()
    
    if solo_section and int(solo_section) in [1, 2, 3, 4]:
        cursor.execute("SELECT id, question_type, section_number, passage_or_section, answer_key, explanation FROM questions WHERE skill = 'Listening' AND section_number = ? ORDER BY id ASC", (int(solo_section),))
    else:
        cursor.execute("SELECT id, question_type, section_number, passage_or_section, answer_key, explanation FROM questions WHERE skill = 'Listening' ORDER BY section_number ASC, id ASC")
    
    rows = cursor.fetchall()
    
    total_questions = len(rows) if rows else 40
    correct_count = 0
    detailed_results = []
    
    section_scores = {
        "S1": {"correct": 0, "total": 0},
        "S2": {"correct": 0, "total": 0},
        "S3": {"correct": 0, "total": 0},
        "S4": {"correct": 0, "total": 0}
    }
    type_scores = {}

    for idx, row in enumerate(rows):
        q_id = row["id"]
        q_type = row["question_type"] or "Form Completion"
        s_sec = row["section_number"] or row["passage_or_section"] or 1
        ans_key = row["answer_key"]
        exp = row["explanation"]
        
        user_ans = answers.get(str(q_id), answers.get(q_id, answers.get(str(idx + 1), answers.get(idx + 1, ""))))
        is_corr = ObjectiveScoringEngine.is_answer_correct(str(user_ans), ans_key)
        
        if is_corr:
            correct_count += 1
            
        s_key = f"S{s_sec}" if f"S{s_sec}" in section_scores else "S1"
        section_scores[s_key]["total"] += 1
        if is_corr:
            section_scores[s_key]["correct"] += 1
            
        if q_type not in type_scores:
            type_scores[q_type] = {"correct": 0, "total": 0}
        type_scores[q_type]["total"] += 1
        if is_corr:
            type_scores[q_type]["correct"] += 1
            
        detailed_results.append({
            "question_id": q_id,
            "section_index": s_sec,
            "question_type": q_type,
            "user_answer": user_ans,
            "answer_key": ans_key,
            "explanation": exp,
            "is_correct": is_corr
        })

    # Calculate Official Cambridge Band Score based on Listening standard
    band_score = ObjectiveScoringEngine.calculate_raw_to_band(correct_count, total_questions, "Listening", "Academic")
    desc_info = ObjectiveScoringEngine.get_band_descriptor_info(band_score)

    # Record into practice_results, skill_mastery, and mistake_notebook
    try:
        for l_item in detailed_results:
            cursor.execute("""
                INSERT INTO practice_results (user_id, skill, question_id, user_answer, is_correct, time_taken_seconds)
                VALUES (?, 'Listening', ?, ?, ?, ?)
            """, (user_id, l_item["question_id"], str(l_item["user_answer"]), 1 if l_item["is_correct"] else 0, 35))
            
            cursor.execute("""
                INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
                VALUES (?, 'Listening', ?, 1, ?, ?, 0, ?)
                ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
                    total_attempted = total_attempted + 1,
                    total_correct = total_correct + excluded.total_correct,
                    independent_correct = independent_correct + excluded.independent_correct,
                    mastery_percentage = ROUND((total_correct + excluded.total_correct) * 100.0 / (total_attempted + 1), 1),
                    last_updated = CURRENT_TIMESTAMP
            """, (user_id, l_item["question_type"], 1 if l_item["is_correct"] else 0, 1 if l_item["is_correct"] else 0, 100.0 if l_item["is_correct"] else 0.0))

            if not l_item["is_correct"] and l_item["user_answer"]:
                cursor.execute("""
                    INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
                    VALUES (?, 'Listening', ?, ?, ?, ?, ?, 'Needs Practice')
                """, (user_id, l_item["question_type"], f"Listening Q#{l_item['question_id']}", str(l_item["user_answer"]), str(l_item["answer_key"]), str(l_item["explanation"] or "")))
    except Exception as e_rec:
        print("Notice: listening practice_results record error:", e_rec)

    try:
        cursor.execute("UPDATE profiles SET current_level = ? WHERE user_id = ?", (band_score, user_id))
        conn.commit()
    except Exception:
        pass
    conn.close()
    
    return {
        "band_score": band_score,
        "descriptor": desc_info["descriptor"],
        "cefr": desc_info["cefr"],
        "cefr_label": f"Band {band_score:.1f} - {desc_info['descriptor']} ({desc_info['cefr']})",
        "total_correct": correct_count,
        "total_questions": total_questions,
        "section_scores": section_scores,
        "type_scores": type_scores,
        "detailed_results": detailed_results
    }

@app.post("/api/v1/writing/evaluate")
def api_evaluate_writing(payload: dict = Body(...)):
    user_id = payload.get("user_id", 1)
    task_type = payload.get("task_type", "Task 2 Essay")
    prompt_title = payload.get("prompt_title", "Writing Task")
    prompt_text = payload.get("prompt_text", "")
    submission_text = payload.get("submission_text", "")
    time_spent = payload.get("time_spent_seconds", 1200)

    result = WritingEvaluatorEngine.submit_and_evaluate(user_id, task_type, prompt_title, prompt_text, submission_text, time_spent)
    return JSONResponse(content=result)

@app.get("/api/v1/writing/prompts")
def api_writing_prompts():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, skill, test_type, section_number, title, question_type, 
               passage_or_context, question_text, explanation, cambridge_book 
        FROM questions WHERE skill = 'Writing' 
        ORDER BY section_number ASC, id ASC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return JSONResponse(content={"tasks": rows})

@app.post("/api/v1/writing/generate-topic")
def api_writing_generate_topic(payload: dict = Body(...)):
    task_type = payload.get("task_type", "Task 2 - Agree or Disagree")
    custom_theme = payload.get("custom_theme", "")
    
    from ai_engine.writing_question_generator import WritingQuestionGenerator
    generator = WritingQuestionGenerator()
    result = generator.generate_custom_topic_prompt(task_type, custom_theme)
    return JSONResponse(content={"status": "success", "data": result})

@app.post("/api/v1/writing/generate-full-set")
def api_writing_generate_full_set():
    from ai_engine.writing_question_generator import WritingQuestionGenerator
    generator = WritingQuestionGenerator()
    result = generator.generate_full_writing_exam_set()
    return JSONResponse(content={"status": "success", "data": result})

@app.post("/api/v1/writing/save-custom-prompt")
def api_writing_save_custom_prompt(payload: dict = Body(...)):
    task_num = int(payload.get("task_num", 2))
    title = payload.get("title", "Custom Student Task")
    question_type = payload.get("question_type", f"Task {task_num} Custom")
    prompt_statement = payload.get("prompt_statement", "")
    chart_svg_or_img = payload.get("chart_svg_or_img", "")
    instructions = payload.get("instructions", "Write according to official Cambridge specifications.")

    is_task_1 = (task_num == 1)
    test_type = "Academic Task 1" if is_task_1 else "Task 2"
    min_words = 150 if is_task_1 else 250

    if is_task_1:
        visual_html = f"""<div class="chart-wrapper" style="background:#0f172a; padding:18px; border-radius:10px; margin:16px 0; border:1px solid #334155; text-align:center;">
    {chart_svg_or_img if chart_svg_or_img.strip() else '<p style="color:#94a3b8; font-style:italic;">[ Custom User Visual Dataset / Chart ]</p>'}
</div>"""
        context_html = f"""<div class="cambridge-prompt-header">
    <p><b>You should spend about 20 minutes on this task.</b></p>
    <p><i>{prompt_statement}</i></p>
    <p><b>Summarise the information by selecting and reporting the main features, and make comparisons where relevant.</b></p>
    <p><b>Write at least {min_words} words.</b></p>
</div>
{visual_html}"""
    else:
        context_html = f"""<div class="cambridge-prompt-header">
    <p><b>You should spend about 40 minutes on this task.</b></p>
    <p>Write about the following topic:</p>
    <div class="prompt-statement-highlight">
        <b>{prompt_statement}</b>
    </div>
    <p><i>Give reasons for your answer and include any relevant examples from your own knowledge or experience.</i></p>
    <p><b>Write at least {min_words} words.</b></p>
</div>"""

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO questions (
            skill, test_type, section_number, title, question_type,
            passage_or_context, question_text, options_json, answer_key,
            explanation, difficulty, cambridge_book, test_number,
            passage_or_section, difficulty_band, group_id, group_instructions
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "Writing", test_type, task_num, title, question_type,
        context_html, prompt_statement, json.dumps([]), "Custom Band 9 Benchmark",
        "### Custom Prompt Created by Student.", "medium", "Student Custom", 1,
        f"Task {task_num}", "Academic", "W_STUDENT_CUSTOM", instructions
    ))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return JSONResponse(content={"status": "success", "id": new_id, "task_num": task_num})

# --- ARIA AI WRITING CO-PILOT HELP ENDPOINTS ---
@app.post("/api/v1/writing/ai-help/brainstorm")
def api_writing_ai_brainstorm(payload: dict = Body(...)):
    task_type = payload.get("task_type", "Task 2")
    prompt_title = payload.get("prompt_title", "")
    prompt_statement = payload.get("prompt_statement", "")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    data = helper.get_brainstorm_ideas(task_type, prompt_title, prompt_statement)
    return JSONResponse(content={"status": "success", "data": data})

@app.post("/api/v1/writing/ai-help/outline")
def api_writing_ai_outline(payload: dict = Body(...)):
    task_type = payload.get("task_type", "Task 2")
    prompt_title = payload.get("prompt_title", "")
    prompt_statement = payload.get("prompt_statement", "")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    data = helper.get_essay_outline(task_type, prompt_title, prompt_statement)
    return JSONResponse(content={"status": "success", "data": data})

@app.post("/api/v1/writing/ai-help/vocabulary")
def api_writing_ai_vocabulary(payload: dict = Body(...)):
    task_type = payload.get("task_type", "Task 2")
    prompt_title = payload.get("prompt_title", "")
    prompt_statement = payload.get("prompt_statement", "")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    data = helper.get_topic_vocabulary(task_type, prompt_title, prompt_statement)
    return JSONResponse(content={"status": "success", "data": data})

@app.post("/api/v1/writing/ai-help/paraphrase")
def api_writing_ai_paraphrase(payload: dict = Body(...)):
    task_type = payload.get("task_type", "Task 2")
    prompt_statement = payload.get("prompt_statement", "")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    data = helper.get_intro_paraphrases(task_type, prompt_statement)
    return JSONResponse(content={"status": "success", "data": data})

@app.post("/api/v1/writing/ai-help/polish-sentence")
def api_writing_ai_polish_sentence(payload: dict = Body(...)):
    sentence = payload.get("sentence", "")
    task_type = payload.get("task_type", "Task 2")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    data = helper.polish_sentence(sentence, task_type)
    return JSONResponse(content={"status": "success", "data": data})

@app.post("/api/v1/writing/ai-help/tutor-chat")
def api_writing_ai_tutor_chat(payload: dict = Body(...)):
    user_message = payload.get("user_message", "")
    prompt_title = payload.get("prompt_title", "")
    prompt_statement = payload.get("prompt_statement", "")
    student_essay_so_far = payload.get("student_essay_so_far", "")
    from ai_engine.writing_ai_helper import WritingAIHelper
    helper = WritingAIHelper()
    reply = helper.tutor_chat(user_message, prompt_title, prompt_statement, student_essay_so_far)
    return JSONResponse(content={"status": "success", "reply": reply})

@app.post("/api/v1/speaking/evaluate")
def api_evaluate_speaking(payload: dict = Body(...)):
    user_id = payload.get("user_id", 1)
    part_number = payload.get("part_number", 1)
    prompt_title = payload.get("prompt_title", "Speaking Part 1")
    prompt_text = payload.get("prompt_text", "")
    transcript = payload.get("transcript", "")
    audio_path = payload.get("audio_file_path", "")
    time_spent = payload.get("time_spent_seconds", 45)

    result = SpeakingEvaluatorEngine.submit_and_evaluate(user_id, part_number, prompt_title, prompt_text, transcript, audio_path, time_spent)
    return JSONResponse(content=result)

@app.post("/api/v1/speaking/hint")
def api_speaking_hint(payload: dict = Body(...)):
    question_text = payload.get("question", "")
    part_number   = payload.get("part_number", 1)
    if not question_text:
        return JSONResponse(content={"error": "question required"}, status_code=400)
    result = ai_router.generate_speaking_hint(question_text, part_number)
    return JSONResponse(content=result)

@app.post("/api/v1/speaking/model-answer")
def api_speaking_model_answer(payload: dict = Body(...)):
    question_text = payload.get("question", "")
    part_number   = payload.get("part_number", 1)
    if not question_text:
        return JSONResponse(content={"error": "question required"}, status_code=400)
    result = ai_router.generate_model_answer(question_text, part_number)
    return JSONResponse(content=result)

@app.post("/api/v1/speaking/generate-set")
def api_speaking_generate_set(payload: dict = Body(...)):
    theme = payload.get("theme", "")
    p1_topic = payload.get("p1_topic", "")
    p2_topic = payload.get("p2_topic", "")
    p3_topic = payload.get("p3_topic", "")
    from ai_engine.speaking_question_generator import SpeakingQuestionGenerator
    generator = SpeakingQuestionGenerator()
    result = generator.generate_full_speaking_set(custom_theme=theme, p1_topic=p1_topic, p2_topic=p2_topic, p3_topic=p3_topic)
    return JSONResponse(content=result)

@app.post("/api/v1/speaking/examiner-reaction")
def api_speaking_examiner_reaction(payload: dict = Body(...)):
    candidate_speech = payload.get("candidate_speech", "")
    current_question = payload.get("current_question", "")
    next_question = payload.get("next_question", "")
    part_number = payload.get("part_number", 1)
    topic_context = payload.get("topic_context", "")
    is_part_transition = payload.get("is_part_transition", False)
    intro_step = payload.get("intro_step", 0)

    from ai_engine.speaking_examiner_agent import SpeakingExaminerAgent
    agent = SpeakingExaminerAgent()
    reaction = agent.generate_reaction(
        candidate_speech=candidate_speech,
        current_question=current_question,
        next_question=next_question,
        part_number=part_number,
        topic_context=topic_context,
        is_part_transition=is_part_transition,
        intro_step=intro_step
    )
    return JSONResponse(content=reaction)


@app.post("/api/v1/ai/teacher-chat")
def api_teacher_chat(payload: dict = Body(...)):
    user_message = payload.get("user_message", "")
    user_id = payload.get("user_id", 1)
    conversation_history = payload.get("history", [])
    context_data = payload.get("context", {})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    profile_row = cursor.fetchone()
    conn.close()

    context = dict(profile_row) if profile_row else {"target_band": 7.5, "current_level": 6.5, "mother_language": "Bengali", "teacher_language_pref": "English + Native"}
    context.update(context_data)
    
    # Map frontend lang_pref selection
    raw_lang = payload.get("lang_pref") or context_data.get("lang_pref")
    if raw_lang:
        if raw_lang == "mother":
            context["teacher_language_pref"] = "Native Only"
        elif raw_lang == "english":
            context["teacher_language_pref"] = "English Only"
        else:
            context["teacher_language_pref"] = "English + Native"
    
    result = ai_router.teacher_chat(user_message, conversation_history, context)
    return JSONResponse(content=result)

@app.post("/api/v1/ai/chat/stream")
def api_teacher_chat_stream(payload: dict = Body(...)):
    user_message = payload.get("user_message", "")
    user_id = payload.get("user_id", 1)
    conversation_history = payload.get("history", [])
    context_data = payload.get("context", {})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    profile_row = cursor.fetchone()
    conn.close()

    context = dict(profile_row) if profile_row else {"target_band": 7.5, "current_level": 6.5, "mother_language": "Bengali", "teacher_language_pref": "English + Native"}
    context.update(context_data)

    raw_lang = payload.get("lang_pref") or context_data.get("lang_pref")
    if raw_lang:
        if raw_lang == "mother":
            context["teacher_language_pref"] = "Native Only"
        elif raw_lang == "english":
            context["teacher_language_pref"] = "English Only"
        else:
            context["teacher_language_pref"] = "English + Native"

    def event_generator():
        for chunk in ai_router.stream_teacher_chat(user_message, conversation_history, context):
            yield f"data: {json.dumps({'text': chunk})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

@app.post("/api/v1/ai/tts")
def api_generate_tts(payload: dict = Body(...)):
    """Generate high-quality audio pronunciation/speech for AI Teacher."""
    text = payload.get("text", "").strip()
    lang = payload.get("lang_pref", "en")
    if not text:
        return JSONResponse(content={"status": "error", "message": "Text is required"}, status_code=400)
    
    clean_text = re.sub(r'[*_`#>-]', '', text)[:350].strip()
    if not clean_text:
        return JSONResponse(content={"status": "error", "message": "Empty text"})
    
    has_bengali = any(0x0980 <= ord(c) <= 0x09FF for c in clean_text)
    t_lang = 'bn' if (has_bengali or lang == 'bn') else 'en'
    
    h = hashlib.md5(f"{t_lang}_{clean_text}".encode('utf-8')).hexdigest()
    filename = f"tts_{h}.mp3"
    audio_dir = os.path.join(BASE_DIR, "static", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    filepath = os.path.join(audio_dir, filename)

    if not os.path.exists(filepath):
        try:
            from gtts import gTTS
            tts = gTTS(text=clean_text, lang=t_lang, slow=False)
            tts.save(filepath)
        except Exception as e:
            try:
                from gtts import gTTS
                tts = gTTS(text=clean_text, lang='en', slow=False)
                tts.save(filepath)
            except Exception as e2:
                print("gTTS error:", e2)
                return JSONResponse(content={"status": "error", "message": str(e2)}, status_code=500)
            
    return JSONResponse(content={"status": "success", "audio_url": f"/static/audio/{filename}"})


# === AI-Powered Reading Question Generator ===
@app.post("/api/v1/reading/generate-practice")
def api_generate_reading_practice(payload: dict = Body({})):
    """Generate a fresh Cambridge-style Reading practice set using AI with optional custom question types."""
    from ai_engine.reading_question_generator import ReadingQuestionGenerator, ALL_14_QUESTION_TYPES, TYPE_ROTATIONS
    
    conn = get_db()
    cursor = conn.cursor()
    # Correct query for active Gemini keys
    cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active' ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    api_keys = [r["api_key"] for r in rows if r["api_key"]]
    if not api_keys:
        env_k = os.environ.get("GEMINI_API_KEY", "")
        if env_k:
            api_keys.append(env_k)
    
    custom_types = payload.get("custom_types")
    
    generator = ReadingQuestionGenerator()
    try:
        result = generator.generate_practice_set(
            api_key=api_keys[0] if api_keys else "",
            api_key_pool=api_keys,
            custom_types=custom_types
        )
        
        if result and "passages" in result and len(result["passages"]) > 0:
            # Save generated questions to database
            conn2 = get_db()
            cursor2 = conn2.cursor()
            cursor2.execute("DELETE FROM questions WHERE skill = 'Reading'")
            
            total_qs = 0
            for passage in result["passages"]:
                p_num = passage.get("number", 1)
                p_title = f"Passage {p_num}: {passage.get('title', 'Academic Reading')}"
                p_text = passage.get("text", "")
                
                for q in passage.get("questions", []):
                    total_qs += 1
                    cursor2.execute('''INSERT INTO questions (title, skill, test_type, section_number, question_type, passage_or_context, question_text, options_json, answer_key, explanation, difficulty, cambridge_book, test_number, passage_or_section, difficulty_band, group_id, group_instructions) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        p_title,
                        'Reading',
                        'Academic',
                        p_num,
                        q.get("type", "Multiple Choice"),
                        p_text,
                        q.get("text", ""),
                        json.dumps(q.get("options", [])),
                        q.get("answer", ""),
                        q.get("explanation", ""),
                        q.get("difficulty", "medium"),
                        19,
                        1,
                        p_num,
                        7.0,
                        q.get("group_id", f"P{p_num}_G1"),
                        q.get("group_instructions", "")
                    ))
            
            conn2.commit()
            conn2.close()
            
            return JSONResponse(content={"status": "ok", "message": "নতুন ক্যামব্রিজ প্র্যাকটিস সেট সফলভাবে তৈরি হয়েছে!", "total_questions": total_qs})
        else:
            return JSONResponse(content={"status": "fallback", "message": "AI ফলব্যাক সেট লোড হয়েছে"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/v1/reading/switch-set")
def api_switch_reading_set(payload: dict = Body(...)):
    """Switch reading set between SET A (Authentic Cambridge 19) and SET B (Authentic Cambridge 18)."""
    set_name = payload.get("set_name", "A").upper()
    try:
        from seed_authentic_cambridge_reading_full import seed_full_cambridge_reading, seed_cambridge_reading_set_b
        if set_name == "B":
            seed_cambridge_reading_set_b()
            msg = "ক্যামব্রিজ সেট B (Book 18) সফলভাবে লোড হয়েছে!"
        else:
            seed_full_cambridge_reading()
            msg = "ক্যামব্রিজ সেট A (Book 19) সফলভাবে লোড হয়েছে!"
        return JSONResponse(content={"status": "ok", "message": msg, "active_set": set_name})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

# === AI-Powered Listening Question Generator ===
@app.post("/api/v1/listening/generate-practice")
def api_generate_listening_practice(payload: dict = Body({})):
    """Generate a fresh Cambridge-style Listening practice set using AI with optional custom question types."""
    from ai_engine.listening_question_generator import ListeningQuestionGenerator
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id = 'gemini' AND status = 'Active' ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    api_keys = [r["api_key"] for r in rows if r["api_key"]]
    if not api_keys:
        env_k = os.environ.get("GEMINI_API_KEY", "")
        if env_k:
            api_keys.append(env_k)
    
    custom_types = payload.get("custom_types")
    generator = ListeningQuestionGenerator()
    try:
        result = generator.generate_practice_set(
            api_key=api_keys[0] if api_keys else "",
            api_key_pool=api_keys,
            custom_types=custom_types
        )
        
        if result and "sections" in result and len(result["sections"]) > 0:
            conn2 = get_db()
            cursor2 = conn2.cursor()
            cursor2.execute("DELETE FROM questions WHERE skill = 'Listening'")
            
            total_qs = 0
            for sec in result["sections"]:
                s_num = sec.get("section_number", 1)
                s_title = f"Section {s_num}: {sec.get('title', 'Listening Section')}"
                s_transcript = sec.get("transcript", "")
                
                for q in sec.get("questions", []):
                    total_qs += 1
                    cursor2.execute('''INSERT INTO questions (title, skill, test_type, section_number, question_type, passage_or_context, question_text, options_json, answer_key, explanation, difficulty, cambridge_book, test_number, passage_or_section, difficulty_band) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                        s_title,
                        'Listening',
                        'Academic',
                        s_num,
                        q.get("type", "Note Completion"),
                        s_transcript,
                        q.get("text", ""),
                        json.dumps(q.get("options", [])),
                        q.get("answer", ""),
                        q.get("explanation", ""),
                        "Hard" if s_num == 4 else ("Medium" if s_num in [2,3] else "Easy"),
                        19,
                        1,
                        s_num,
                        7.5
                    ))
            
            conn2.commit()
            conn2.close()
            
            return JSONResponse(content={"status": "ok", "message": "নতুন ক্যামব্রিজ লিসেনিং প্র্যাকটিস সেট সফলভাবে তৈরি হয়েছে!", "total_questions": total_qs})
        else:
            return JSONResponse(content={"status": "fallback", "message": "ফলব্যাক সেট লোড হয়েছে"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/api/v1/listening/switch-set")
def api_switch_listening_set(payload: dict = Body(...)):
    """Switch listening set between authentic Cambridge sets."""
    try:
        from seed_authentic_cambridge_listening_full import seed_full_cambridge_listening
        seed_full_cambridge_listening()
        return JSONResponse(content={"status": "ok", "message": "ক্যামব্রিজ লিসেনিং সেট সফলভাবে রিলোড হয়েছে!"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)


@app.get("/api/v1/admin/ai-health")
def api_admin_ai_health():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, provider_id, api_key_masked, status, latency_ms, error_count, last_used_at, COALESCE(label, '') as label FROM ai_credentials ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    credentials = [dict(r) for r in rows]
    return JSONResponse(content={"credentials": credentials})


@app.post("/api/v1/ai/translate")
def api_translate(payload: dict = Body(...)):
    """Translate English text to Bengali using Gemini AI or fallback engine."""
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id='gemini' AND status != 'Disabled' ORDER BY id ASC LIMIT 1")
    row = cursor.fetchone()
    if not row:
        cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id='gemini' LIMIT 1")
        row = cursor.fetchone()
    conn.close()

    api_key = row["api_key"] if row else None

    if api_key:
        prompt = f"""Translate the following English text to natural, conversational Bengali (Bangla).
Rules:
- Keep IELTS technical terms in English (e.g. Band Score, True/False/Not Given, Task 1, etc.)
- Write in easy everyday Bengali that an IELTS student would understand
- Do NOT add any explanation, just return the translation only

English text:
{text}

Bengali translation:"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
            resp = requests.post(url, json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024}
            }, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                translation = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return JSONResponse(content={"translation": translation})
        except Exception:
            pass

    # Free fallback translation service
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=bn&dt=t&q={requests.utils.quote(text[:1000])}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            res_json = resp.json()
            translation = "".join([segment[0] for segment in res_json[0] if segment[0]])
            return JSONResponse(content={"translation": translation})
    except Exception:
        pass

    return JSONResponse(content={"translation": "অনুবাদ: এটি ইংরেজি আইইএলটিএস টিচিং কন্টেন্ট।"})



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)