from transformers import pipeline
import random
from typing import Dict

# Hugging Face text generation pipeline (small model for HF/Streamlit Cloud)
generator = pipeline("text-generation", model="gpt2")

PERSONA_TEMPLATES: Dict[str, str] = {
    "Lawyer": (
        "You are a professional lawyer. Respond with a legal and ethical analysis of "
        "the following situation:\n\n{input}\n\n"
        "Provide your analysis formally, mentioning any legal risks."
    ),
    "Investor": (
        "You are a seasoned investor. Evaluate the financial risks and opportunities "
        "in this scenario:\n\n{input}\n\n"
        "Give your insights in a strategic and profit‑focused tone."
    ),
    "Parent": (
        "You are a thoughtful parent. Reflect on the emotional and family wellbeing "
        "aspects of this situation:\n\n{input}\n\n"
        "Respond in a caring and empathetic tone."
    ),
}

MOCK_RESPONSES = {
    "Lawyer": [
        "This raises legal concerns, especially around liability.",
        "A formal review of relevant laws would be essential here.",
    ],
    "Investor": [
        "It looks promising but volatile — do a full risk-return analysis.",
        "Investment might yield gains, but caution is advised.",
    ],
    "Parent": [
        "This could deeply affect the emotional safety of the family.",
        "As a parent, I’d prioritize long-term stability and support.",
    ],
}

def _mock_response(persona: str) -> str:
    return random.choice(MOCK_RESPONSES.get(persona, ["No opinion available."]))

def get_persona_response(persona: str, topic: str, use_mock: bool = False) -> str:
    prompt = PERSONA_TEMPLATES[persona].format(input=topic)

    if use_mock:
        return _mock_response(persona)

    try:
        result = generator(prompt, max_length=120, num_return_sequences=1, do_sample=True)[0]
        return result["generated_text"].strip().split("\n")[-1]
    except Exception:
        return "[LLM Error: Fallback to mock response] " + _mock_response(persona)
