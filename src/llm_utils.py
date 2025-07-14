import subprocess

OLLAMA_PATH = r"C:\Users\ashis\AppData\Local\Programs\Ollama\ollama.exe"

def run_ollama_llm(prompt: str, model: str = "llama3") -> str:
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
        return f" Verdict LLM Error: {e.stderr.strip()}"
def summarize_debate(responses: dict) -> str:
    bullet_points = "\n".join([f"{persona}: {resp}" for persona, resp in responses.items()])
    
    prompt = f"""You are a neutral AI judge.
Based on the following persona arguments, write a concise and thoughtful summary verdict.

Arguments:
{bullet_points}

Summary Verdict:"""

    return run_ollama_llm(prompt)
