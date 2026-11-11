# -*- coding: utf-8 -*-
import json
import random
import re
from typing import Dict, Any, List, Optional
from ai_engine.ai_router import ai_router
from seed_authentic_cambridge_listening_multiset import seed_random_listening_set, ALL_SETS, insert_listening_set
import sqlite3

class ListeningQuestionGenerator:
    """
    Universal Multi-Provider AI Listening Question Generator.
    Works seamlessly with ANY LLM provider:
    - OpenAI (GPT-4o, GPT-4o-mini, o1)
    - Claude (Claude 3.5 Sonnet / Haiku)
    - DeepSeek (V3, R1)
    - Grok (xAI)
    - Google Gemini
    - Custom / OpenRouter / Ollama / Local LLM
    """

    def __init__(self):
        self.router = ai_router

    def generate_practice_set(self, preferred_provider: Optional[str] = None, topic_theme: Optional[str] = None) -> Dict[str, Any]:
        """Generates a complete 4-Section, 40-Question authentic IELTS Listening Test."""
        prompt = self._build_generation_prompt(topic_theme)
        
        try:
            res_json = self.router.generate_json(
                prompt=prompt,
                system_instruction="You are a Senior Principal Examiner at Cambridge University Assessment English. You create 100% authentic British Council / IDP / Cambridge CD-IELTS Listening practice tests with natural transcripts and standard British English conventions.",
                preferred_provider=preferred_provider
            )
            
            if res_json and "sections" in res_json and len(res_json["sections"]) == 4:
                return self._save_ai_set_to_db(res_json)
        except Exception as e:
            print(f"[ListeningQuestionGenerator] AI Generation fallback triggered: {e}")
            
        # Fallback to authentic rotating Cambridge set
        return seed_random_listening_set()

    def _build_generation_prompt(self, topic_theme: Optional[str] = None) -> str:
        themes = [
            "Oceanographic Research & Coastal Marine Biology",
            "Renewable Microgrids & Green Energy Architecture",
            "Urban Forestry, Vertical Farming & Food Security",
            "Cognitive Neuroscience & Neuroplasticity",
            "Space Remote Sensing & Archaeology",
            "Autonomous Transport & Smart City Logistics",
            "Linguistics Anthropology & Ancient Manuscripts",
            "Materials Science & Nanotechnology"
        ]
        chosen_theme = topic_theme or random.choice(themes)

        return f"""Generate an official Cambridge IELTS Academic Listening Mock Test (4 Sections, exactly 40 Questions) on thematic domain: "{chosen_theme}".

Structure requirements:
1. Section 1 (Q1-10): Everyday social transaction / enquiry dialogue (2 speakers).
   - Question Type: "Form Completion"
   - Must include spelling of names, numbers, dates, room/service types, monetary amounts.
   - Instructions: "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer."

2. Section 2 (Q11-20): Monologue / tour guide of a public facility or cultural site.
   - Q11-15: "Multiple Choice" (4 options: A, B, C, D)
   - Q16-20: "Map Labelling" (options: A, B, C, D, E) matching specific zones in the facility.

3. Section 3 (Q21-30): Academic tutorial / thesis discussion between a professor/tutor and 2 university students.
   - Q21-23: "Multiple Choice"
   - Q24-30: "Sentence Completion" (NO MORE THAN TWO WORDS)

4. Section 4 (Q31-40): University academic lecture monologue on an advanced scientific or historical topic.
   - Q31-40: "Note Completion" (NO MORE THAN TWO WORDS AND/OR A NUMBER)

RETURN ONLY VALID JSON matching this exact schema:
{{
  "set_id": "AI_CUSTOM",
  "name": "Cambridge AI Generated - {chosen_theme}",
  "cambridge_book": 19,
  "test_number": 1,
  "sections": [
    {{
      "section_number": 1,
      "title": "Section 1: ... Registration Form",
      "instructions": "Complete the form below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
      "transcript": "Full realistic English dialogue text with clear question cues...",
      "questions": [
        {{"num": 1, "type": "Form Completion", "text": "...", "opts": [], "ans": "...", "exp": "..."}},
        ...
        {{"num": 10, "type": "Form Completion", "text": "...", "opts": [], "ans": "...", "exp": "..."}}
      ]
    }},
    {{
      "section_number": 2,
      "title": "Section 2: ... Facility Tour",
      "instructions": "Questions 11–15: Choose the correct letter, A, B, C, or D. Questions 16–20: Label the map below.",
      "transcript": "Full monologue text detailing facility zones A through E...",
      "questions": [
        {{"num": 11, "type": "Multiple Choice", "text": "...", "opts": ["A) ...", "B) ...", "C) ...", "D) ..."], "ans": "A) ...", "exp": "..."}},
        ...
        {{"num": 16, "type": "Map Labelling", "text": "Zone Name", "opts": ["A", "B", "C", "D", "E"], "ans": "A", "exp": "..."}},
        ...
        {{"num": 20, "type": "Map Labelling", "text": "Zone Name", "opts": ["A", "B", "C", "D", "E"], "ans": "E", "exp": "..."}}
      ]
    }},
    {{
      "section_number": 3,
      "title": "Section 3: ... Thesis Discussion",
      "instructions": "Answer questions 21–30 based on the academic discussion.",
      "transcript": "Full tutorial discussion between tutor and students...",
      "questions": [
        {{"num": 21, "type": "Multiple Choice", "text": "...", "opts": ["A) ...", "B) ...", "C) ...", "D) ..."], "ans": "B) ...", "exp": "..."}},
        ...
        {{"num": 24, "type": "Sentence Completion", "text": "... ________ ...", "opts": [], "ans": "...", "exp": "..."}},
        ...
        {{"num": 30, "type": "Sentence Completion", "text": "... ________ ...", "opts": [], "ans": "...", "exp": "..."}}
      ]
    }},
    {{
      "section_number": 4,
      "title": "Section 4: ... Academic Lecture",
      "instructions": "Complete the notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.",
      "transcript": "Full university academic lecture monologue...",
      "questions": [
        {{"num": 31, "type": "Note Completion", "text": "... ________ ...", "opts": [], "ans": "...", "exp": "..."}},
        ...
        {{"num": 40, "type": "Note Completion", "text": "... ________ ...", "opts": [], "ans": "...", "exp": "..."}}
      ]
    }}
  ]
}}"""

    def _save_ai_set_to_db(self, set_data: Dict[str, Any]) -> Dict[str, Any]:
        conn = sqlite3.connect('ielts_platform.db')
        cursor = conn.cursor()
        insert_listening_set(cursor, set_data)
        conn.commit()
        conn.close()
        return set_data

listening_question_generator = ListeningQuestionGenerator()
