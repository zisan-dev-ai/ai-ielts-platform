# -*- coding: utf-8 -*-
import json
import random
import re
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional
from ai_engine.gemini_adapter import GeminiAdapter

ALL_14_QUESTION_TYPES = [
    "True / False / Not Given",
    "Yes / No / Not Given",
    "Multiple Choice",
    "Matching Headings",
    "Matching Information",
    "Matching Features",
    "Matching Sentence Endings",
    "Sentence Completion",
    "Summary Completion",
    "Note Completion",
    "Table Completion",
    "Flow-chart Completion",
    "Short Answer Questions"
]

TYPE_ROTATIONS = [
    # Set 1: Classic Balanced
    {
        "P1": ["True / False / Not Given", "Note Completion"],
        "P2": ["Matching Headings", "Matching Features", "Summary Completion"],
        "P3": ["Yes / No / Not Given", "Multiple Choice", "Matching Sentence Endings"]
    },
    # Set 2: Completion & Info Matching
    {
        "P1": ["Sentence Completion", "Table Completion"],
        "P2": ["Matching Information", "Short Answer Questions", "Multiple Choice"],
        "P3": ["True / False / Not Given", "Flow-chart Completion", "Summary Completion"]
    },
    # Set 3: Headings & Analysis
    {
        "P1": ["Matching Information", "True / False / Not Given"],
        "P2": ["Multiple Choice", "Note Completion", "Matching Features"],
        "P3": ["Yes / No / Not Given", "Matching Sentence Endings", "Short Answer Questions"]
    },
    # Set 4: Summary & Sentence Flow
    {
        "P1": ["Multiple Choice", "Short Answer Questions"],
        "P2": ["Matching Headings", "True / False / Not Given", "Sentence Completion"],
        "P3": ["Matching Information", "Summary Completion", "Yes / No / Not Given"]
    },
    # Set 5: Flowchart & Features
    {
        "P1": ["Flow-chart Completion", "True / False / Not Given"],
        "P2": ["Matching Information", "Matching Features", "Note Completion"],
        "P3": ["Multiple Choice", "Yes / No / Not Given", "Table Completion"]
    },
    # Set 6: Headings & Table
    {
        "P1": ["Matching Headings", "Sentence Completion"],
        "P2": ["True / False / Not Given", "Table Completion", "Short Answer Questions"],
        "P3": ["Matching Information", "Yes / No / Not Given", "Multiple Choice"]
    }
]

class ReadingQuestionGenerator:
    def __init__(self):
        self.adapter = GeminiAdapter()

    def generate_practice_set(
        self, 
        api_key: str, 
        api_key_pool: list = None, 
        custom_types: Optional[Dict[str, List[str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate authentic Cambridge IELTS Academic Reading practice test.
        Uses high-speed parallel generation for all 3 passages (~4-6s total).
        """
        rotation = custom_types if custom_types and any(custom_types.values()) else self._get_type_rotation()
        
        p1_types = rotation.get("P1") or ["True / False / Not Given", "Note Completion"]
        p2_types = rotation.get("P2") or ["Matching Headings", "Summary Completion"]
        p3_types = rotation.get("P3") or ["Yes / No / Not Given", "Multiple Choice", "Matching Sentence Endings"]

        # Run all 3 passage generations concurrently in parallel
        tasks = [
            {
                "passage_num": 1,
                "q_start": 1,
                "q_count": 13,
                "selected_types": p1_types,
                "topic_category": "History, archaeology, exploration, or biodiversity",
                "difficulty": "Band 6.5 (Easy to Moderate)"
            },
            {
                "passage_num": 2,
                "q_start": 14,
                "q_count": 13,
                "selected_types": p2_types,
                "topic_category": "Technology, renewable energy, urban planning, agriculture, or sociology",
                "difficulty": "Band 7.0 (Moderate to Challenging)"
            },
            {
                "passage_num": 3,
                "q_start": 27,
                "q_count": 14,
                "selected_types": p3_types,
                "topic_category": "Neuroscience, cognitive psychology, AI ethics, astrophysics, or linguistics",
                "difficulty": "Band 8.0 (Academic & Challenging)"
            }
        ]

        passages_by_num = {}

        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_num = {
                executor.submit(
                    self._generate_single_passage,
                    t["passage_num"],
                    t["q_start"],
                    t["q_count"],
                    t["selected_types"],
                    t["topic_category"],
                    t["difficulty"],
                    api_key,
                    api_key_pool
                ): t["passage_num"] for t in tasks
            }

            for future in as_completed(future_to_num):
                p_num = future_to_num[future]
                try:
                    res = future.result()
                    if res and "questions" in res and len(res["questions"]) > 0:
                        passages_by_num[p_num] = res
                except Exception as e:
                    print(f"[ReadingQuestionGenerator] Passage {p_num} thread error: {e}")

        # If all 3 succeeded, return them in order
        if len(passages_by_num) == 3:
            ordered_passages = [passages_by_num[1], passages_by_num[2], passages_by_num[3]]
            return {"passages": ordered_passages}
        
        # If any passage failed, merge with fallback
        fallback = self._get_rich_fallback_set()
        for i in range(1, 4):
            if i not in passages_by_num and i <= len(fallback["passages"]):
                passages_by_num[i] = fallback["passages"][i - 1]

        ordered_passages = [passages_by_num.get(1), passages_by_num.get(2), passages_by_num.get(3)]
        ordered_passages = [p for p in ordered_passages if p]
        return {"passages": ordered_passages}

    def _generate_single_passage(
        self,
        passage_num: int,
        q_start: int,
        q_count: int,
        selected_types: List[str],
        topic_category: str,
        difficulty: str,
        api_key: str,
        api_key_pool: list
    ) -> Optional[Dict[str, Any]]:
        types_str = ", ".join(selected_types)
        q_end = q_start + q_count - 1

        prompt = f"""Create Reading Passage {passage_num} for Cambridge IELTS Academic Reading.

TOPIC: {topic_category}
DIFFICULTY: {difficulty}
QUESTIONS: Exactly {q_count} questions (numbered {q_start} to {q_end}) using these question types: {types_str}.

REQUIREMENTS:
1. Academic passage: 750–900 words, split into Paragraphs A, B, C, D, E, F with rich academic vocabulary.
2. Group the {q_count} questions into realistic Cambridge question groups (e.g. Group 1: Q{q_start}-Q{q_start+5}, Group 2: Q{q_start+6}-Q{q_end}).
3. For each group provide group_instructions (e.g. 'Do the following statements agree...', 'Choose NO MORE THAN TWO WORDS', etc.).
4. Provide detailed explanation for every question with Cambridge trap analysis.

RETURN STRICTLY A SINGLE RAW JSON OBJECT (no markdown, no backticks, no code fences):
{{
  "number": {passage_num},
  "title": "Passage Title",
  "text": "Paragraph A\\n[Content of A]\\n\\nParagraph B\\n[Content of B]\\n\\nParagraph C\\n[Content of C]\\n\\nParagraph D\\n[Content of D]\\n\\nParagraph E\\n[Content of E]",
  "questions": [
    {{
      "num": {q_start},
      "type": "{selected_types[0] if selected_types else 'Multiple Choice'}",
      "group_id": "P{passage_num}_G1",
      "group_instructions": "Official Cambridge instructions...",
      "text": "Question statement or text...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "Option A",
      "explanation": "Paragraph B states... explaining why this is correct.",
      "difficulty": "medium"
    }}
  ]
}}
"""
        system = "You are a Cambridge IELTS Senior Test Constructor. Output ONLY valid JSON matching the exact schema."
        try:
            from ai_engine.ai_router import ai_router
            parsed = ai_router.generate_json(prompt, system_instruction=system)
            if parsed and "title" in parsed and "questions" in parsed and len(parsed["questions"]) > 0:
                parsed["number"] = passage_num
                return parsed
        except Exception as e:
            print(f"[ReadingQuestionGenerator] AIRouter passage {passage_num} error, trying fallback: {e}")

        try:
            raw_text = self._call_gemini(prompt, api_key, system, api_key_pool)
            parsed = self._parse_json_safe(raw_text)
            if parsed and "title" in parsed and "questions" in parsed and len(parsed["questions"]) > 0:
                parsed["number"] = passage_num
                return parsed
        except Exception as e:
            print(f"[ReadingQuestionGenerator] Passage {passage_num} generation error: {e}")
        return None

    def _parse_json_safe(self, raw_text: str) -> Optional[Dict[str, Any]]:
        clean = raw_text.strip()
        clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.MULTILINE)
        clean = re.sub(r"\s*```$", "", clean, flags=re.MULTILINE)
        clean = clean.strip()

        first_brace = clean.find("{")
        last_brace = clean.rfind("}")
        if first_brace != -1 and last_brace != -1:
            clean = clean[first_brace:last_brace + 1]

        try:
            return json.loads(clean)
        except Exception:
            # Try cleaning trailing commas
            clean_fixed = re.sub(r",\s*([\]}])", r"\1", clean)
            try:
                return json.loads(clean_fixed)
            except Exception:
                return None

    def _call_gemini(self, prompt: str, api_key: str, system_instruction: str, api_key_pool: list) -> str:
        keys_to_try = [api_key] if api_key else []
        if api_key_pool:
            for k in api_key_pool:
                if k and k not in keys_to_try:
                    keys_to_try.append(k)

        if not keys_to_try:
            raise ValueError("No valid API keys available.")

        models_to_try = [
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash",
            "gemini-3.7-flash",
            "gemini-flash-latest"
        ]
        last_error = None

        for model in models_to_try:
            for key in keys_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 4096
                    }
                }
                if system_instruction:
                    payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

                try:
                    response = requests.post(url, json=payload, timeout=25)
                    if response.status_code == 200:
                        data = response.json()
                        candidates = data.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            parts = candidates[0]["content"].get("parts", [])
                            if parts:
                                return parts[0].get("text", "")
                    elif response.status_code in [429, 503]:
                        last_error = f"Model {model} busy ({response.status_code})"
                        continue
                    else:
                        last_error = f"Model {model} HTTP {response.status_code}"
                        continue
                except Exception as e:
                    last_error = f"Model {model} error: {str(e)}"
                    continue

        raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")

    def _get_type_rotation(self) -> Dict[str, List[str]]:
        return random.choice(TYPE_ROTATIONS)

    def _get_rich_fallback_set(self) -> Dict[str, Any]:
        from seed_authentic_cambridge_reading_full import get_set_a_questions
        questions = get_set_a_questions()
        
        passages_map = {1: {"title": "", "text": "", "questions": []},
                        2: {"title": "", "text": "", "questions": []},
                        3: {"title": "", "text": "", "questions": []}}

        for q in questions:
            sec = q.get("section_number", 1)
            if not passages_map[sec]["title"]:
                passages_map[sec]["title"] = q.get("title", f"Passage {sec}")
                passages_map[sec]["text"] = q.get("passage_or_context", "")
            
            passages_map[sec]["questions"].append({
                "num": len(passages_map[sec]["questions"]) + 1,
                "type": q.get("question_type", "Multiple Choice"),
                "group_id": q.get("group_id", f"P{sec}_G1"),
                "group_instructions": q.get("group_instructions", ""),
                "text": q.get("question_text", ""),
                "options": q.get("options_json", []),
                "answer": q.get("answer_key", ""),
                "explanation": q.get("explanation", ""),
                "difficulty": q.get("difficulty", "medium")
            })

        return {
            "passages": [
                {"number": 1, "title": passages_map[1]["title"], "text": passages_map[1]["text"], "questions": passages_map[1]["questions"]},
                {"number": 2, "title": passages_map[2]["title"], "text": passages_map[2]["text"], "questions": passages_map[2]["questions"]},
                {"number": 3, "title": passages_map[3]["title"], "text": passages_map[3]["text"], "questions": passages_map[3]["questions"]}
            ]
        }
