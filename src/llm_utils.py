from typing import Dict
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_debate(responses: Dict[str, str]) -> str:
    persona_block = "\n\n".join(f"{p}: {r}" for p, r in responses.items())

    result = summarizer(
        persona_block,
        max_length=120,
        min_length=50,
        truncation=True,
    )
    return result[0]["summary_text"].strip()
