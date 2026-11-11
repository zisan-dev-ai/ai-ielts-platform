import json
from ai_engine.ai_router import ai_router
from database import get_db

class WritingEvaluatorEngine:
    @staticmethod
    def submit_and_evaluate(user_id: int, task_type: str, prompt_title: str, prompt_text: str, submission_text: str, time_spent_seconds: int) -> dict:
        word_count = len(submission_text.strip().split()) if submission_text else 0
        
        # 1. Save submission to DB
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO writing_submissions 
            (user_id, task_type, prompt_title, prompt_text, submission_text, word_count, time_spent_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, task_type, prompt_title, prompt_text, submission_text, word_count, time_spent_seconds))
        sub_id = cursor.lastrowid
        conn.commit()

        # 2. Invoke AI Router for Rubric Evaluation
        eval_result = ai_router.evaluate_writing(prompt_text, submission_text, task_type)

        # 3. Save Evaluation to DB
        cursor.execute("""
            INSERT INTO writing_evaluations 
            (submission_id, task_achievement, coherence_cohesion, lexical_resource, grammatical_range, overall_band, 
             strengths_json, weaknesses_json, line_by_line_errors_json, improvement_plan, provider_used)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sub_id,
            eval_result.get("task_achievement", 6.5),
            eval_result.get("coherence_cohesion", 6.5),
            eval_result.get("lexical_resource", 6.5),
            eval_result.get("grammatical_range", 6.0),
            eval_result.get("overall_band", 6.5),
            json.dumps(eval_result.get("strengths", [])),
            json.dumps(eval_result.get("weaknesses", [])),
            json.dumps(eval_result.get("line_by_line_errors", [])),
            eval_result.get("improvement_plan", ""),
            eval_result.get("provider_used", "AI Router")
        ))
        conn.commit()
        conn.close()

        eval_result["submission_id"] = sub_id
        eval_result["word_count"] = word_count
        return eval_result
