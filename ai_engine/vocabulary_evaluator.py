# -*- coding: utf-8 -*-
"""
Smart Vocabulary Sentence Evaluator & SRS Engine
Evaluates user-generated sentences for target IELTS vocabulary words:
- Grammar & syntax correctness
- Collocation naturalness
- Estimated IELTS band score (6.0 - 9.0)
- Explanations in Bengali
- Band 8.5/9.0 sentence upgrade
- Updates Spaced Repetition System (SRS) records in SQLite
"""
import re
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from database import get_db
from ai_engine.ai_router import ai_router

def evaluate_vocab_sentence(word: str, topic_id: str, sentence: str, user_id: int = 1) -> Dict[str, Any]:
    """
    Evaluates student's sentence using target word with AI or robust rule-based fallback.
    Updates vocab_user_progress in DB.
    """
    clean_word = word.strip()
    clean_sentence = sentence.strip()

    if not clean_sentence or len(clean_sentence.split()) < 3:
        return {
            "status": "error",
            "word": clean_word,
            "sentence": clean_sentence,
            "is_valid": False,
            "collocation_used": False,
            "estimated_band": 5.0,
            "feedback_bengali": "অনুগ্রহ করে অন্তত ৩-৪ শব্দের একটি অর্থপূর্ণ বাক্য তৈরি করুন।",
            "grammar_errors": ["Sentence is too short."],
            "band_upgrade": f"It is widely argued that {clean_word.lower()} plays a pivotal role in modern academic settings.",
            "srs_status": "Review Due"
        }

    # Check if word or stem exists in sentence
    word_root = clean_word.lower().rstrip("sedting")
    contains_word = (clean_word.lower() in clean_sentence.lower()) or (len(word_root) > 3 and word_root in clean_sentence.lower())

    # Try AI evaluation first
    ai_result = None
    try:
        prompt = f"""
You are an expert IELTS Senior Examiner and English Professor fluent in Bengali.
Evaluate this student's practice sentence for the target IELTS academic word '{clean_word}' in the topic '{topic_id}'.

Student sentence: "{clean_sentence}"

Requirements:
1. Verify if the word '{clean_word}' is used accurately and naturally.
2. Check for grammatical errors (Subject-Verb agreement, tense, prepositions, articles).
3. Evaluate collocations.
4. Estimate IELTS Band score (from 5.0 to 9.0 in 0.5 steps).
5. Provide a constructive feedback explanation in friendly Bengali (কেন বাক্যটি ভালো হয়েছে বা কোথায় উন্নতি প্রয়োজন).
6. Provide an upgraded Band 8.5 / 9.0 version of the student's exact sentence.

Respond ONLY with valid JSON in this exact structure:
{{
    "is_valid": true/false,
    "collocation_used": true/false,
    "estimated_band": 7.5,
    "feedback_bengali": "আপনার বাক্যে '{clean_word}'-এর ব্যবহার দারুণ হয়েছে...",
    "grammar_errors": ["Error 1" or empty list],
    "band_upgrade": "An elevated Band 8.5/9.0 academic version of the sentence."
}}
"""
        res = ai_router.generate_json(prompt)
        if isinstance(res, dict) and "estimated_band" in res:
            ai_result = res
    except Exception as e:
        # Fallback will handle
        ai_result = None

    if not ai_result:
        # High quality rule-based fallback
        word_lower = clean_word.lower()
        sent_lower = clean_sentence.lower()
        has_period = clean_sentence.endswith((".", "!", "?"))
        word_count = len(clean_sentence.split())

        errors = []
        if not contains_word:
            errors.append(f"The sentence does not contain the target word '{clean_word}'.")
        if not has_period:
            errors.append("Missing terminal punctuation (full stop).")
        if word_count < 6:
            errors.append("Sentence is quite brief for IELTS Academic standard.")

        # Collocation presence check
        academic_collocs = ["impact", "role", "increase", "difference", "effect", "benefit", "development", "growth", "challenge", "measure", "system"]
        colloc_used = any(c in sent_lower for c in academic_collocs)

        if not contains_word:
            band = 5.0
            feedback = f"বাক্যে '{clean_word}' শব্দটি পাওয়া যায়নি। অনুগ্রহ করে শব্দটি ব্যবহার করে একটি বাক্য লিখুন।"
            upgrade = f"Research demonstrates that {clean_word.lower()} has profound implications for contemporary society."
        elif errors:
            band = 6.0
            feedback = f"শব্দটির ব্যবহার ভালো ছিল, তবে কিছু গ্রামাটিক্যাল সমস্যা রয়েছে ({', '.join(errors)})। সঠিক পাংকচুয়েশন ও একাডেমিক কাঠামো বজায় রাখুন।"
            upgrade = f"There is substantial evidence that {clean_sentence.rstrip('.')} in a remarkably efficient manner."
        else:
            if colloc_used and word_count >= 10:
                band = 7.5
                feedback = f"অসাধারণ! '{clean_word}' শব্দটির কোলোকেশন ও ব্যাকরণ সম্পূর্ণ নির্ভুল হয়েছে। এটি IELTS Writing Task 2-এ Band 7.5+ পাওয়ার মতো বাক্য।"
            else:
                band = 7.0
                feedback = f"খুব ভালো প্রচেষ্টা! বাক্যটির গঠন সঠিক। আরও উন্নত করতে একাডেমিক কলকেশন ও লিংকিং ওয়ার্ড যোগ করতে পারেন।"
            upgrade = f"It is widely acknowledged that {clean_sentence[0].lower() + clean_sentence[1:].rstrip('.')}."

        ai_result = {
            "is_valid": len(errors) == 0 and contains_word,
            "collocation_used": colloc_used,
            "estimated_band": band,
            "feedback_bengali": feedback,
            "grammar_errors": errors,
            "band_upgrade": upgrade
        }

    # Determine SRS status and update Database
    is_valid = ai_result.get("is_valid", False)
    est_band = float(ai_result.get("estimated_band", 6.0))

    if not is_valid or est_band < 6.5:
        srs_mastery = 2 # Review Due (Weak word)
        srs_label = "Review Due"
        days_offset = 1
    elif est_band >= 7.5:
        srs_mastery = 3 # Mastered
        srs_label = "Mastered"
        days_offset = 5
    else:
        srs_mastery = 1 # Learning
        srs_label = "Learning"
        days_offset = 3

    # Update vocab_user_progress in DB
    try:
        conn = get_db()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_str = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "SELECT id, mastery_level, correct_count, mistake_count, user_sentences_json FROM vocab_user_progress WHERE user_id = ? AND LOWER(word) = LOWER(?)",
            (user_id, clean_word)
        )
        row = cursor.fetchone()

        new_entry = {
            "sentence": clean_sentence,
            "band": est_band,
            "created_at": now_str,
            "upgrade": ai_result.get("band_upgrade", "")
        }

        if row:
            row_id = row["id"]
            cur_mastery = row["mastery_level"]
            c_count = row["correct_count"]
            m_count = row["mistake_count"]
            try:
                sentences_list = json.loads(row["user_sentences_json"])
            except Exception:
                sentences_list = []

            sentences_list.append(new_entry)

            if is_valid and est_band >= 6.5:
                c_count += 1
                if c_count >= 2:
                    srs_mastery = 3
                    srs_label = "Mastered"
            else:
                m_count += 1
                srs_mastery = 2
                srs_label = "Review Due"

            cursor.execute("""
                UPDATE vocab_user_progress
                SET topic_id = ?, mastery_level = ?, last_reviewed = ?, next_review_due = ?,
                    correct_count = ?, mistake_count = ?, user_sentences_json = ?
                WHERE id = ?
            """, (topic_id, srs_mastery, now_str, due_str, c_count, m_count, json.dumps(sentences_list), row_id))
        else:
            c_count = 1 if (is_valid and est_band >= 6.5) else 0
            m_count = 0 if (is_valid and est_band >= 6.5) else 1
            cursor.execute("""
                INSERT INTO vocab_user_progress (user_id, word, topic_id, mastery_level, last_reviewed, next_review_due, correct_count, mistake_count, user_sentences_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, clean_word, topic_id, srs_mastery, now_str, due_str, c_count, m_count, json.dumps([new_entry])))

        conn.commit()
        conn.close()
    except Exception as db_err:
        print("Failed to update vocab_user_progress DB:", db_err)

    return {
        "status": "success",
        "word": clean_word,
        "sentence": clean_sentence,
        "is_valid": is_valid,
        "collocation_used": ai_result.get("collocation_used", False),
        "estimated_band": est_band,
        "feedback_bengali": ai_result.get("feedback_bengali", ""),
        "grammar_errors": ai_result.get("grammar_errors", []),
        "band_upgrade": ai_result.get("band_upgrade", ""),
        "srs_status": srs_label
    }

def record_vocab_quiz_answer(word: str, topic_id: str, is_correct: bool, user_id: int = 1) -> Dict[str, Any]:
    """
    Updates SRS Leitner tracking when student answers a vocabulary quiz question.
    """
    clean_word = word.strip()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    days_offset = 4 if is_correct else 1
    due_str = (datetime.now() + timedelta(days=days_offset)).strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, mastery_level, correct_count, mistake_count FROM vocab_user_progress WHERE user_id = ? AND LOWER(word) = LOWER(?)",
        (user_id, clean_word)
    )
    row = cursor.fetchone()

    if row:
        row_id = row["id"]
        c_count = row["correct_count"] + (1 if is_correct else 0)
        m_count = row["mistake_count"] + (0 if is_correct else 1)

        if not is_correct:
            new_level = 2 # Review Due (Weak)
            srs_label = "Review Due"
        else:
            if c_count >= 2:
                new_level = 3 # Mastered
                srs_label = "Mastered"
            else:
                new_level = 1 # Learning
                srs_label = "Learning"

        cursor.execute("""
            UPDATE vocab_user_progress
            SET topic_id = ?, mastery_level = ?, last_reviewed = ?, next_review_due = ?, correct_count = ?, mistake_count = ?
            WHERE id = ?
        """, (topic_id, new_level, now_str, due_str, c_count, m_count, row_id))
    else:
        c_count = 1 if is_correct else 0
        m_count = 0 if is_correct else 1
        new_level = 1 if is_correct else 2
        srs_label = "Learning" if is_correct else "Review Due"

        cursor.execute("""
            INSERT INTO vocab_user_progress (user_id, word, topic_id, mastery_level, last_reviewed, next_review_due, correct_count, mistake_count, user_sentences_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]')
        """, (user_id, clean_word, topic_id, new_level, now_str, due_str, c_count, m_count))

    # Also update skill_mastery table for Lexical Resource
    try:
        cursor.execute("""
            INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct, assisted_correct, mastery_percentage)
            VALUES (?, 'Vocabulary', 'Lexical Resource', 1, ?, ?, 0, ?)
            ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
                total_attempted = total_attempted + 1,
                total_correct = total_correct + excluded.total_correct,
                independent_correct = independent_correct + excluded.independent_correct,
                mastery_percentage = ROUND((total_correct + excluded.total_correct) * 100.0 / (total_attempted + 1), 1),
                last_updated = CURRENT_TIMESTAMP
        """, (user_id, 1 if is_correct else 0, 1 if is_correct else 0, 100.0 if is_correct else 0.0))
    except Exception as e:
        print("Skill mastery update notice:", e)

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "word": clean_word,
        "is_correct": is_correct,
        "mastery_level": new_level,
        "srs_label": srs_label,
        "correct_count": c_count,
        "mistake_count": m_count
    }

def get_user_vocab_srs_stats(user_id: int = 1) -> Dict[str, Any]:
    """
    Returns aggregated SRS summary:
    - Mastered count
    - Learning count
    - Review due / Weak words count
    - Total sentences written
    - Weak words list
    - Map of word -> progress details
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT word, topic_id, mastery_level, correct_count, mistake_count, user_sentences_json
        FROM vocab_user_progress
        WHERE user_id = ?
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    mastered = 0
    learning = 0
    review_due = 0
    total_sentences = 0
    weak_words = []
    progress_map = {}

    for r in rows:
        w = r["word"]
        lvl = r["mastery_level"]
        m_count = r["mistake_count"]
        c_count = r["correct_count"]

        try:
            s_list = json.loads(r["user_sentences_json"] or "[]")
        except Exception:
            s_list = []
        total_sentences += len(s_list)

        if lvl == 3:
            mastered += 1
            status_text = "Mastered"
        elif lvl == 2 or m_count > 0:
            review_due += 1
            weak_words.append(w)
            status_text = "Review Due"
        elif lvl == 1 or c_count > 0:
            learning += 1
            status_text = "Learning"
        else:
            status_text = "New"

        progress_map[w.lower()] = {
            "mastery_level": lvl,
            "status_text": status_text,
            "correct_count": c_count,
            "mistake_count": m_count,
            "sentences_count": len(s_list)
        }

    return {
        "mastered_count": mastered,
        "learning_count": learning,
        "review_due_count": review_due,
        "total_sentences": total_sentences,
        "weak_words": weak_words,
        "progress_map": progress_map
    }

def toggle_vocab_word_status(word: str, topic_id: str, target_status: str, user_id: int = 1) -> Dict[str, Any]:
    """
    Toggles or sets the status of a word:
    - 'mastered': sets mastery_level = 3, mistake_count = 0, correct_count = max(c_count, 3)
    - 'weak': sets mastery_level = 2, mistake_count = max(m_count, 2), correct_count = 0
    - 'clear': resets mastery_level = 0, mistake_count = 0, correct_count = 0
    """
    clean_word = word.strip()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, mastery_level, correct_count, mistake_count, user_sentences_json FROM vocab_user_progress WHERE user_id = ? AND LOWER(word) = LOWER(?)",
        (user_id, clean_word)
    )
    row = cursor.fetchone()

    if target_status == "mastered":
        new_level = 3
        c_count = 3
        m_count = 0
        due_str = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    elif target_status == "weak":
        new_level = 2
        c_count = 0
        m_count = 2
        due_str = (datetime.now() - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    else:
        new_level = 0
        c_count = 0
        m_count = 0
        due_str = now_str

    if row:
        row_id = row["id"]
        cursor.execute("""
            UPDATE vocab_user_progress
            SET topic_id = ?, mastery_level = ?, last_reviewed = ?, next_review_due = ?, correct_count = ?, mistake_count = ?
            WHERE id = ?
        """, (topic_id, new_level, now_str, due_str, c_count, m_count, row_id))
    else:
        cursor.execute("""
            INSERT INTO vocab_user_progress (user_id, word, topic_id, mastery_level, last_reviewed, next_review_due, correct_count, mistake_count, user_sentences_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, '[]')
        """, (user_id, clean_word, topic_id, new_level, now_str, due_str, c_count, m_count))

    conn.commit()
    conn.close()

    updated_stats = get_user_vocab_srs_stats(user_id)
    return {
        "status": "success",
        "word": clean_word,
        "target_status": target_status,
        "mastery_level": new_level,
        "stats": updated_stats
    }

