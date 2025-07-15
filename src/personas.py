from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import random
from typing import Dict

# Templates for each persona's tone and reasoning
PERSONA_TEMPLATES: Dict[str, str] = {
    "Lawyer": (
        "You are a professional lawyer. Respond with a legal and ethical analysis of "
        "the following situation.\n\nSituation:\n{input}\n\n"
        "Give your argument in a formal tone and mention any legal risks."
    ),
    "Investor": (
        "You are a seasoned investor. Evaluate the financial risks and opportunities "
        "in this scenario.\n\nScenario:\n{input}\n\n"
        "Give your opinion in a strategic and profit-focused tone."
    ),
    "Parent": (
        "You are a thoughtful and caring parent. Reflect on the emotional, safety, "
        "and family wellbeing aspects of this situation.\n\nScenario:\n{input}\n\n"
        "Respond in a warm, protective, and empathetic tone."
    ),
}

# Load the Mistral 7B instruct model
model_id = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", trust_remote_code=True)
chat = pipeline("text-generation", model=model, tokenizer=tokenizer)

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
        "Think about how this could affect long-term family wellbeing.",
    ],
}

def _mock_response(persona: str) -> str:
    return random.choice(MOCK_RESPONSES.get(persona, ["No opinion available."]))

def get_persona_response(persona: str, topic: str, use_mock: bool = False) -> str:
    if use_mock:
        return _mock_response(persona)

    if len(topic.strip().split()) < 4:
        topic = f"{topic.strip().capitalize()} — A scenario involving moral dilemmas, legal risks, and emotional consequences."

    prompt = PERSONA_TEMPLATES[persona].format(input=topic)
    prompt = f"{prompt}\n\nRespond as the {persona}."

    response = chat(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)
    return response[0]["generated_text"].replace(prompt, "").strip()
