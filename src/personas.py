import os
import random
from typing import Dict
from transformers import pipeline, set_seed

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
set_seed(42)

PERSONA_TEMPLATES: Dict[str, str] = {
    "Lawyer": (
        "As a lawyer, provide a formal, ethical, and legal viewpoint on:\n{input}"
    ),
    "Investor": (
        "As a seasoned investor, give your analysis on the risks and opportunities:\n{input}"
    ),
    "Parent": (
        "As a caring parent, share your emotional and safety concerns about:\n{input}"
    ),
}

def get_persona_response(persona: str, topic: str, use_mock: bool = False) -> str:
    if use_mock:
        return _mock_response(persona)

    prompt = PERSONA_TEMPLATES[persona].format(input=topic)

    try:
        summary = summarizer(
            prompt,
            max_length=100,
            min_length=30,
            truncation=True,
            do_sample=True,
            temperature=0.7,
        )
        return summary[0]["summary_text"].strip()
    except Exception:
        return "[Model error: Unable to generate response]"

MOCK_RESPONSES = {
    "Lawyer": [
        "From a legal standpoint, this raises compliance concerns.",
        "There may be liabilities if you proceed without legal advice.",
    ],
    "Investor": [
        "This opportunity looks profitable, but carries significant risk.",
        "Evaluate your capital exposure before investing here.",
    ],
    "Parent": [
        "This could affect emotional stability of the child.",
        "Think about long-term safety and wellbeing first.",
    ],
}

def _mock_response(persona: str) -> str:
    return random.choice(MOCK_RESPONSES.get(persona, ["No opinion available."]))
