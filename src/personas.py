"""
src/personas.py
Memory‑agnostic persona generator that supports:
1) Local Ollama usage
2) Hugging Face Space fallback (no local binaries allowed)
3) Explicit mock mode for fast testing
"""

import os
import subprocess
import random
from typing import Dict

OLLAMA_PATH = r"C:\Users\ashis\AppData\Local\Programs\Ollama\ollama.exe"
OLLAMA_MODEL = "llama3"


IS_HF_SPACE = os.getenv("SPACE_ID") is not None


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


def _run_ollama(prompt: str) -> str:
    """Call Ollama locally; fall back to placeholder if binary missing."""
    if not os.path.exists(OLLAMA_PATH):
        return "[Ollama binary not found on this system]"
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", OLLAMA_MODEL],
            input=prompt,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as exc:
        return f"[Persona LLM Error] {exc.stderr.strip()}"


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
    """
    Return a persona‑specific response.
    - If use_mock=True  : always return a canned response.
    - If running on HF  : return fallback response (LLM unavailable).
    - Otherwise         : call local Ollama.
    """
    prompt = PERSONA_TEMPLATES[persona].format(input=topic)

    # Explicit mock mode
    if use_mock:
        return _mock_response(persona)

    # Hugging Face fallback (no local binaries)
    if IS_HF_SPACE:
        return "[HF fallback] Local LLM disabled on Hugging Face Spaces."

    # Normal local generation
    return _run_ollama(prompt)
