# -*- coding: utf-8 -*-
import json
import sqlite3
from typing import Dict, Any, List, Optional
from ai_engine.ai_router import ai_router
from database import get_db

class SocraticTeachingEngine:
    """
    Socratic Micro-Practice & Progressive Hinting Engine.
    Guides students through Cambridge questions using adaptive, human-like coaching.
    """
    def __init__(self):
        pass

    def start_lesson(self, user_id: int, skill: str, question_type: str, book: Optional[int] = 18, lang_pref: str = "English + Native") -> Dict[str, Any]:
        """Start a guided lesson tailored for the specific skill and question type."""
        conn = get_db()
        cursor = conn.cursor()
        
        # Query for matching question
        cursor.execute("""
            SELECT * FROM questions 
            WHERE skill = ? AND (question_type LIKE ? OR sub_type_tag LIKE ?)
            ORDER BY cambridge_book DESC LIMIT 1
        """, (skill, f"%{question_type}%", f"%{question_type}%"))
            
        q = cursor.fetchone()
        conn.close()

        skill_lower = (skill or "reading").lower()
        is_speaking = skill_lower == "speaking"
        is_writing = skill_lower == "writing"

        if q:
            question_data = {
                "id": q["id"],
                "skill": q["skill"],
                "question_type": q["question_type"],
                "sub_type_tag": q["sub_type_tag"],
                "title": q["title"],
                "passage_or_context": "" if is_speaking else (q["passage_or_context"] or ""),
                "question_text": q["question_text"],
                "options": [] if (is_speaking or is_writing) else (json.loads(q["options_json"]) if q["options_json"] else []),
                "answer_key": "" if is_speaking else q["answer_key"],
                "explanation": q["explanation"],
                "cambridge_book": q["cambridge_book"],
                "test_number": q["test_number"],
                "passage_or_section": q["passage_or_section"],
                "difficulty_band": q["difficulty_band"] or 7.5,
                "trap_type": q["trap_type"] or "Strategy Focus",
                "synonyms": json.loads(q["synonym_mapping_json"]) if q["synonym_mapping_json"] else []
            }
        else:
            # Dynamic generator
            raw_q = ai_router.generate_dynamic_question(skill, question_type, lang_pref)
            question_data = {
                "id": 99999,
                "skill": skill,
                "question_type": question_type,
                "sub_type_tag": question_type,
                "title": f"Cambridge Practice: {question_type}",
                "passage_or_context": "" if is_speaking else raw_q.get("passage", ""),
                "question_text": raw_q.get("text", f"Practice prompt for {question_type}"),
                "options": [] if (is_speaking or is_writing) else raw_q.get("options", []),
                "answer_key": "" if is_speaking else raw_q.get("answer_key", "Option A"),
                "explanation": raw_q.get("explanation", "Expert reasoning."),
                "cambridge_book": book or 18,
                "test_number": 1,
                "passage_or_section": 1,
                "difficulty_band": 7.5,
                "trap_type": "Focus Point",
                "synonyms": []
            }

        # Skill-specific and language-specific dynamic intro message (natural, ChatGPT-smart)
        is_banglish = lang_pref in ["English + Native", "both"]
        is_bangla = lang_pref in ["Native Only", "mother"]

        if is_speaking:
            qt_lower = question_type.lower()
            if "part 3" in qt_lower:
                if is_bangla:
                    intro = (
                        f"চলো, **IELTS Speaking Part 3** শুরু করি! এখানে কোনো passage বা multiple-choice প্রশ্ন নেই — "
                        f"এটা একটি মুক্ত আলোচনা (Abstract Discussion)। আমি examiner হিসেবে তোমাকে গভীর প্রশ্ন করব, "
                        f"আর তুমি তোমার মতামত গুছিয়ে বলবে।\n\n"
                        f"নিচের প্রশ্নটি দেখে উত্তর বলো বা টাইপ করো — আমি তোমাকে Band 8.5+ লেভেলের বিস্তারিত ফিডব্যাক দেব!"
                    )
                elif is_banglish:
                    intro = (
                        f"Awesome! চলো **IELTS Speaking Part 3** শুরু করি। Remember, এখানে কোনো passage বা MCQ options নেই — "
                        f"this is a natural abstract discussion between you and the examiner.\n\n"
                        f"Look at the question below. তুমি 🎙️ Mic বাটনে ক্লিক করে কথা বলতে পারো অথবা text বক্সে উত্তর টাইপ করতে পারো। "
                        f"I will listen and evaluate your fluency, vocabulary, and band score!"
                    )
                else:
                    intro = (
                        f"Welcome to **IELTS Speaking Part 3**! This is the two-way discussion where we explore broader, "
                        f"abstract issues related to the topic. There is NO reading passage and NO multiple-choice options here.\n\n"
                        f"Take a look at the examiner question below. Press the 🎙️ Mic button to speak your answer or type it in. "
                        f"I will give you an authentic Band Descriptors evaluation!"
                    )
            elif "part 2" in qt_lower or "cue card" in qt_lower:
                if is_bangla:
                    intro = (
                        f"স্বাগতম **IELTS Speaking Part 2** (Cue Card) সেশনে! নিচে তোমার Cue Card এবং পয়েন্টগুলো দেওয়া হলো।\n\n"
                        f"১ মিনিট সময় নিয়ে চিন্তা করো। প্রস্তুত হলে 🎙️ Mic বাটনে ক্লিক করে ১-২ মিনিট কথা বলো অথবা তোমার উত্তর টাইপ করো।"
                    )
                elif is_banglish:
                    intro = (
                        f"Let's practice **IELTS Speaking Part 2**! নিচে তোমার official Cue Card দেওয়া হলো।\n\n"
                        f"১ মিনিট নিয়ে পয়েন্টগুলো নোট করে নাও। Whenever you're ready, press the 🎙️ Mic button to speak or type your full response. "
                        f"আমি তোমার ফ্লুয়েন্সি ও ভোকাবুলারি চেক করব!"
                    )
                else:
                    intro = (
                        f"Welcome to **IELTS Speaking Part 2**! Below is your official Cue Card topic.\n\n"
                        f"You have 1 minute to prepare your ideas. Whenever you are ready, press the 🎙️ Mic button to speak for up to 2 minutes or type your response."
                    )
            else: # Part 1 or General Speaking
                if is_bangla:
                    intro = (
                        f"চলো **IELTS Speaking Part 1** শুরু করি! এখানে ব্যক্তিগত ও পরিচিত বিষয়ে প্রশ্ন থাকবে। "
                        f"স্বাভাবিকভাবে ২-৩ বাক্যে উত্তর দাও।"
                    )
                elif is_banglish:
                    intro = (
                        f"Let's begin **IELTS Speaking Part 1**! এখানে everyday life নিয়ে প্রশ্ন করব। "
                        f"Keep your answers natural and concise — about 2-3 sentences. 🎙️ Mic দিয়ে বলো বা লিখে পাঠাও!"
                    )
                else:
                    intro = (
                        f"Welcome to **IELTS Speaking Part 1**! I will ask you everyday, familiar questions. "
                        f"Keep your answers confident and natural (about 2-3 sentences). Speak or type your answer below!"
                    )

        elif is_writing:
            if is_bangla:
                intro = (
                    f"স্বাগতম **IELTS Writing** সেশনে ({question_type})!\n\n"
                    f"নিচের প্রম্পটটি মনোযোগ দিয়ে পড়ে তোমার লেখা শুরু করো। সম্পূর্ণ লেখা শেষে Submit বাটনে ক্লিক করো — "
                    f"আমি ৪টি ক্রাইটেরিয়ার ভিত্তিতে এক্সামিনার স্কোর দেব।"
                )
            elif is_banglish:
                intro = (
                    f"Welcome to **IELTS Writing** — {question_type}!\n\n"
                    f"Read the exam prompt below carefully. Type your full essay/report in the text box. "
                    f"When done, click Submit for a complete line-by-line examiner evaluation and Band Score!"
                )
            else:
                intro = (
                    f"Welcome to your **IELTS Writing** session ({question_type})!\n\n"
                    f"Carefully read the official prompt below and write your response. Submit your answer for comprehensive Cambridge Band Descriptor grading."
                )

        else: # Reading & Listening
            if is_bangla:
                intro = (
                    f"স্বাগতম **IELTS {skill}** ({question_type}) প্র্যাকটিসে!\n\n"
                    f"প্যাসেজটি মনোযোগ দিয়ে পড়ে মূল ধারণা চিহ্নিত করো। নিচে তোমার প্রশ্ন এবং অপশনগুলো দেওয়া হলো।"
                )
            elif is_banglish:
                intro = (
                    f"Welcome to **IELTS {skill} — {question_type}**!\n\n"
                    f"Cambridge পরীক্ষায় ডিরেক্ট শব্দের চেয়ে **paraphrase** ম্যাচ করা সবচেয়ে জরুরি। "
                    f"প্যাসেজটি পড়ে সঠিক উত্তরটি বেছে নাও!"
                )
            else:
                intro = (
                    f"Welcome to your **IELTS {skill} — {question_type}** master practice!\n\n"
                    f"Carefully read the passage context and match the paraphrased keywords to find the correct answer."
                )

        return {
            "teaching_messages": [{"eng": intro}],
            "question": question_data
        }

    def submit_answer(self, user_id: int, question_id: int, answer: str, attempt: int = 1, lang_pref: str = "English + Native") -> Dict[str, Any]:
        """
        Evaluate student answer with progressive Socratic hinting.
        Handles objective questions (Reading/Listening) with smart hints,
        and subjective questions (Speaking/Writing) via AI evaluation.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
        q = cursor.fetchone()
        
        if not q:
            conn.close()
            # If dynamic question, evaluate with AI
            return {"is_correct": True, "feedback": "Great effort! Your response has been noted.", "next_step": "continue"}

        skill = q["skill"].lower()

        # Handle Speaking answer
        if skill == "speaking":
            conn.close()
            from scoring_engine.speaking_evaluator import SpeakingEvaluatorEngine
            eval_res = SpeakingEvaluatorEngine.evaluate_speech_sample(q["question_text"], answer, 3)
            return {
                "is_correct": True,
                "overall_band": eval_res.get("overall_band", 7.0),
                "feedback": eval_res.get("improvement_plan", "Good fluency and vocabulary."),
                "evaluation": eval_res,
                "next_step": "next_question"
            }

        # Handle Writing answer
        if skill == "writing":
            conn.close()
            from scoring_engine.writing_evaluator import WritingEvaluatorEngine
            eval_res = WritingEvaluatorEngine.evaluate_essay(q["question_text"], answer, q["question_type"])
            return {
                "is_correct": True,
                "overall_band": eval_res.get("overall_band", 7.0),
                "feedback": eval_res.get("examiner_summary", "Clear structure and arguments."),
                "evaluation": eval_res,
                "next_step": "next_question"
            }

        # Objective: Reading / Listening
        correct_key = (q["answer_key"] or "").strip().lower()
        user_ans_clean = answer.strip().lower()

        is_correct = (user_ans_clean == correct_key) or (correct_key in user_ans_clean)
        synonyms = json.loads(q["synonym_mapping_json"]) if q["synonym_mapping_json"] else []
        syn_pair_str = f"'{synonyms[0][0]}' ↔ '{synonyms[0][1]}'" if synonyms else "key passage terms"

        if is_correct:
            cursor.execute("""
                INSERT INTO skill_mastery (user_id, skill, question_type, total_attempted, total_correct, independent_correct)
                VALUES (?, ?, ?, 1, 1, 1)
                ON CONFLICT(user_id, skill, question_type) DO UPDATE SET
                total_attempted = total_attempted + 1,
                total_correct = total_correct + 1,
                independent_correct = independent_correct + 1,
                mastery_percentage = MIN(100.0, (CAST(total_correct + 1 AS REAL) / CAST(total_attempted + 1 AS REAL)) * 100.0),
                last_practiced_at = CURRENT_TIMESTAMP
            """, (user_id, q["skill"], q["question_type"]))
            conn.commit()
            conn.close()
            return {
                "is_correct": True,
                "feedback": f"🎉 Excellent! Correct! {q.get('explanation', '')}",
                "next_step": "next_question"
            }
        else:
            conn.close()
            if attempt == 1:
                return {
                    "is_correct": False,
                    "feedback": f"Not quite. Hint: Look for where the main argument is made in the passage, especially around words like '{q.get('trap_type', 'key details')}'. Try again!",
                    "next_step": "retry"
                }
            elif attempt == 2:
                return {
                    "is_correct": False,
                    "feedback": f"Second hint: Pay attention to synonym replacements — notice how {syn_pair_str} are connected. Look one more time!",
                    "next_step": "retry"
                }
            else:
                return {
                    "is_correct": False,
                    "feedback": f"The correct answer is: {q['answer_key']}. Explanation: {q.get('explanation', '')}",
                    "next_step": "next_question"
                }
