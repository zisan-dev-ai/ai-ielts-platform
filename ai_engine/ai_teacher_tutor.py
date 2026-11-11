# -*- coding: utf-8 -*-
import json
import sqlite3
from typing import Dict, Any, List, Optional
from ai_engine.ai_router import ai_router
from database import get_db

class AITeacherTutorEngine:
    """
    World-Class AI IELTS Teacher & Master Tutor Engine
    Modeled after Cambridge Senior Examiners and elite IELTS pedagogy.
    Integrates Cambridge 1 to 21 Question Taxonomy, Socratic Hinting, 
    Distractor Deconstruction, and Banglish/English Code-Switching.
    """
    def __init__(self):
        pass

    def get_cambridge_tier(self, book_number: int) -> Dict[str, Any]:
        """Classify Cambridge Book into pedagogical progression tiers."""
        if book_number <= 10:
            return {
                "tier": 1,
                "name": "Foundational Era (Books 1–10)",
                "focus": "Core Question Mechanics, Baseline Grammar & Direct Synonym Paraphrasing."
            }
        elif book_number <= 15:
            return {
                "tier": 2,
                "name": "Modern Standard Era (Books 11–15)",
                "focus": "Sophisticated Distractors, Complex Chart/Map Data & Paraphrase Filtering."
            }
        else:
            return {
                "tier": 3,
                "name": "Peak Exam Standard (Books 16–21)",
                "focus": "Fast Audio Tempo, High Lexical Density & Multi-layered Logic Traps."
            }

    def generate_strategy_blueprint(self, skill: str, question_type: str, book_number: int = 18, lang_pref: str = "English + Native") -> str:
        """
        Generate Band 9 Strategy Blueprint inspired by top Cambridge examiners.
        """
        tier_info = self.get_cambridge_tier(book_number)
        
        system_instruction = (
            "You are a Senior Cambridge IELTS Examiner and Master AI Tutor. "
            "Explain how to master this specific Cambridge question type. "
            "Format with Markdown: # Title, ## Band 9 Rules, ## Cambridge Trap Avoidance, ## Top Synonym Pairs. "
            "Strict Language Preference: " + lang_pref
        )

        prompt = (
            f"Skill: {skill}\n"
            f"Question Type: {question_type}\n"
            f"Target Cambridge Book Tier: Cambridge {book_number} ({tier_info['name']})\n"
            f"Pedagogical Focus: {tier_info['focus']}\n\n"
            f"Provide a clear, engaging, world-class teaching blueprint."
        )

        try:
            cred = ai_router.adapters["gemini"]
            # Fallback to AI router generate
            return ai_router.generate_dynamic_question(skill, question_type, lang_pref).get("passage_text", "")
        except Exception as e:
            return f"### 📌 BAND 9 STRATEGY BLUEPRINT: {skill} — {question_type} (Cambridge {book_number})\n\n" \
                   f"**Tier**: {tier_info['name']}\n" \
                   f"**Core Focus**: {tier_info['focus']}\n\n" \
                   f"1. **Identify Core Keywords**: Spot un-paraphrasable nouns and main verbs.\n" \
                   f"2. **Deconstruct Traps**: Watch for extreme qualifiers (*always, only, never*) and word-spotting tricks.\n" \
                   f"3. **Match Synonyms**: Align passage evidence with question wording."

    def get_cambridge_questions(self, skill: str, book: Optional[int] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch indexed Cambridge 1 to 21 questions from database."""
        conn = get_db()
        cursor = conn.cursor()
        
        if book:
            cursor.execute("""
                SELECT id, skill, question_type, sub_type_tag, title, passage_or_context, 
                       question_text, options_json, answer_key, explanation, 
                       cambridge_book, test_number, passage_or_section, difficulty_band, trap_type, synonym_mapping_json
                FROM questions
                WHERE skill = ? AND cambridge_book = ?
                LIMIT ?
            """, (skill, book, limit))
        else:
            cursor.execute("""
                SELECT id, skill, question_type, sub_type_tag, title, passage_or_context, 
                       question_text, options_json, answer_key, explanation, 
                       cambridge_book, test_number, passage_or_section, difficulty_band, trap_type, synonym_mapping_json
                FROM questions
                WHERE skill = ?
                ORDER BY cambridge_book DESC, test_number ASC
                LIMIT ?
            """, (skill, limit))
            
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "skill": r["skill"],
                "question_type": r["question_type"],
                "sub_type_tag": r["sub_type_tag"],
                "title": r["title"],
                "passage_or_context": r["passage_or_context"],
                "question_text": r["question_text"],
                "options": json.loads(r["options_json"]) if r["options_json"] else [],
                "answer_key": r["answer_key"],
                "explanation": r["explanation"],
                "cambridge_book": r["cambridge_book"],
                "test_number": r["test_number"],
                "passage_or_section": r["passage_or_section"],
                "difficulty_band": r["difficulty_band"],
                "trap_type": r["trap_type"],
                "synonyms": json.loads(r["synonym_mapping_json"]) if r["synonym_mapping_json"] else []
            })
        return result

    def teach_interactive_session(self, user_id: int, user_message: str, current_skill: str = "Reading", conversation_history: List[Dict[str, str]] = [], lang_pref: str = "English + Native") -> str:
        """
        Conduct an ongoing conversational teaching session with code-switching support.
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT mother_language, teacher_language_pref, target_band FROM profiles WHERE user_id = ?", (user_id,))
        prof = cursor.fetchone()
        conn.close()
        
        actual_lang_pref = prof["teacher_language_pref"] if prof and prof["teacher_language_pref"] else lang_pref
        target_band = float(prof["target_band"]) if prof and prof["target_band"] else 7.5

        # Delegate conversational teaching to ai_router
        return ai_router.teacher_conversation(
            user_message=user_message,
            conversation_history=conversation_history,
            current_skill=current_skill,
            user_preference=actual_lang_pref,
            target_band=target_band
        )

ai_teacher = AITeacherTutorEngine()
