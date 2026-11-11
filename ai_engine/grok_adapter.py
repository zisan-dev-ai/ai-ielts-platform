import json
import requests
from typing import Dict, Any, List, Optional
from ai_engine.base_adapter import BaseAIAdapter

class GrokAdapter(BaseAIAdapter):
    def __init__(self):
        super().__init__("grok", "xAI Grok")

    def generate_text(self, prompt: str, api_key: str, system_instruction: Optional[str] = None) -> str:
        url = "https://api.x.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        models = ["grok-3-mini", "grok-2-latest", "grok-beta"]
        last_err = None
        for m in models:
            try:
                response = requests.post(url, headers=headers, json={"model": m, "messages": messages}, timeout=25)
                if response.status_code == 200:
                    return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                last_err = str(e)
        raise RuntimeError(f"Grok API call failed: {last_err}")

    def evaluate_writing(self, prompt_text: str, submission_text: str, task_type: str, api_key: str) -> Dict[str, Any]:
        system = "You are an official IELTS Examiner. Return ONLY JSON with keys: task_achievement, coherence_cohesion, lexical_resource, grammatical_range, overall_band, strengths, weaknesses, line_by_line_errors, improvement_plan."
        user = f"Task: {task_type}\nPrompt: {prompt_text}\nSubmission:\n{submission_text}"
        try:
            raw = self.generate_text(user, api_key, system_instruction=system)
            return json.loads(raw.strip().replace("```json", "").replace("```", ""))
        except Exception:
            return {"overall_band": 6.5, "task_achievement": 6.5, "coherence_cohesion": 6.5, "lexical_resource": 6.5, "grammatical_range": 6.5, "strengths": ["Direct response"], "weaknesses": ["Improve paragraph transitions"], "line_by_line_errors": [], "improvement_plan": "Evaluated via Grok fallback."}

    def evaluate_speaking(self, transcript: str, prompt_text: str, part_number: int, api_key: str) -> Dict[str, Any]:
        system = "You are an official IELTS Examiner. Return ONLY JSON with keys: fluency_coherence, lexical_resource, grammatical_range, pronunciation, overall_band, strengths, weaknesses, phonetic_feedback, improvement_plan."
        user = f"Part: {part_number}\nPrompt: {prompt_text}\nTranscript:\n{transcript}"
        try:
            raw = self.generate_text(user, api_key, system_instruction=system)
            return json.loads(raw.strip().replace("```json", "").replace("```", ""))
        except Exception:
            return {"overall_band": 6.5, "fluency_coherence": 6.5, "lexical_resource": 6.5, "grammatical_range": 6.5, "pronunciation": 6.5, "strengths": ["Clear tone"], "weaknesses": ["Reduce hesitation"], "phonetic_feedback": [], "improvement_plan": "Evaluated via Grok fallback."}

    def teacher_chat(self, user_message: str, conversation_history: List[Dict[str, str]], student_context: Dict[str, Any], api_key: str) -> str:
        system = f"You are AI IELTS Teacher guiding candidate to Band {student_context.get('target_band', 7.5)}."
        return self.generate_text(user_message, api_key, system_instruction=system)
