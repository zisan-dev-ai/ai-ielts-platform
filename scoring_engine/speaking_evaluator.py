import json
from ai_engine.ai_router import ai_router
from database import get_db

class SpeakingEvaluatorEngine:
    @staticmethod
    def submit_and_evaluate(user_id: int, part_number: int, prompt_title: str, prompt_text: str, transcript: str, audio_file_path: str, time_spent_seconds: int) -> dict:
        # 1. Save Speaking session to DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO speaking_sessions 
            (user_id, part_number, prompt_title, prompt_text, audio_file_path, transcript, time_spent_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, part_number, prompt_title, prompt_text, audio_file_path, transcript, time_spent_seconds))
        session_id = cursor.lastrowid
        conn.commit()

        # 2. Invoke AI Router for Rubric Evaluation
        eval_result = ai_router.evaluate_speaking(transcript, prompt_text, part_number)

        # 3. Save Evaluation to DB
        cursor.execute("""
            INSERT INTO speaking_evaluations 
            (session_id, fluency_coherence, lexical_resource, grammatical_range, pronunciation, overall_band, 
             strengths_json, weaknesses_json, phonetic_feedback_json, improvement_plan, provider_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            eval_result.get("fluency_coherence", 6.5),
            eval_result.get("lexical_resource", 6.5),
            eval_result.get("grammatical_range", 6.0),
            eval_result.get("pronunciation", 6.5),
            eval_result.get("overall_band", 6.5),
            json.dumps(eval_result.get("strengths", [])),
            json.dumps(eval_result.get("weaknesses", [])),
            json.dumps(eval_result.get("phonetic_feedback", [])),
            eval_result.get("improvement_plan", ""),
            eval_result.get("provider_used", "AI Router")
        ))
        conn.commit()
        conn.close()

        eval_result["session_id"] = session_id
        return eval_result
