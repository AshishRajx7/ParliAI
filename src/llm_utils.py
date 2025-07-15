from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from typing import Dict

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)

summarizer = pipeline("text-generation", model=model, tokenizer=tokenizer)

def summarize_debate(responses: Dict[str, str]) -> str:
    persona_block = "\n\n".join(f"{p}: {r}" for p, r in responses.items())
    prompt = (
        "You are an expert debate moderator. Your job is to summarize the key arguments "
        "from each persona and produce a concise, balanced, and neutral verdict.\n\n"
        f"{persona_block}\n\nSummary Verdict:"
    )

    response = summarizer(prompt, max_new_tokens=220, do_sample=True, temperature=0.7)
    return response[0]["generated_text"].replace(prompt, "").strip()
