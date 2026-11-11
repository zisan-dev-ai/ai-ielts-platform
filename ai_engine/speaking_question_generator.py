"""
AI Speaking Question Generator for Cambridge IELTS Speaking Tests
Generates authentic Part 1 (Interview), Part 2 (Cue Card with bullet prompts), 
and Part 3 (Analytical Discussion) sets dynamically using Gemini AI with rich fallbacks.
"""

import json
import random
from typing import Dict, Any, Optional
import sqlite3
from ai_engine.gemini_adapter import GeminiAdapter

class SpeakingQuestionGenerator:
    def __init__(self):
        self.ai = GeminiAdapter()

    def generate_full_speaking_set(self, custom_theme: str = "", p1_topic: str = "", p2_topic: str = "", p3_topic: str = "", api_key: str = "", api_key_pool: list = None) -> Dict[str, Any]:
        """
        Generates a complete 3-part Cambridge IELTS Speaking test set (Part 1, Part 2, Part 3)
        with specific or integrated topics for each part.
        """
        FALLBACK_THEMES = [
            "Artificial Intelligence and Future Employment",
            "Environmental Sustainability and Green Cities",
            "Digital Media and Interpersonal Communication",
            "Cultural Heritage and Ancient Architecture",
            "Sports, Physical Endurance and Public Health",
            "Global Tourism and Environmental Conservation",
            "Lifelong Learning and Higher Education Reform",
            "Space Exploration vs Domestic Social Investment"
        ]

        theme = custom_theme if custom_theme else (f"{p1_topic} / {p2_topic} / {p3_topic}" if (p1_topic or p2_topic or p3_topic) else random.choice(FALLBACK_THEMES))

        p1_instruction = 'Part 1 MUST have Frame 1 (Q1-Q2) on a mandatory baseline topic (Hometown & Neighbourhood, Work/Studies, or Home/Accommodation), and Frame 2 (Q3-Q4) on a separate secondary familiar topic.'
        p2_instruction = f'Part 2 Cue Card MUST focus on a specific personal experience or topic related to {theme}.'
        p3_instruction = f'Part 3 Discussion MUST be 100% thematically linked to the Part 2 topic, exploring broad societal, global, future, and ethical implications.'

        prompt = f"""You are a Cambridge IELTS Senior Speaking Examiner and test creator.
Generate an authentic, official Cambridge IELTS Speaking Test.
Main Theme: "{theme}"
Specifications:
- {p1_instruction}
- {p2_instruction}
- {p3_instruction}

You MUST return a strictly valid JSON object with this exact structure:
{{
  "theme": "{theme}",
  "part1": {{
    "title": "Mandatory Topic -> Secondary Topic",
    "topic": "Combined Topic Label",
    "mandatory_topic": "Hometown & Neighbourhood (or Work/Studies or Home/Accommodation)",
    "secondary_topic": "Secondary Familiar Topic (e.g. Food & Cooking, Weather, Tech, Sports, etc.)",
    "questions": [
      "Q1 (Mandatory topic question e.g. about hometown / studies / home)?",
      "Q2 (Mandatory topic question)?",
      "Q3 (Secondary topic question e.g. about food / weather / tech)?",
      "Q4 (Secondary topic question)?"
    ],
    "model_answers": [
      "Band 9 concise, natural answer for Q1 (2-3 sentences)...",
      "Band 9 concise, natural answer for Q2...",
      "Band 9 concise, natural answer for Q3...",
      "Band 9 concise, natural answer for Q4..."
    ]
  }},
  "part2": {{
    "title": "Describe a ... (official Cambridge phrasing)",
    "topic": "Cue Card topic tag",
    "cue_card_prompt": "<div class='cambridge-cue-card-inner'><h4>Describe a [specific experience/person/place/object/event].</h4><p><b>You should say:</b></p><ul><li>What / Who / Where it was</li><li>When and how it occurred</li><li>What specific actions were involved</li></ul><p><b>and explain why this experience was significant or memorable to you.</b></p></div>",
    "model_answer": "Full 180-220 word Band 9 model speech organized logically with natural discourse markers, rich academic idioms, and varied grammatical structures."
  }},
  "part3": {{
    "title": "Analytical Discussion (Thematically linked to Part 2)",
    "topic": "Abstract discussion tag linked to Part 2",
    "questions": [
      "Deep analytical question 1 (opinion / social trend related to Part 2 topic)?",
      "Deep analytical question 2 (comparison past vs present)?",
      "Deep analytical question 3 (future prediction or impact)?",
      "Deep analytical question 4 (policy / ethical aspect)?"
    ],
    "model_answers": [
      "Band 9 analytical, nuanced answer for Q1 with justification...",
      "Band 9 analytical answer for Q2...",
      "Band 9 analytical answer for Q3...",
      "Band 9 analytical answer for Q4..."
    ]
  }}
}}

CRITICAL REQUIREMENTS:
1. Part 1 Q1-Q2 MUST be baseline (Hometown/Studies/Home), Q3-Q4 MUST be secondary topic.
2. Part 3 MUST be thematically linked to Part 2.
3. Questions must match official Cambridge phrasing and difficulty.
4. Model answers must demonstrate Band 8.5-9.0 vocabulary and complex sentence structures.
5. Output ONLY the valid JSON object, without markdown backticks or commentary."""

        try:
            from ai_engine.ai_router import ai_router
            parsed = ai_router.generate_json(prompt)
            if parsed and "part1" in parsed and "part2" in parsed and "part3" in parsed:
                self._save_to_database(parsed)
                return parsed
        except Exception as e:
            print("AIRouter speaking set generation error, falling back:", e)

        raw_response = self._call_ai(prompt, api_key, api_key_pool)
        parsed = self._parse_json_safe(raw_response)

        if not parsed or "part1" not in parsed or "part2" not in parsed or "part3" not in parsed:
            # Fallback to database seeded set or targeted set
            return self._get_db_fallback_set(theme=theme, p1_topic=p1_topic, p2_topic=p2_topic, p3_topic=p3_topic)

        # Save generated set to database
        self._save_to_database(parsed)
        return parsed

    def _call_ai(self, prompt: str, api_key: str, api_key_pool: list) -> str:
        try:
            from ai_engine.ai_router import ai_router
            return ai_router.generate_text(prompt)
        except Exception:
            pass

        keys_to_try = [api_key] if api_key else []
        if api_key_pool:
            keys_to_try.extend([k for k in api_key_pool if k and k != api_key])

        if not keys_to_try:
            conn = sqlite3.connect('ielts_platform.db')
            cursor = conn.cursor()
            cursor.execute("SELECT api_key FROM ai_credentials WHERE status = 'Active'")
            keys_to_try = [r[0] for r in cursor.fetchall() if r[0]]
            conn.close()

        models_to_try = [
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash",
            "gemini-3.7-flash",
            "gemini-flash-latest"
        ]

        for model in models_to_try:
            for key in keys_to_try:
                try:
                    import requests
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                    resp = requests.post(
                        url,
                        json={
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {
                                "temperature": 0.3,
                                "maxOutputTokens": 4096,
                                "responseMimeType": "application/json"
                            }
                        },
                        timeout=18
                    )
                    if resp.status_code == 200:
                        data = resp.json()
                        return data['candidates'][0]['content']['parts'][0]['text']
                except Exception:
                    continue
        return ""

    def _parse_json_safe(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        clean = clean.strip()
        try:
            return json.loads(clean)
        except Exception:
            return None

    def _save_to_database(self, data: Dict[str, Any]):
        try:
            conn = sqlite3.connect('ielts_platform.db')
            cursor = conn.cursor()
            theme = data.get("theme", "Custom Topic")

            # Part 1
            p1 = data.get("part1", {})
            cursor.execute('''
                INSERT INTO questions (
                    skill, test_type, section_number, title, question_type,
                    passage_or_context, question_text, options_json, answer_key,
                    explanation, difficulty, cambridge_book, test_number,
                    passage_or_section, difficulty_band, group_id, group_instructions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Speaking", "Academic", 1, f"Speaking Part 1: {p1.get('title', 'Interview')}", "Speaking Part 1",
                json.dumps({"questions": p1.get("questions", []), "topic": p1.get("topic", theme)}),
                p1.get("questions", ["Tell me about yourself."])[0],
                json.dumps(p1.get("questions", [])),
                json.dumps(p1.get("model_answers", [])),
                json.dumps({"model_answers": p1.get("model_answers", []), "topic": p1.get("topic", theme)}),
                "Medium", "AI Custom", 1, "Part 1", 7.5, "SPK_AI_CUSTOM_P1",
                "Answer each interview question naturally and fluently."
            ))

            # Part 2
            p2 = data.get("part2", {})
            cursor.execute('''
                INSERT INTO questions (
                    skill, test_type, section_number, title, question_type,
                    passage_or_context, question_text, options_json, answer_key,
                    explanation, difficulty, cambridge_book, test_number,
                    passage_or_section, difficulty_band, group_id, group_instructions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Speaking", "Academic", 2, f"Speaking Part 2: {p2.get('title', 'Cue Card')}", "Speaking Part 2 - Cue Card",
                p2.get("cue_card_prompt", "<div>Describe a memorable experience.</div>"),
                p2.get("title", "Cue Card"),
                json.dumps({"notes_placeholder": "Key points & vocabulary..."}),
                p2.get("model_answer", "Band 9 answer"),
                f"### Band 9.0 Model Answer:\n{p2.get('model_answer', '')}",
                "Hard", "AI Custom", 1, "Part 2", 7.5, "SPK_AI_CUSTOM_P2",
                "Take 1 minute to prepare notes, then speak for 1 to 2 minutes."
            ))

            # Part 3
            p3 = data.get("part3", {})
            cursor.execute('''
                INSERT INTO questions (
                    skill, test_type, section_number, title, question_type,
                    passage_or_context, question_text, options_json, answer_key,
                    explanation, difficulty, cambridge_book, test_number,
                    passage_or_section, difficulty_band, group_id, group_instructions
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Speaking", "Academic", 3, f"Speaking Part 3: {p3.get('title', 'Discussion')}", "Speaking Part 3 - Discussion",
                json.dumps({"questions": p3.get("questions", []), "topic": p3.get("topic", theme)}),
                p3.get("questions", ["What are the broader impacts?"])[0],
                json.dumps(p3.get("questions", [])),
                json.dumps(p3.get("model_answers", [])),
                json.dumps({"model_answers": p3.get("model_answers", []), "topic": p3.get("topic", theme)}),
                "Hard", "AI Custom", 1, "Part 3", 7.5, "SPK_AI_CUSTOM_P3",
                "Discuss deep analytical issues with nuanced examples."
            ))

            conn.commit()
            conn.close()
        except Exception:
            pass

    def _get_db_fallback_set(self, theme: str = "", p1_topic: str = "", p2_topic: str = "", p3_topic: str = "") -> Dict[str, Any]:
        """Fetch an authentic test set from SQLite database or build targeted topic fallback"""
        conn = sqlite3.connect('ielts_platform.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT cambridge_book, test_number FROM questions WHERE skill = 'Speaking' AND cambridge_book != 'AI Custom' ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        if not row:
            conn.close()
            return {}

        book, test_num = row['cambridge_book'], row['test_number']

        cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 1", (book, test_num))
        p1_row = cursor.fetchone()

        cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 2", (book, test_num))
        p2_row = cursor.fetchone()

        cursor.execute("SELECT * FROM questions WHERE skill = 'Speaking' AND cambridge_book = ? AND test_number = ? AND section_number = 3", (book, test_num))
        p3_row = cursor.fetchone()

        conn.close()

        p1_ctx = json.loads(p1_row['passage_or_context']) if p1_row and p1_row['passage_or_context'].startswith('{') else {}
        p3_ctx = json.loads(p3_row['passage_or_context']) if p3_row and p3_row['passage_or_context'].startswith('{') else {}

        active_theme = theme or (f"{p1_topic} / {p2_topic} / {p3_topic}" if (p1_topic or p2_topic or p3_topic) else f"Cambridge Speaking Practice (Test {test_num})")

        p1_questions = [
            f"Let's talk about {p1_topic or 'your hometown'}. What do you like most about it?",
            f"How has {p1_topic or 'your area'} changed over the past few years?",
            f"Do you think you will continue to be involved in this in the future?",
            f"What advice would you give to someone new exploring {p1_topic or 'this subject'}?"
        ] if p1_topic else (json.loads(p1_row['options_json']) if p1_row and p1_row['options_json'] else ["Tell me about your daily routine."])

        p2_cue_card = f"""<div class='cambridge-cue-card-inner'>
<h4>{p2_topic or (p2_row['title'] if p2_row else 'Describe an interesting experience')}</h4>
<p><b>You should say:</b></p>
<ul>
  <li>What or who this was</li>
  <li>When and where this took place</li>
  <li>What key actions or decisions were involved</li>
</ul>
<p><b>and explain why this was particularly significant or memorable to you.</b></p>
</div>""" if p2_topic else (p2_row['passage_or_context'] if p2_row else "")

        p3_questions = [
            f"How do developments in {p3_topic or 'modern society'} affect everyday citizens?",
            f"Why do some people hold contrasting opinions regarding {p3_topic or 'social changes'}?",
            f"What role should governments or institutions play in addressing issues related to this?",
            f"How do you anticipate {p3_topic or 'this trend'} evolving over the next twenty years?"
        ] if p3_topic else (json.loads(p3_row['options_json']) if p3_row and p3_row['options_json'] else ["Discuss your perspective on modern trends."])

        return {
            "theme": active_theme,
            "part1": {
                "title": f"Part 1: {p1_topic or (p1_row['title'] if p1_row else 'Interview')}",
                "topic": p1_topic or p1_ctx.get("topic", "General"),
                "questions": p1_questions,
                "model_answers": [
                    "Well, speaking frankly, I find this area deeply fascinating because it directly connects to personal growth and daily adaptability.",
                    "In recent years, rapid modern development and digital tools have noticeably transformed how people approach this.",
                    "Looking ahead, I certainly anticipate staying actively engaged with this domain given its growing relevance in global society.",
                    "For newcomers, my primary advice would be to maintain consistency, curiosity, and an open-minded perspective."
                ]
            },
            "part2": {
                "title": p2_topic or (p2_row['title'] if p2_row else "Part 2: Cue Card"),
                "topic": p2_topic or "Cue Card",
                "cue_card_prompt": p2_cue_card,
                "model_answer": p2_row['answer_key'] if p2_row else "I would like to speak about this deeply memorable experience. It took place a few years ago and significantly reshaped my outlook on personal responsibility and academic determination. Through this experience, I gained invaluable insight into perseverance and critical problem-solving."
            },
            "part3": {
                "title": f"Part 3: Analytical Discussion on {p3_topic or (p3_row['title'] if p3_row else 'Society')}",
                "topic": p3_topic or p3_ctx.get("topic", "General Discussion"),
                "questions": p3_questions,
                "model_answers": [
                    "From an analytical standpoint, this phenomenon creates significant ripple effects across both economic productivity and societal well-being.",
                    "Public sentiment often diverges because different demographics prioritize short-term convenience versus long-term sustainability.",
                    "Institutional policymakers must implement balanced, evidence-based frameworks to ensure equitable access and ethical oversight.",
                    "Over the next few decades, I envision unprecedented technological integration and greater cross-cultural collaboration in this sector."
                ]
            }
        }
