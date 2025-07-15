from transformers import pipeline
import random
from typing import Dict

# Use summarization pipeline as a simple stand-in
generator = pipeline("text-generation", model="gpt2")

PERSONA_TEMPLATES: Dict[str, str] = {
    "Lawyer": (
        "You are a professional lawyer. Respond with a legal and ethical analysis of "
        "the following situation.\n\nSituation:\n{input}\n\n"
        "Give your argument in a formal tone and mention any legal risks."
    ),
    "Investor": (
        "You are a seasoned investor. Evaluate the financial risks and opportunities "
        "in this scenario.\n\nScenario:\n{input}\n\n"
        "Give your opinion in a strategic and profit‑focused tone."
    ),
    "Parent": (
        "You are a thoughtful and caring parent. Reflect on the emotional, safety, "
        "and family wellbeing aspects of this situation.\n\nScenario:\n{input}\n\n"
        "Respond in a warm, protective, and empathetic tone."
    ),
}

MOCK_RESPONSES = {
    "Lawyer": [
        "From a legal perspective, this may expose you to certain liabilities.",
        "You should consult legal counsel before proceeding.",
    ],
    "Investor": [
        "This might offer strong ROI but comes with significant risk.",
        "Consider whether the financial upside is worth the volatility.",
    ],
    "Parent": [
        "As a parent, I worry about the emotional impact of this decision.",
        "Think about how this could affect long‑term family wellbeing.",
    ],
}

def _mock_response(persona: str) -> str:
    return random.choice(MOCK_RESPONSES.get(persona, ["No opinion available."]))

def get_persona_response(persona: str, topic: str, use_mock: bool = False) -> str:
    prompt = PERSONA_TEMPLATES[persona].format(input=topic)

    if use_mock:
        return _mock_response(persona)

    try:
        response = generator(prompt, max_length=100, do_sample=True, num_return_sequences=1)
        return response[0]["generated_text"].strip().split("\n")[-1]
    except Exception:
        return "[LLM Error: Fallback to mock response] " + _mock_response(persona)
