import sqlite3
import json
from typing import Dict, Any, List, Optional
from scoring_engine.objective_scoring import ObjectiveScoringEngine

from database import get_db

def get_db_connection():
    return get_db()

def calculate_ielts_overall(bands: List[float]) -> Optional[float]:
    if not bands:
        return None
    raw_avg = sum(bands) / len(bands)
    integer_part = int(raw_avg)
    decimal_part = raw_avg - integer_part
    if decimal_part < 0.25:
        return float(integer_part)
    elif decimal_part < 0.75:
        return float(integer_part) + 0.5
    else:
        return float(integer_part) + 1.0

def get_full_user_analytics(user_id: int = 1) -> Dict[str, Any]:
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Profile & Target
    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    p_row = cursor.fetchone()
    profile = dict(p_row) if p_row else {}
    target_band = float(profile.get("target_band") or 7.5)
    ielts_type = profile.get("ielts_type") or "Academic"

    # 2. Reading Analytics
    cursor.execute("""
        SELECT COUNT(*) as total_q,
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_q,
               AVG(time_taken_seconds) as avg_time
        FROM practice_results
        WHERE user_id = ? AND skill = 'Reading'
    """, (user_id,))
    r_res = cursor.fetchone()
    r_total_q = r_res["total_q"] if r_res else 0
    r_correct_q = r_res["correct_q"] if r_res and r_res["correct_q"] else 0
    r_avg_time = round(r_res["avg_time"] or 0, 1) if r_res else 0

    cursor.execute("""
        SELECT question_type, total_attempted, total_correct, mastery_percentage
        FROM skill_mastery
        WHERE user_id = ? AND skill = 'Reading'
        ORDER BY total_attempted DESC
    """, (user_id,))
    reading_mastery_rows = [dict(r) for r in cursor.fetchall()]

    reading_has_data = r_total_q > 0 or len(reading_mastery_rows) > 0
    if reading_has_data:
        # If total attempted is recorded in practice_results
        tot = r_total_q if r_total_q > 0 else sum(m["total_attempted"] for m in reading_mastery_rows)
        corr = r_correct_q if r_total_q > 0 else sum(m["total_correct"] for m in reading_mastery_rows)
        r_accuracy = round((corr / tot) * 100.0, 1) if tot > 0 else 0.0
        # Scaled to 40 questions to compute official band
        scaled_correct = int(round((corr / tot) * 40)) if tot > 0 else 0
        r_band = ObjectiveScoringEngine.calculate_raw_to_band(scaled_correct, 40, "Reading", ielts_type)
    else:
        tot = 0
        corr = 0
        r_accuracy = None
        r_band = None

    reading_data = {
        "has_data": reading_has_data,
        "band": r_band,
        "accuracy_pct": r_accuracy,
        "total_attempted": tot,
        "total_correct": corr,
        "avg_time_seconds": r_avg_time,
        "question_types": reading_mastery_rows
    }

    # 3. Listening Analytics
    cursor.execute("""
        SELECT COUNT(*) as total_q,
               SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct_q,
               AVG(time_taken_seconds) as avg_time
        FROM practice_results
        WHERE user_id = ? AND skill = 'Listening'
    """, (user_id,))
    l_res = cursor.fetchone()
    l_total_q = l_res["total_q"] if l_res else 0
    l_correct_q = l_res["correct_q"] if l_res and l_res["correct_q"] else 0
    l_avg_time = round(l_res["avg_time"] or 0, 1) if l_res else 0

    cursor.execute("""
        SELECT question_type, total_attempted, total_correct, mastery_percentage
        FROM skill_mastery
        WHERE user_id = ? AND skill = 'Listening'
        ORDER BY total_attempted DESC
    """, (user_id,))
    listening_mastery_rows = [dict(r) for r in cursor.fetchall()]

    listening_has_data = l_total_q > 0 or len(listening_mastery_rows) > 0
    if listening_has_data:
        l_tot = l_total_q if l_total_q > 0 else sum(m["total_attempted"] for m in listening_mastery_rows)
        l_corr = l_correct_q if l_total_q > 0 else sum(m["total_correct"] for m in listening_mastery_rows)
        l_accuracy = round((l_corr / l_tot) * 100.0, 1) if l_tot > 0 else 0.0
        scaled_correct = int(round((l_corr / l_tot) * 40)) if l_tot > 0 else 0
        l_band = ObjectiveScoringEngine.calculate_raw_to_band(scaled_correct, 40, "Listening", ielts_type)
    else:
        l_tot = 0
        l_corr = 0
        l_accuracy = None
        l_band = None

    listening_data = {
        "has_data": listening_has_data,
        "band": l_band,
        "accuracy_pct": l_accuracy,
        "total_attempted": l_tot,
        "total_correct": l_corr,
        "avg_time_seconds": l_avg_time,
        "question_types": listening_mastery_rows
    }

    # 4. Writing Analytics
    cursor.execute("""
        SELECT we.*, ws.task_type, ws.prompt_title, ws.word_count, ws.created_at as submitted_at
        FROM writing_evaluations we
        JOIN writing_submissions ws ON we.submission_id = ws.id
        WHERE ws.user_id = ?
        ORDER BY we.id DESC
    """, (user_id,))
    writing_rows = [dict(r) for r in cursor.fetchall()]

    writing_has_data = len(writing_rows) > 0
    if writing_has_data:
        latest_w = writing_rows[0]
        w_band = float(latest_w.get("overall_band") or 0.0)
        ta_score = float(latest_w.get("task_achievement") or 0.0)
        cc_score = float(latest_w.get("coherence_cohesion") or 0.0)
        lr_score = float(latest_w.get("lexical_resource") or 0.0)
        gra_score = float(latest_w.get("grammatical_range") or 0.0)
        
        try:
            strengths = json.loads(latest_w.get("strengths_json") or "[]")
        except Exception:
            strengths = []
        try:
            weaknesses = json.loads(latest_w.get("weaknesses_json") or "[]")
        except Exception:
            weaknesses = []
        try:
            corrections = json.loads(latest_w.get("line_by_line_errors_json") or "[]")
        except Exception:
            corrections = []

        task1_count = sum(1 for w in writing_rows if "1" in str(w.get("task_type", "")))
        task2_count = sum(1 for w in writing_rows if "2" in str(w.get("task_type", "")))
        avg_wc = int(sum(w.get("word_count") or 0 for w in writing_rows) / len(writing_rows))
    else:
        w_band = None
        ta_score = None
        cc_score = None
        lr_score = None
        gra_score = None
        strengths = []
        weaknesses = []
        corrections = []
        task1_count = 0
        task2_count = 0
        avg_wc = 0

    writing_data = {
        "has_data": writing_has_data,
        "overall_band": w_band,
        "task_achievement": ta_score,
        "coherence_cohesion": cc_score,
        "lexical_resource": lr_score,
        "grammatical_range": gra_score,
        "total_submissions": len(writing_rows),
        "task1_count": task1_count,
        "task2_count": task2_count,
        "avg_word_count": avg_wc,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "corrections": corrections,
        "recent_submissions": writing_rows[:5]
    }

    # 5. Speaking Analytics
    cursor.execute("""
        SELECT se.*, ss.prompt_title, ss.part_number, ss.created_at as session_date
        FROM speaking_evaluations se
        JOIN speaking_sessions ss ON se.session_id = ss.id
        WHERE ss.user_id = ?
        ORDER BY se.id DESC
    """, (user_id,))
    speaking_rows = [dict(r) for r in cursor.fetchall()]

    speaking_has_data = len(speaking_rows) > 0
    if speaking_has_data:
        latest_s = speaking_rows[0]
        s_band = float(latest_s.get("overall_band") or 0.0)
        fc_score = float(latest_s.get("fluency_coherence") or 0.0)
        s_lr_score = float(latest_s.get("lexical_resource") or 0.0)
        s_gra_score = float(latest_s.get("grammatical_range") or 0.0)
        pr_score = float(latest_s.get("pronunciation") or 0.0)

        try:
            s_strengths = json.loads(latest_s.get("strengths_json") or "[]")
        except Exception:
            s_strengths = []
        try:
            s_weaknesses = json.loads(latest_s.get("weaknesses_json") or "[]")
        except Exception:
            s_weaknesses = []
        try:
            phonetic_fb = json.loads(latest_s.get("phonetic_feedback_json") or "[]")
        except Exception:
            phonetic_fb = []
    else:
        s_band = None
        fc_score = None
        s_lr_score = None
        s_gra_score = None
        pr_score = None
        s_strengths = []
        s_weaknesses = []
        phonetic_fb = []

    speaking_data = {
        "has_data": speaking_has_data,
        "overall_band": s_band,
        "fluency_coherence": fc_score,
        "lexical_resource": s_lr_score,
        "grammatical_range": s_gra_score,
        "pronunciation": pr_score,
        "total_sessions": len(speaking_rows),
        "strengths": s_strengths,
        "weaknesses": s_weaknesses,
        "phonetic_feedback": phonetic_fb,
        "recent_sessions": speaking_rows[:5]
    }

    # 6. Vocabulary Analytics (from vocab_user_progress)
    from ai_engine.vocabulary_evaluator import get_user_vocab_srs_stats
    v_stats = get_user_vocab_srs_stats(user_id)
    vocab_data = {
        "mastered_count": v_stats.get("mastered_count", 0),
        "review_due_count": v_stats.get("review_due_count", 0),
        "learning_count": v_stats.get("learning_count", 0),
        "total_sentences": v_stats.get("total_sentences", 0),
        "weak_words": v_stats.get("weak_words", [])[:10],
        "total_words_studied": v_stats.get("mastered_count", 0) + v_stats.get("review_due_count", 0) + v_stats.get("learning_count", 0)
    }

    # 7. Mistake Notebook Analytics
    cursor.execute("""
        SELECT skill, question_type, COUNT(*) as count
        FROM mistake_notebook
        WHERE user_id = ?
        GROUP BY skill, question_type
        ORDER BY count DESC
    """, (user_id,))
    mistake_rows = [dict(r) for r in cursor.fetchall()]
    total_mistakes = sum(m["count"] for m in mistake_rows)

    cursor.execute("""
        SELECT id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status
        FROM mistake_notebook
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,))
    recent_mistakes = [dict(r) for r in cursor.fetchall()]

    mistakes_data = {
        "total_mistakes": total_mistakes,
        "by_skill": mistake_rows,
        "recent_mistakes": recent_mistakes
    }

    # 8. Overall Projected Band Calculation
    valid_bands = []
    if reading_data["band"] is not None:
        valid_bands.append(reading_data["band"])
    if listening_data["band"] is not None:
        valid_bands.append(listening_data["band"])
    if writing_data["overall_band"] is not None:
        valid_bands.append(writing_data["overall_band"])
    if speaking_data["overall_band"] is not None:
        valid_bands.append(speaking_data["overall_band"])

    completed_modules_count = len(valid_bands)
    projected_overall = calculate_ielts_overall(valid_bands)
    
    if projected_overall is not None:
        band_gap = round(target_band - projected_overall, 1)
        readiness_status = "Full 4-Module Evaluated" if completed_modules_count == 4 else f"{completed_modules_count} of 4 Modules Assessed"
    else:
        band_gap = None
        readiness_status = "Diagnostic Test Needed"

    conn.close()

    return {
        "profile": profile,
        "target_band": target_band,
        "ielts_type": ielts_type,
        "projected_overall_band": projected_overall,
        "completed_modules_count": completed_modules_count,
        "band_gap": band_gap,
        "readiness_status": readiness_status,
        "reading": reading_data,
        "listening": listening_data,
        "writing": writing_data,
        "speaking": speaking_data,
        "vocab": vocab_data,
        "mistakes": mistakes_data,
        "total_practice_items": tot + l_tot + writing_data["total_submissions"] + speaking_data["total_sessions"] + vocab_data["total_words_studied"]
    }

def reset_analytics_data(user_id: int = 1, conn=None) -> bool:
    close_at_end = False
    if conn is None:
        conn = get_db_connection()
        close_at_end = True
    cursor = conn.cursor()
    cursor.execute("DELETE FROM practice_results WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM skill_mastery WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM mistake_notebook WHERE user_id = ?", (user_id,))
    
    cursor.execute("SELECT id FROM writing_submissions WHERE user_id = ?", (user_id,))
    w_ids = [r["id"] for r in cursor.fetchall()]
    for wid in w_ids:
        cursor.execute("DELETE FROM writing_evaluations WHERE submission_id = ?", (wid,))
    cursor.execute("DELETE FROM writing_submissions WHERE user_id = ?", (user_id,))

    cursor.execute("SELECT id FROM speaking_sessions WHERE user_id = ?", (user_id,))
    s_ids = [r["id"] for r in cursor.fetchall()]
    for sid in s_ids:
        cursor.execute("DELETE FROM speaking_evaluations WHERE session_id = ?", (sid,))
    cursor.execute("DELETE FROM speaking_sessions WHERE user_id = ?", (user_id,))

    conn.commit()
    if close_at_end:
        conn.close()
    return True

def seed_benchmark_data(user_id: int = 1) -> bool:
    conn = get_db_connection()
    reset_analytics_data(user_id, conn=conn)
    cursor = conn.cursor()

    # 1. Reading: 40 questions (31 correct -> Band 7.0 Academic)
    reading_types = [
        ("True / False / Not Given", 14, 11, 78.6),
        ("Matching Headings", 10, 6, 60.0),
        ("Multiple Choice", 8, 7, 87.5),
        ("Summary Completion", 8, 7, 87.5)
    ]
    q_counter = 1
    for q_type, tot, corr, mastery in reading_types:
        cursor.execute("""
            INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
            VALUES (?, 'Reading', ?, ?, ?, ?, 0, ?)
        """, (user_id, q_type, tot, corr, corr, mastery))

        for i in range(tot):
            is_c = 1 if i < corr else 0
            cursor.execute("""
                INSERT INTO practice_results (user_id, skill, question_id, user_answer, is_correct, time_taken_seconds)
                VALUES (?, 'Reading', ?, ?, ?, ?)
            """, (user_id, q_counter, "True" if is_c else "False", is_c, 48))
            q_counter += 1

    # 2. Listening: 40 questions (33 correct -> Band 7.5 Listening)
    listening_sections = [
        ("Part 1: Social Form Completion", 10, 9, 90.0),
        ("Part 2: Local Map Labelling", 10, 8, 80.0),
        ("Part 3: Academic Discussion MCQ", 10, 8, 80.0),
        ("Part 4: Science Lecture Note Completion", 10, 8, 80.0)
    ]
    for s_name, tot, corr, mastery in listening_sections:
        cursor.execute("""
            INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
            VALUES (?, 'Listening', ?, ?, ?, ?, 0, ?)
        """, (user_id, s_name, tot, corr, corr, mastery))

        for i in range(tot):
            is_c = 1 if i < corr else 0
            cursor.execute("""
                INSERT INTO practice_results (user_id, skill, question_id, user_answer, is_correct, time_taken_seconds)
                VALUES (?, 'Listening', ?, ?, ?, ?)
            """, (user_id, q_counter, "Word" if is_c else "Typo", is_c, 35))
            q_counter += 1

    # 3. Writing: 1 Task 2 submission with genuine Band 7.0 evaluation
    cursor.execute("""
        INSERT INTO writing_submissions (user_id, task_type, prompt_title, prompt_text, submission_text, word_count, time_spent_seconds)
        VALUES (?, 'Task 2 Essay',
                'Should university education be free for all students?',
                'Some people argue that tertiary education should be fully funded by governments, while others believe students should pay tuition fees. Discuss both views and give your opinion.',
                'In the modern knowledge-based economy, the question of whether tertiary education should be fully subsidized by the government remains contentious. While detractors argue that universal free education places an unsustainable burden on public revenues, I firmly contend that subsidizing higher education fosters meritocratic upward mobility and drives long-term economic prosperity.\\n\\nOn the one hand, proponents of tuition fees suggest that state-funded university schemes divert vital capital away from foundational public services like healthcare and primary schooling. From their perspective, individuals who attain university degrees typically command substantially higher lifetime earnings, making it equitable that beneficiaries share the financial investment of their qualifications.\\n\\nOn the other hand, financial barriers disproportionately deter talented students from lower-income backgrounds, exacerbating generational socioeconomic inequality. When tertiary institutions eliminate tuition hurdles, admission is governed strictly by academic aptitude rather than familial wealth. For instance, Nordic nations with tuition-free universities consistently report higher innovation indices and lower wealth disparities.\\n\\nIn conclusion, while funding tertiary education demands prudent fiscal planning, the collective societal benefits far outweigh initial expenditure. Consequently, governments ought to invest in higher education as an indispensable engine of national development.',
                286, 2340)
    """, (user_id,))
    w_sub_id = cursor.lastrowid

    strengths = [
        "Consistent academic tone with mature stance presented from the introduction to the conclusion.",
        "Well-structured cohesive body paragraphs with appropriate paragraph transitions ('On the one hand', 'In conclusion').",
        "High-density academic lexical chunks: 'socioeconomic inequality', 'meritocratic upward mobility', 'knowledge-based economy'."
    ]
    weaknesses = [
        "Minor punctuation slips in complex conditional structures.",
        "Ensure counter-arguments are examined with specific real-world empirical examples."
    ]
    corrections = [
        {"original": "goverment ought to pay", "fixed": "the government ought to subsidize", "explanation": "Spelling and lexical register upgrade."}
    ]

    cursor.execute("""
        INSERT INTO writing_evaluations (submission_id, task_achievement, coherence_cohesion, lexical_resource, grammatical_range, overall_band, strengths_json, weaknesses_json, line_by_line_errors_json, improvement_plan, provider_used)
        VALUES (?, 7.0, 7.0, 7.0, 6.5, 7.0, ?, ?, ?, 'Focus on complex clause punctuation and nominalization.', 'gemini')
    """, (w_sub_id, json.dumps(strengths), json.dumps(weaknesses), json.dumps(corrections)))

    # 4. Speaking: 1 Session with genuine Band 7.0 evaluation
    cursor.execute("""
        INSERT INTO speaking_sessions (user_id, part_number, prompt_title, prompt_text, audio_file_path, transcript, time_spent_seconds)
        VALUES (?, 2,
                'Describe a memorable journey you took by public transport',
                'You should say: where you went, what kind of transport you used, who you travelled with, and explain why it was memorable.',
                '/static/audio/sample_speaking.mp3',
                'I would like to talk about a train journey I took two years ago through the countryside. We boarded an intercity express early in the morning. What made this journey particularly memorable was the breathtaking panoramic scenery outside the carriage window. The lush green paddy fields and meandering rivers offered a spectacular escape from the hectic urban environment. Moreover, the carriage was spacious and quiet, allowing us to have uninterrupted conversations throughout the four-hour journey.',
                180)
    """, (user_id,))
    s_session_id = cursor.lastrowid

    spk_strengths = [
        "Extended discourse with natural flow and minimal hesitation.",
        "Accurate, natural collocations: 'panoramic scenery', 'hectic urban environment', 'uninterrupted conversations'."
    ]
    spk_weaknesses = [
        "A few moments of vowel reduction on unstressed syllables in multisyllabic terms."
    ]
    spk_phonetic = [
        "Clear rhythm and natural sentence stress on key content words."
    ]

    cursor.execute("""
        INSERT INTO speaking_evaluations (session_id, fluency_coherence, lexical_resource, grammatical_range, pronunciation, overall_band, strengths_json, weaknesses_json, phonetic_feedback_json, provider_used)
        VALUES (?, 7.0, 7.5, 6.5, 7.0, 7.0, ?, ?, ?, 'gemini')
    """, (s_session_id, json.dumps(spk_strengths), json.dumps(spk_weaknesses), json.dumps(spk_phonetic)))

    # 5. Mistake Notebook: 3 realistic mistakes
    cursor.execute("""
        INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
        VALUES (?, 'Reading', 'Matching Headings', 'Reading Passage 2 - Paragraph D', 'v. Technological advancements in travel', 'ii. The environmental impact of modern tourism', 'Paragraph D focuses primarily on carbon emissions and habitat loss, rather than technology.', 'Needs Practice')
    """, (user_id,))
    cursor.execute("""
        INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
        VALUES (?, 'Listening', 'Form Completion', 'Section 1 - Hotel Booking Q4', 'reservation', 'reservations', 'The audio clearly pronounced plural /z/ at the end. In IELTS Listening, singular/plural precision is strictly penalized.', 'Needs Practice')
    """, (user_id,))
    cursor.execute("""
        INSERT INTO mistake_notebook (user_id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status)
        VALUES (?, 'Writing', 'Grammar & Accuracy', 'Task 2 Punctuation', 'Education is vital, it changes society.', 'Education is vital; it changes society.', 'Comma splice between two grammatically complete independent clauses. Use a semicolon or conjunction.', 'Needs Practice')
    """, (user_id,))

    conn.commit()
    conn.close()
    return True

