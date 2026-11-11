# -*- coding: utf-8 -*-
"""
Speaking Examiner Agent — Dr. Sarah Jenkins AI Engine
Provides authentic, real-time, context-aware conversational reactions and transitions
for British Council Computer-Delivered IELTS Speaking Examination.
"""

import json
import re
import random
from typing import Dict, Any, Optional
from ai_engine.ai_router import AIRouter

class SpeakingExaminerAgent:
    def __init__(self):
        self.router = AIRouter()

    def generate_reaction(
        self,
        candidate_speech: str,
        current_question: str,
        next_question: str,
        part_number: int = 1,
        topic_context: str = "",
        is_part_transition: bool = False
    ) -> Dict[str, Any]:
        """
        Generates Dr. Sarah Jenkins' spoken response, bridging what the student actually said
        to the next scheduled question or section.
        """
        speech_clean = (candidate_speech or "").strip()
        speech_lower = speech_clean.lower()

        # 1. Profanity / Abusive / Non-exam behavior check
        profanity_patterns = [r'\bfuck\b', r'\bshit\b', r'\bbitch\b', r'\basshole\b', r'\bdick\b', r'\bpiss off\b', r'\bshut up\b', r'\bshala\b', r'\bkhankir\b', r'\bchoda\b', r'\bbal\b']
        is_abusive = any(re.search(p, speech_lower) for p in profanity_patterns)

        if is_abusive:
            spoken_reaction = (
                f"Please maintain formal examination conduct and refrain from using inappropriate language. "
                f"Let us continue with the test. {next_question}"
            )
            return {
                "spoken_text": spoken_reaction,
                "display_text": next_question,
                "examiner_note": "⚠️ Inappropriate language detected. Examiner reminded candidate of formal test decorum.",
                "quality": "inappropriate"
            }

        # 2. Empty / Inaudible / Very short
        words = [w for w in speech_clean.split() if w.isalnum()]
        if len(words) < 2:
            if is_part_transition:
                spoken_reaction = f"Thank you. Now let us move on. {next_question}"
            else:
                spoken_reaction = f"Thank you. Moving on to our next question: {next_question}"
            return {
                "spoken_text": spoken_reaction,
                "display_text": next_question,
                "examiner_note": "Brief / minimal response recorded.",
                "quality": "minimal"
            }

        # 3. "I don't know" / Refusal to answer
        idk_patterns = [r"i don'?t know", r"no idea", r"not sure", r"skip", r"pass this", r"can'?t answer"]
        if any(re.search(p, speech_lower) for p in idk_patterns) and len(words) < 8:
            spoken_reaction = f"I understand. Let us move to a different question. {next_question}"
            return {
                "spoken_text": spoken_reaction,
                "display_text": next_question,
                "examiner_note": "Candidate requested to move to next question.",
                "quality": "skipped"
            }

        # 4. Try AI LLM for context-aware, human examiner acknowledgment (Dr. Sarah Jenkins)
        ai_bridge = self._try_llm_examiner_bridge(speech_clean, current_question, next_question, part_number, topic_context)
        if ai_bridge:
            return {
                "spoken_text": ai_bridge,
                "display_text": next_question,
                "examiner_note": "Contextually acknowledged candidate response.",
                "quality": "conversational"
            }

        # 5. Smart Rule-Based Fallback if LLM unavailable
        smart_bridge = self._generate_smart_fallback_bridge(speech_clean, current_question, next_question, part_number)
        return {
            "spoken_text": smart_bridge,
            "display_text": next_question,
            "examiner_note": "Standard conversational transition.",
            "quality": "standard"
        }

    def _try_llm_examiner_bridge(
        self,
        candidate_speech: str,
        current_question: str,
        next_question: str,
        part_number: int,
        topic_context: str
    ) -> Optional[str]:
        prompt = f"""You are Dr. Sarah Jenkins, an authentic senior British Council IELTS Speaking Examiner.
The candidate just responded to your question in Part {part_number} of the IELTS Speaking exam.

### WHAT YOU ASKED:
"{current_question}"

### WHAT THE CANDIDATE JUST SAID:
"{candidate_speech}"

### THE NEXT SCHEDULED QUESTION:
"{next_question}"

### YOUR TASK:
1. Provide a short, natural, human examiner reaction (3 to 8 words) reacting directly to what the candidate just said.
   - For example:
     - If candidate said they study computer science: "I see, computing is a rapidly expanding field."
     - If candidate mentioned working as an accountant: "That sounds like a role requiring great precision."
     - If candidate mentioned living near the beach: "A coastal town must be very refreshing."
     - If candidate gave a general answer: "Thank you, that's a very clear perspective."
2. Then, seamlessly attach the next question: "{next_question}"

### RULES:
- Output ONLY the final speech string that Dr. Sarah Jenkins will say aloud.
- Do NOT output any markdown, JSON, or quotes.
- Total response should be 1-2 spoken sentences containing your brief natural reaction followed by the next question."""

        try:
            for provider in ["gemini", "deepseek", "openai", "claude"]:
                adapter = self.router.adapters.get(provider)
                cred = self.router.fallback_order
                if adapter:
                    resp = adapter.generate_text(prompt, max_tokens=150, timeout=3)
                    if resp and len(resp.strip()) > 10:
                        clean_resp = resp.strip().replace('"', '').replace('\n', ' ')
                        return clean_resp
        except Exception:
            pass

        return None

    def _generate_smart_fallback_bridge(
        self,
        candidate_speech: str,
        current_question: str,
        next_question: str,
        part_number: int
    ) -> str:
        speech_lower = candidate_speech.lower()

        # Contextual detection
        if any(w in speech_lower for w in ["student", "study", "university", "college", "school", "major", "degree", "class"]):
            lead = random.choice([
                "I see, academic life can certainly be demanding.",
                "Thank you, that gives a clear picture of your studies.",
                "Right, that sounds like an engaging field of study."
            ])
        elif any(w in speech_lower for w in ["work", "job", "office", "company", "career", "business", "colleague", "boss", "profession"]):
            lead = random.choice([
                "I see, that sounds like a dynamic professional environment.",
                "Thank you, that's very clear regarding your work.",
                "Right, professional experience is very valuable."
            ])
        elif any(w in speech_lower for w in ["city", "town", "village", "born", "grew up", "live", "flat", "apartment", "house", "neighbourhood"]):
            lead = random.choice([
                "Thank you, that gives a vivid picture of your area.",
                "I see, living in that kind of environment must have its unique qualities.",
                "Right, that is very interesting."
            ])
        elif any(w in speech_lower for w in ["food", "cook", "dish", "meal", "restaurant", "taste", "delicious"]):
            lead = random.choice([
                "Thank you, that sounds like a very distinctive culinary tradition.",
                "I see, home cooking certainly has its own special appeal.",
                "Right, food culture is always fascinating."
            ])
        elif any(w in speech_lower for w in ["phone", "app", "technology", "computer", "internet", "social media", "ai", "digital"]):
            lead = random.choice([
                "Indeed, digital tools have transformed how we navigate our days.",
                "I see, technology certainly plays a major role in daily life.",
                "Right, that's a very common experience with modern devices."
            ])
        else:
            lead = random.choice([
                "Thank you, that is very clear.",
                "I see, thank you for sharing that.",
                "Right, thank you.",
                "That's a thoughtful point, thank you."
            ])

        return f"{lead} Now, {next_question}"
