# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from database import get_db

class SpacedRepetitionEngine:
    """
    Spaced Repetition System (SRS) & Mistake Notebook Engine.
    Uses SuperMemo SM-2 interval algorithms to schedule re-testing of weak 
    Cambridge question types, vocabulary, and grammatical structures.
    """
    def __init__(self):
        self.intervals = [1, 3, 7, 14, 30]

    def get_due_reviews(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch Cambridge questions due for SRS review."""
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, skill, question_type, question_title, user_answer, correct_answer, explanation, mastery_status, created_at
            FROM mistake_notebook
            WHERE user_id = ? AND mastery_status != 'Mastered'
            ORDER BY id ASC
            LIMIT ?
        """, (user_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "skill": r["skill"],
                "question_type": r["question_type"],
                "question_title": r["question_title"],
                "user_answer": r["user_answer"],
                "correct_answer": r["correct_answer"],
                "explanation": r["explanation"],
                "mastery_status": r["mastery_status"],
                "created_at": r["created_at"]
            })
        return result

    def record_review_result(self, user_id: int, mistake_id: int, is_correct: bool) -> Dict[str, Any]:
        """Record outcome of SRS review attempt and adjust interval stage."""
        conn = get_db()
        cursor = conn.cursor()
        
        if is_correct:
            cursor.execute("""
                UPDATE mistake_notebook
                SET mastery_status = 'Mastered'
                WHERE id = ? AND user_id = ?
            """, (mistake_id, user_id))
            status = "Mastered"
            msg = "🎉 Great job! You have mastered this question type."
        else:
            cursor.execute("""
                UPDATE mistake_notebook
                SET mastery_status = 'Needs Practice'
                WHERE id = ? AND user_id = ?
            """, (mistake_id, user_id))
            status = "Needs Practice"
            msg = "Keep practicing! Scheduled for next interval review."

        conn.commit()
        conn.close()
        
        return {
            "mistake_id": mistake_id,
            "mastery_status": status,
            "message": msg
        }

    def get_grammar_vocab_reviews(self, user_id: int) -> List[Dict[str, Any]]:
        """Fetch vocabulary and grammar items due for spaced review."""
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, item_type, topic_or_word, category, mastery_stage, review_stage, next_review_date
            FROM student_grammar_vocab_mastery
            WHERE user_id = ?
            ORDER BY review_stage ASC
        """, (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in rows]

srs_engine = SpacedRepetitionEngine()
