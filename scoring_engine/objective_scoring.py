import re
from typing import Dict, Any, List

class ObjectiveScoringEngine:
    """100% Deterministic Answer-Key Scoring Engine for Reading & Listening with Word Limit Validation."""

    @staticmethod
    def normalize_answer(ans: str) -> str:
        if not ans:
            return ""
        cleaned = ans.strip().lower()
        # Remove extra whitespace and leading/trailing punctuation
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip('"\'.,')
        return cleaned

    @staticmethod
    def validate_word_limit(user_ans: str, max_words: int = 2, allow_number: bool = True) -> Dict[str, Any]:
        """Validates instructions like 'NO MORE THAN TWO WORDS AND/OR A NUMBER'."""
        cleaned = ObjectiveScoringEngine.normalize_answer(user_ans)
        if not cleaned:
            return {"is_valid": False, "reason": "Answer cannot be empty."}

        # Tokenize by words (hyphenated words count as single words in standard IELTS scoring)
        words = cleaned.split()
        word_count = len(words)

        if word_count > max_words:
            return {
                "is_valid": False,
                "reason": f"Exceeded word limit! Maximum {max_words} words allowed, but you entered {word_count} words."
            }

        return {"is_valid": True, "word_count": word_count}

    @staticmethod
    def is_answer_correct(user_ans: str, answer_key: str) -> bool:
        norm_user = ObjectiveScoringEngine.normalize_answer(user_ans)
        norm_key = ObjectiveScoringEngine.normalize_answer(answer_key)

        if not norm_user or not norm_key:
            return False

        if norm_user == norm_key:
            return True

        # True / False / Not Given & Yes / No / Not Given mapping
        tf_map = {
            "true": ["true", "t"],
            "false": ["false", "f"],
            "not given": ["not given", "ng"],
            "yes": ["yes", "y"],
            "no": ["no", "n"]
        }

        for key, valid_list in tf_map.items():
            if norm_key in valid_list and norm_user in valid_list:
                return True

        # Multiple slash-separated valid keys (e.g. "15 / fifteen / 15 percent")
        if "/" in answer_key:
            valid_keys = [ObjectiveScoringEngine.normalize_answer(k) for k in answer_key.split("/")]
            if norm_user in valid_keys:
                return True

        return False

    @staticmethod
    def calculate_raw_to_band(raw_score: int, total_questions: int = 40, skill: str = "reading", ielts_type: str = "Academic") -> float:
        """
        Converts raw score (0-40) to 100% official Cambridge IELTS Band Score (Band 0.0 to 9.0).
        Supports Academic Reading, General Training Reading, and Listening.
        """
        if total_questions == 0 or raw_score <= 0:
            return 0.0

        scaled_raw = int(round((raw_score / total_questions) * 40))
        scaled_raw = max(0, min(40, scaled_raw))

        if skill.lower() == "reading":
            if ielts_type.lower() == "academic":
                if scaled_raw >= 39: return 9.0
                elif scaled_raw >= 37: return 8.5
                elif scaled_raw >= 35: return 8.0
                elif scaled_raw >= 33: return 7.5
                elif scaled_raw >= 30: return 7.0
                elif scaled_raw >= 27: return 6.5
                elif scaled_raw >= 23: return 6.0
                elif scaled_raw >= 19: return 5.5
                elif scaled_raw >= 15: return 5.0
                elif scaled_raw >= 13: return 4.5
                elif scaled_raw >= 10: return 4.0
                elif scaled_raw >= 8:  return 3.5
                elif scaled_raw >= 6:  return 3.0
                elif scaled_raw >= 4:  return 2.5
                elif scaled_raw >= 2:  return 2.0
                elif scaled_raw >= 1:  return 1.0
                else: return 0.0
            else:  # General Training Reading
                if scaled_raw >= 40: return 9.0
                elif scaled_raw >= 39: return 8.5
                elif scaled_raw >= 37: return 8.0
                elif scaled_raw >= 36: return 7.5
                elif scaled_raw >= 34: return 7.0
                elif scaled_raw >= 32: return 6.5
                elif scaled_raw >= 30: return 6.0
                elif scaled_raw >= 27: return 5.5
                elif scaled_raw >= 23: return 5.0
                elif scaled_raw >= 19: return 4.5
                elif scaled_raw >= 15: return 4.0
                elif scaled_raw >= 12: return 3.5
                elif scaled_raw >= 9:  return 3.0
                elif scaled_raw >= 6:  return 2.5
                elif scaled_raw >= 3:  return 2.0
                elif scaled_raw >= 1:  return 1.0
                else: return 0.0
        else:  # Listening (Standard across Academic & General)
            if scaled_raw >= 39: return 9.0
            elif scaled_raw >= 37: return 8.5
            elif scaled_raw >= 35: return 8.0
            elif scaled_raw >= 32: return 7.5
            elif scaled_raw >= 30: return 7.0
            elif scaled_raw >= 26: return 6.5
            elif scaled_raw >= 23: return 6.0
            elif scaled_raw >= 18: return 5.5
            elif scaled_raw >= 16: return 5.0
            elif scaled_raw >= 13: return 4.5
            elif scaled_raw >= 10: return 4.0
            elif scaled_raw >= 8:  return 3.5
            elif scaled_raw >= 6:  return 3.0
            elif scaled_raw >= 4:  return 2.5
            elif scaled_raw >= 2:  return 2.0
            elif scaled_raw >= 1:  return 1.0
            else: return 0.0

    @staticmethod
    def get_band_descriptor_info(band: float) -> Dict[str, str]:
        """Returns official Cambridge IELTS band description and CEFR level for Band 0.0 to 9.0."""
        if band >= 9.0:
            return {"descriptor": "Expert User", "cefr": "C2", "summary": "Fully operational command of the language: appropriate, accurate and fluent with complete understanding."}
        elif band >= 8.0:
            return {"descriptor": "Very Good User", "cefr": "C1/C2", "summary": "Fully operational command with only occasional unsystematic inaccuracies. Handles complex detailed argumentation well."}
        elif band >= 7.0:
            return {"descriptor": "Good User", "cefr": "C1", "summary": "Operational command, though with occasional inaccuracies. Generally handles complex language well and understands detailed reasoning."}
        elif band >= 6.0:
            return {"descriptor": "Competent User", "cefr": "B2", "summary": "Generally effective command despite some inaccuracies. Can use and understand fairly complex language, particularly in familiar situations."}
        elif band >= 5.0:
            return {"descriptor": "Modest User", "cefr": "B1", "summary": "Partial command, coping with overall meaning in most situations, though is likely to make many mistakes."}
        elif band >= 4.0:
            return {"descriptor": "Limited User", "cefr": "A2", "summary": "Basic competence is limited to familiar situations. Has frequent problems in understanding and expression."}
        elif band >= 3.0:
            return {"descriptor": "Extremely Limited User", "cefr": "A1", "summary": "Conveys and understands only general meaning in very familiar situations. Frequent breakdowns in communication occur."}
        elif band >= 2.0:
            return {"descriptor": "Intermittent User", "cefr": "Pre-A1", "summary": "No real communication is possible except for the most basic information using isolated words."}
        elif band >= 1.0:
            return {"descriptor": "Non-User", "cefr": "Pre-A1", "summary": "Essentially has no ability to use the language beyond possibly a few isolated words."}
        else:
            return {"descriptor": "Did Not Attempt", "cefr": "N/A", "summary": "No assessable information provided."}
