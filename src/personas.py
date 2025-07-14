import subprocess
import random

OLLAMA_PATH = r"C:\Users\ashis\AppData\Local\Programs\Ollama\ollama.exe"
PERSONA_TEMPLATES = {
    "Lawyer": (
        "You are a professional lawyer. Respond with a legal and ethical analysis of the following situation.\n\n"
        "Situation:\n{input}\n\n"
        "Give your argument in a formal tone and mention any legal risks."
    ),
    "Investor": (
        "You are a seasoned investor. Evaluate the financial risks and opportunities in this scenario.\n\n"
        "Scenario:\n{input}\n\n"
        "Give your opinion in a strategic and profit-focused tone."
    ),
    "Parent": (
        "You are a thoughtful and caring parent. Reflect on the emotional, safety, and family wellbeing aspects of this situation.\n\n"
        "Scenario:\n{input}\n\n"
        "Respond in a warm, protective, and empathetic tone."
    ),
}

def run_ollama_prompt(prompt: str, model: str = "llama3") -> str:
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", model],
            input=prompt,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f" Persona LLM Error: {e.stderr.strip()}"

def generate_mock_response(persona: str, topic: str) -> str:
    generic_opinions = {
        "Lawyer": [
            "From a legal perspective, this may expose you to certain liabilities.",
            "You should consult legal counsel before proceeding.",
        ],
        "Investor": [
            "This might offer strong ROI, but comes with significant risk.",
            "Consider whether the financial upside is worth the volatility.",
        ],
        "Parent": [
            "As a parent, I worry about the emotional effects of this decision.",
            "Think about how this might impact long-term family wellbeing.",
        ],
    }
    return random.choice(generic_opinions.get(persona, ["No opinion."]))

def get_persona_response(persona: str, topic: str, use_mock=False) -> str:
    prompt = PERSONA_TEMPLATES[persona].format(input=topic)

    if use_mock:
        return generate_mock_response(persona, topic)
    
    return run_ollama_prompt(prompt)
