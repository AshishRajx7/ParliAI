import os
from typing import Dict
import openai

_OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if _OPENAI_KEY is None:
    try:
        import streamlit as st  # imported only if running inside Streamlit
        _OPENAI_KEY = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise RuntimeError(
            "OPENAI_API_KEY not found. "
            "Set it as an environment variable or in .streamlit/secrets.toml"
        )

openai.api_key = _OPENAI_KEY
MODEL = "gpt-3.5-turbo"      # or gpt-4o, gpt-4o-mini, etc.


def summarize_debate(responses: Dict[str, str]) -> str:
    """
    Combine persona responses into a concise summary verdict.
    """
    persona_block = "\n\n".join(
        f"{name}: {text}" for name, text in responses.items()
    )
    prompt = (
        "You are an expert debate moderator. Produce a concise (≈150‑word) "
        "summary verdict that captures the key points of agreement and disagreement, "
        "then recommend a balanced course of action.\n\n"
        f"Persona arguments:\n{persona_block}\n\n"
        "Summary verdict:"
    )

    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=220,
    )
    return completion.choices[0].message.content.strip()
