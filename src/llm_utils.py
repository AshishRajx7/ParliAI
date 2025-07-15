# src/llm_utils.py
import os
from typing import Dict
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise RuntimeError("OPENAI_API_KEY not set.")

client = OpenAI(api_key=api_key)
MODEL = "gpt-3.5-turbo"

def summarize_debate(responses: Dict[str, str]) -> str:
    persona_block = "\n\n".join(f"{p}: {r}" for p, r in responses.items())
    prompt = (
        "You are an expert debate moderator. Produce a concise (~150‑word) "
        "summary verdict that captures key arguments and suggests a balanced recommendation.\n\n"
        f"{persona_block}\n\nSummary verdict:"
    )

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=220,
    )
    return completion.choices[0].message.content.strip()
