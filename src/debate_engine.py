from typing import List, Dict
from src.personas import get_persona_response
from src.llm_utils import summarize_debate

class DebateManager:
    def __init__(self, topic: str, personas: List[str], use_mock: bool = False):
        self.topic = topic
        self.personas = personas
        self.use_mock = use_mock
        self.responses = {}

    def run_debate(self) -> Dict[str, str]:
        self.responses = {
            persona: get_persona_response(persona, self.topic, use_mock=self.use_mock)
            for persona in self.personas
        }
        return self.responses

    def get_summary_verdict(self) -> str:
        if not self.responses:
            self.run_debate()
        return summarize_debate(self.responses)
