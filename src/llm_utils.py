from typing import Dict
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_debate(responses: Dict[str, str]) -> str:
    combined = "\n\n".join(f"{p}: {r}" for p, r in responses.items())
    trimmed = combined[:3500]
    summary = summarizer(trimmed, max_length=120, min_length=40, do_sample=False)[0]["summary_text"]
    return summary.strip()

def suggest_strategy(responses: Dict[str, str]) -> str:
    combined = "\n\n".join(f"{p}: {r}" for p, r in responses.items())
    trimmed = combined[:3500]
    prompt = (
        "Based on the arguments presented by each persona below, suggest a final strategy "
        "that balances their views and optimizes the outcome.\n\n"
        f"{trimmed}\n\nStrategy:"
    )
    strategy = summarizer(prompt, max_length=100, min_length=40, do_sample=False)[0]["summary_text"]
    return strategy.strip()
