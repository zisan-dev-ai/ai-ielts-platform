# -*- coding: utf-8 -*-
import sqlite3
import json
from typing import Dict, Any, List, Optional
from database import get_db
from ai_engine.health_checker import KeyPoolHealthChecker
from ai_engine.gemini_adapter import GeminiAdapter

class GrammarVocabEngine:
    def __init__(self):
        self.gemini_adapter = GeminiAdapter()

    def _get_key_pool(self, provider_id: str) -> List[str]:
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("SELECT api_key FROM ai_credentials WHERE provider_id = ? AND status = 'Active' ORDER BY id ASC", (provider_id,))
            rows = cursor.fetchall()
            conn.close()
            return [r["api_key"] for r in rows if r["api_key"]]
        except Exception:
            return []

    def get_skill_map(self, user_id: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        conn = get_db()
        cursor = conn.cursor()

        # Fetch all baseline rules
        cursor.execute("SELECT * FROM grammar_rules ORDER BY id ASC")
        rules = [dict(r) for r in cursor.fetchall()]

        # Fetch student mastery data
        cursor.execute("SELECT * FROM student_grammar_vocab_mastery WHERE user_id = ? AND item_type = 'grammar'", (user_id,))
        mastery_rows = {r["topic_or_word"]: dict(r) for r in cursor.fetchall()}

        conn.close()

        skill_map: Dict[str, List[Dict[str, Any]]] = {
            "Foundational (Band 5.0-6.0)": [],
            "Intermediate (Band 6.5-7.0)": [],
            "Advanced Master (Band 7.5-9.0)": []
        }

        for rule in rules:
            tier = rule.get("level_tier", "Foundational (Band 5.0-6.0)")
            topic = rule.get("topic_name", "General Rule")
            m = mastery_rows.get(topic, {})

            item_data = {
                "rule_id": rule["id"],
                "topic_or_word": topic,
                "rule_description": rule["rule_description"],
                "common_error": rule["common_error"],
                "correct_example": rule["correct_example"],
                "cambridge_tip": rule.get("cambridge_tip", ""),
                "mastery_stage": m.get("mastery_stage", "Needs Practice"),
                "passive_mastery_pct": m.get("passive_mastery_pct", 50.0),
                "active_mastery_pct": m.get("active_mastery_pct", 30.0)
            }

            if tier in skill_map:
                skill_map[tier].append(item_data)
            else:
                skill_map["Foundational (Band 5.0-6.0)"].append(item_data)

        return skill_map

    def get_error_alerts(self, user_id: int = 1) -> List[Dict[str, Any]]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grammar_error_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (user_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    def generate_exercise(self, topic_or_word: str, user_id: int = 1) -> Dict[str, Any]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grammar_rules WHERE topic_name = ?", (topic_or_word,))
        rule = cursor.fetchone()
        conn.close()

        rule_desc = rule["rule_description"] if rule else "Grammar precision rule."
        common_err = rule["common_error"] if rule else "Incorrect sentence structure."
        correct_ex = rule["correct_example"] if rule else "Correct sentence."

        # Try generating dynamic exercise via Gemini AI if available
        cred = KeyPoolHealthChecker.get_active_credential("gemini")
        if cred:
            system_inst = (
                "You are a Senior Cambridge IELTS Tutor. Generate a 4-step progressive learning lesson.\n"
                "Return ONLY valid JSON with keys:\n"
                "{\n"
                "  \"rule\": \"Clear, step-by-step grammar rule in simple English\",\n"
                "  \"rule_bengali\": \"বাংলায় সহজ ব্যাখ্যাসহ নিয়মটি\",\n"
                "  \"incorrect_example\": \"❌ Incorrect sentence showing the mistake\",\n"
                "  \"correct_example\": \"✅ Correct sentence showing proper usage\",\n"
                "  \"easy_practice\": {\n"
                "     \"question\": \"Simple warm-up sentence with blank (___)\",\n"
                "     \"options\": [\"Option A\", \"Option B\"],\n"
                "     \"correct_option\": \"Option A\",\n"
                "     \"explanation\": \"Easy practice explanation\"\n"
                "  },\n"
                "  \"main_drill\": {\n"
                "     \"question_text\": \"Full Cambridge Band 7.5+ Exam Drill Question\",\n"
                "     \"options\": [\"Option A: ...\", \"Option B: ...\", \"Option C: ...\", \"Option D: ...\"],\n"
                "     \"correct_option\": \"Option A\",\n"
                "     \"explanation\": \"Deep IELTS explanation & distractor trap breakdown\"\n"
                "  }\n"
                "}"
            )
            prompt = f"Topic: {topic_or_word}\nRule: {rule_desc}\nCommon Error: {common_err}\nCorrect Example: {correct_ex}"
            try:
                raw = self.gemini_adapter.generate_text(prompt, cred["api_key"], system_instruction=system_inst, api_key_pool=self._get_key_pool('gemini'))
                clean = raw.replace("```json", "").replace("```", "").strip()
                return json.loads(clean)
            except Exception as e:
                print("Error generating exercise via AI:", e)

        # Procedural fallback exercise
        return {
            "rule": rule_desc,
            "rule_bengali": f"{topic_or_word} এর সঠিক নিয়ম অনুসরণ করে বাক্য গঠন করতে হয়।",
            "incorrect_example": f"❌ {common_err}",
            "correct_example": f"✅ {correct_ex}",
            "easy_practice": {
                "question": f"Easy Warm-up: Choose the correct verb form for {topic_or_word}.",
                "options": [f"Option A: {correct_ex[:30]}...", f"Option B: {common_err[:30]}..."],
                "correct_option": f"Option A: {correct_ex[:30]}...",
                "explanation": "Great start! Option A correctly applies the basic rule."
            },
            "main_drill": {
                "question_text": f"Main Exam Drill: Which sentence demonstrates Band 8.0+ precision for {topic_or_word}?",
                "options": [
                    f"Option A: {correct_ex}",
                    f"Option B: {common_err}",
                    f"Option C: Informal phrase violating {topic_or_word} rules.",
                    f"Option D: Misplaced clause structure."
                ],
                "correct_option": f"Option A: {correct_ex}",
                "explanation": f"Option A is correct according to the rule: '{rule_desc}'."
            }
        }

    def evaluate_submission(self, user_id: int, topic: str, is_correct: bool) -> Dict[str, Any]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_grammar_vocab_mastery WHERE user_id = ? AND topic_or_word = ?", (user_id, topic))
        row = cursor.fetchone()

        if row:
            curr_active = row["active_mastery_pct"]
            curr_passive = row["passive_mastery_pct"]
            new_active = min(100.0, curr_active + 10.0) if is_correct else max(0.0, curr_active - 5.0)
            new_passive = min(100.0, curr_passive + 5.0) if is_correct else curr_passive

            if new_active >= 80:
                stage = "Mastered"
            elif new_active >= 60:
                stage = "Contextualized"
            elif new_active >= 40:
                stage = "Understood"
            else:
                stage = "Recognized"

            cursor.execute("""
                UPDATE student_grammar_vocab_mastery
                SET active_mastery_pct = ?, passive_mastery_pct = ?, mastery_stage = ?
                WHERE user_id = ? AND topic_or_word = ?
            """, (new_active, new_passive, stage, user_id, topic))
        else:
            new_active = 60.0 if is_correct else 30.0
            stage = "Contextualized" if is_correct else "Recognized"
            cursor.execute("""
                INSERT INTO student_grammar_vocab_mastery (user_id, item_type, topic_or_word, category, mastery_stage, passive_mastery_pct, active_mastery_pct)
                VALUES (?, 'grammar', ?, 'General', ?, 70.0, ?)
            """, (user_id, topic, stage, new_active))

        conn.commit()
    def generate_more_questions(self, skill: str, topic: str, count: int = 3, existing_count: int = 0) -> List[Dict[str, Any]]:
        # 1. Try AI Router for dynamic, tailored questions across any provider
        system_inst = (
            f"You are a Senior Cambridge IELTS Tutor. The student is practicing '{topic}' ({skill}).\n"
            f"Generate {count} distinct multiple-choice practice questions specifically testing this topic.\n"
            "Return ONLY a JSON array of objects with keys:\n"
            "[\n"
            "  {\n"
            "    \"id\": \"dyn_1\",\n"
            "    \"question\": \"Sentence with blank (___) or error spotting instruction\",\n"
            "    \"options\": [\"Option A\", \"Option B\", \"Option C\", \"Option D\"],\n"
            "    \"answer\": \"Option A\",\n"
            "    \"explanation\": \"Clear, encouraging explanation in simple English and Bengali\"\n"
            "  }\n"
            "]"
        )
        prompt = f"Topic: {topic}, Module: {skill}. Generate {count} fresh multiple-choice practice questions."
        try:
            from ai_engine.ai_router import ai_router
            raw = ai_router.generate_text(prompt, system_instruction=system_inst)
            clean = raw.replace("```json", "").replace("```", "").strip()
            items = json.loads(clean)
            if isinstance(items, list) and len(items) > 0:
                for idx, it in enumerate(items):
                    it["id"] = f"dyn_{existing_count + idx + 1}"
                return items
        except Exception as e:
            print("Error generating dynamic practice questions via AI Router:", e)

        # 2. Dynamic high-quality procedural fallback generator
        fallback = []
        for i in range(1, count + 1):
            num = existing_count + i
            if skill.lower() == "grammar":
                fallback.append({
                    "id": f"dyn_{num}",
                    "question": f"Practice Drill #{num}: Which option demonstrates accurate application of '{topic}' in an IELTS sentence?",
                    "options": [
                        f"Sentence demonstrating standard, accurate {topic} usage.",
                        f"Sentence containing a common {topic} trap.",
                        f"Sentence with misplaced clauses or modifiers.",
                        f"Sentence violating standard academic register."
                    ],
                    "answer": f"Sentence demonstrating standard, accurate {topic} usage.",
                    "explanation": f"সঠিক উত্তর: প্রথম অপশনটি {topic}-এর নিয়মানুযায়ী শতভাগ নির্ভুল।"
                })
            else:
                fallback.append({
                    "id": f"dyn_{num}",
                    "question": f"Vocabulary Drill #{num}: Which term or collocation provides the most natural Band 8+ academic lexical resource for '{topic}'?",
                    "options": [
                        f"Band 8.5+ Academic Collocation for {topic}",
                        f"Informal / basic conversational synonym",
                        f"Inappropriate or awkward word choice",
                        f"Grammatically mismatched phrase"
                    ],
                    "answer": f"Band 8.5+ Academic Collocation for {topic}",
                    "explanation": f"সঠিক উত্তর: প্রথম অপশনটি {topic} থিমের জন্য সর্বোচ্চ মানের অ্যাকাডেমিক কলোকেশন।"
                })
        return fallback

    def generate_more_exam_challenges(self, topic: str, count: int = 3, existing_count: int = 0) -> Dict[str, Any]:
        """Generates authentic Cambridge IELTS GRA Band 8.5+ error correction / sentence upgrade challenges via AI."""
        system_inst = (
            f"You are a Senior Cambridge IELTS Examiner assessing Grammatical Range & Accuracy (GRA) for Band 8.5-9.0.\n"
            f"The grammar topic being tested is '{topic}'.\n"
            f"Generate a realistic Academic Writing Task 2 or Task 1 essay passage (2-3 sentences) demonstrating common IELTS candidate errors or advanced syntactic structures for '{topic}'.\n"
            f"Then create {count} challenging multiple-choice correction or enhancement tasks.\n"
            "Return ONLY a JSON object with this exact structure:\n"
            "{\n"
            f"  \"title\": \"Academic Task 2 Band 8.5 GRA Challenge ({topic})\",\n"
            "  \"passage\": \"2-3 sentence authentic academic passage with subtle errors or advanced grammar targets.\",\n"
            "  \"questions\": [\n"
            "    {\n"
            "      \"id\": \"exam_dyn_1\",\n"
            "      \"label\": \"Correction / Upgrade (Line X): 'Target phrase in passage'\",\n"
            "      \"options\": [\"Option A (Band 8.5 Accurate)\", \"Option B (Common Candidate Error)\", \"Option C (Grammar Trap)\"],\n"
            "      \"answer\": \"Option A (Band 8.5 Accurate)\",\n"
            "      \"explanation\": \"Examiner explanation in English and Bengali explaining why this option achieves Band 8.5+ Grammatical Range and Accuracy.\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )
        prompt = f"Topic: {topic}. Generate {count} rigorous IELTS Academic Exam Challenge questions with an academic passage context."

        try:
            from ai_engine.ai_router import ai_router
            data = ai_router.generate_json(prompt, system_instruction=system_inst)
            if isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list) and len(data["questions"]) > 0:
                for idx, q in enumerate(data["questions"]):
                    q["id"] = f"exam_dyn_{existing_count + idx + 1}"
                return data
        except Exception as e:
            print("Error generating dynamic exam challenges via AI Router:", e)

        # Procedural fallback if AI providers are unreachable
        fallback_questions = []
        for i in range(1, count + 1):
            num = existing_count + i
            fallback_questions.append({
                "id": f"exam_dyn_{num}",
                "label": f"Correction {num} (Task 2 GRA): Identify the Band 8.5+ accurate structure for '{topic}'",
                "options": [
                    f"Evidence clearly indicates that key variables in this {topic} pattern demonstrate consistent correlation.",
                    f"Evidence clearly indicate that key variables in this {topic} pattern demonstrates consistent correlation.",
                    f"Evidence clearly indicating that key variables in this {topic} pattern to demonstrate consistent correlation."
                ],
                "answer": f"Evidence clearly indicates that key variables in this {topic} pattern demonstrate consistent correlation.",
                "explanation": f"ব্যান্ড ৮.৫ মানদণ্ড: '{topic}'-এর সূক্ষ্ম নিয়ম ও অ্যাকাডেমিক বাক্যের সাবজেক্ট-ভার্ব নির্ভুলভাবে মেলাতে হবে।"
            })

        return {
            "title": f"Academic Task 2 Band 8.5 Challenge ({topic})",
            "passage": f"Recent empirical investigations into global developments demonstrate that various interrelated factors require careful analysis. A significant body of research indicates that strategic implementations yield substantial benefits.",
            "questions": fallback_questions
        }

    def generate_more_vocab_exam_challenges(self, topic: str, count: int = 3, existing_count: int = 0) -> Dict[str, Any]:
        """Generates authentic Cambridge IELTS Lexical Resource (LR) Band 8.5+ academic paraphrasing & vocabulary upgrade challenges via AI."""
        system_inst = (
            f"You are a Senior Cambridge IELTS Examiner assessing Lexical Resource (LR) for Band 8.5-9.0.\n"
            f"The academic vocabulary topic being tested is '{topic}'.\n"
            f"Generate a realistic student draft paragraph (2-3 sentences) written in basic or repetitive English (Band 5.5-6.0) about '{topic}'.\n"
            f"Then create {count} challenging multiple-choice questions asking candidate to replace informal or repetitive phrases with sophisticated academic C1/C2 collocations.\n"
            "Return ONLY a JSON object with this exact structure:\n"
            "{\n"
            f"  \"title\": \"Academic Lexical Upgrade Challenge ({topic})\",\n"
            "  \"passage\": \"2-3 sentence student draft in basic English needing C1/C2 lexical upgrade.\",\n"
            "  \"questions\": [\n"
            "    {\n"
            "      \"id\": \"v_exam_dyn_1\",\n"
            "      \"label\": \"Best Academic Upgrade for 'target basic phrase':\",\n"
            "      \"options\": [\"Option A (Band 8.5 Academic)\", \"Option B (Informal / Weak)\", \"Option C (Inaccurate Collocation)\"],\n"
            "      \"answer\": \"Option A (Band 8.5 Academic)\",\n"
            "      \"explanation\": \"Examiner explanation in English and Bengali explaining why this collocation achieves Band 8.5+ Lexical Resource.\"\n"
            "    }\n"
            "  ]\n"
            "}"
        )
        prompt = f"Vocabulary Theme: {topic}. Generate {count} rigorous IELTS Academic Lexical Resource (LR) upgrade questions with student passage context."

        try:
            from ai_engine.ai_router import ai_router
            data = ai_router.generate_json(prompt, system_instruction=system_inst)
            if isinstance(data, dict) and "questions" in data and isinstance(data["questions"], list) and len(data["questions"]) > 0:
                for idx, q in enumerate(data["questions"]):
                    q["id"] = f"v_exam_dyn_{existing_count + idx + 1}"
                return data
        except Exception as e:
            print("Error generating dynamic vocab exam challenges via AI Router:", e)

        # Procedural fallback
        fallback_questions = []
        for i in range(1, count + 1):
            num = existing_count + i
            fallback_questions.append({
                "id": f"v_exam_dyn_{num}",
                "label": f"Academic Lexical Upgrade {num} ({topic}): Replace basic phrasing with C1/C2 lexis",
                "options": [
                    f"Comprehensive empirical evidence substantiates the profound impact of {topic} developments.",
                    f"A lot of studies show that big things happen with {topic}.",
                    f"People say that {topic} is getting very important nowadays."
                ],
                "answer": f"Comprehensive empirical evidence substantiates the profound impact of {topic} developments.",
                "explanation": f"ব্যান্ড ৮.৫ লেক্সিক্যাল রিসোর্স: 'Comprehensive empirical evidence' এবং 'substantiates the profound impact' হলো উচ্চমানের অ্যাকাডেমিক কলকেশন।"
            })

        return {
            "title": f"Academic Lexical Upgrade Challenge ({topic})",
            "passage": f"Many people believe that issues relating to {topic} are getting very serious nowadays. Society should do something quickly to make sure that things do not get worse.",
            "questions": fallback_questions
        }

grammar_vocab_engine = GrammarVocabEngine()


