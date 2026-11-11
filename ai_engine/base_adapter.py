# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAIAdapter(ABC):
    def __init__(self, provider_id: str, provider_name: str):
        self.provider_id = provider_id
        self.provider_name = provider_name

    @abstractmethod
    def generate_text(self, prompt: str, api_key: str, system_instruction: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def evaluate_writing(self, prompt_text: str, submission_text: str, task_type: str, api_key: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def evaluate_speaking(self, transcript: str, prompt_text: str, part_number: int, api_key: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def teacher_chat(self, user_message: str, conversation_history: List[Dict[str, str]], student_context: Dict[str, Any], api_key: str) -> str:
        pass
