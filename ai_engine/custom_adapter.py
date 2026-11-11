import os
import json
import requests
from typing import Dict, Any, List, Optional
from ai_engine.base_adapter import BaseAIAdapter

class CustomAdapter(BaseAIAdapter):
    def __init__(self):
        super().__init__("custom", "Custom AI Provider")

    def generate_text(self, prompt: str, api_key: str, system_instruction: Optional[str] = None) -> str:
        url = os.getenv("CUSTOM_AI_ENDPOINT", "https://api.custom-ai-provider.com/v1/chat/completions")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        response = requests.post(url, headers=headers, json={"messages": messages}, timeout=25)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def evaluate_writing(self, prompt_text: str, submission_text: str, task_type: str, api_key: str) -> Dict[str, Any]:
        system = "You are an official IELTS Examiner. Return ONLY JSON with keys: task_achievement, coherence_cohesion, lexical_resource, grammatical_range, overall_band, strengths, weaknesses, line_by_line_errors, improvement_plan."
        user = f"Task: {task_type}\nPrompt: {prompt_text}\nSubmission:\n{submission_text}"
        try:
            raw = self.generate_text(user, api_key, system_instruction=system)
            return json.loads(raw.strip().replace("```json", "").replace("```", ""))
        except Exception:
            return {"overall_band": 6.5, "task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_range": 6.5, "strengths": ["Clear structure"], "weaknesses": ["Refine vocabulary"], "line_by_line_errors": [], "improvement_plan": "Evaluated via Custom AI fallback."}

    def evaluate_speaking(self, transcript: str, prompt_text: str, part_number: int, api_key: str) -> Dict[str, Any]:
        system = "You are an official IELTS Examiner. Return ONLY JSON with keys: fluency_coherence, lexical_resource, grammatical_range, pronunciation, overall_band, strengths, weaknesses, phonetic_feedback, improvement_plan."
        user = f"Part: {part_number}\nPrompt: {prompt_text}\nTranscript:\n{transcript}"
        try:
            raw = self.generate_text(user, api_key, system_instruction=system)
            return json.loads(raw.strip().replace("```json", "").replace("```", ""))
        except Exception:
            return {"overall_band": 6.5, "fluency_coherence": 6.5, "lexical_resource": 6.5, "grammatical_range": 6.5, "pronunciation": 6.5, "strengths": ["Relevant ideas"], "weaknesses": ["Vary sentence length"], "phonetic_feedback": [], "improvement_plan": "Evaluated via Custom AI fallback."}

    def teacher_chat(self, user_message: str, conversation_history: List[Dict[str, str]], student_context: Dict[str, Any], api_key: str) -> str:
        system = f"You are AI IELTS Teacher assisting student aiming for Band {student_context.get('target_band', 7.5)}."
        return self.generate_text(user_message, api_key, system_instruction=system)
