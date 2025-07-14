# ParliAI

ParliAI is an AI-powered debate assistant that simulates expert reasoning using intelligent personas. Built with Streamlit and Ollama (LLaMA3), it helps users explore life decisions or ethical dilemmas through debates between personas like a Lawyer, Investor, or Parent. Each persona remembers its past arguments, allowing the system to evolve advice across sessions — just like a real mentor.

---

## Features

- Memory-Enabled Personas  
  Each persona remembers past conversations stored in `memory/`. Advice becomes smarter and more contextual over time.

- Multi-Persona Debate  
  Select any combination of Lawyer, Investor, and Parent to simulate diverse perspectives on your issue.

- Verdict Summary  
  A synthesized AI-generated summary helps distill the most rational path forward.

- PDF Report Generation  
  Export full debates and verdicts for documentation or sharing.

- Continue Previous Debates  
  Debates can evolve and deepen over time using memory from earlier discussions.

---

## Demo

To be added:

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/AshishRajx7/ParliAI.git
cd ParliAI
2. Create and activate a virtual environment
bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate   # On Windows
3. Install dependencies
bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
4. Start the Streamlit app
bash
Copy
Edit
streamlit run streamlit_app/ParliAI_Dashboard.py
Project Structure
bash
Copy
Edit
ParliAI/
├── memory/                  # JSON-based memory for each persona
├── src/
│   ├── personas.py          # Handles persona memory, prompt building, and responses
│   ├── debate_engine.py     # Manages the overall debate logic
│   ├── llm_utils.py         # Generates summary verdicts
│   └── report_utils.py      # Generates PDF reports
├── streamlit_app/
│   └── ParliAI_Dashboard.py # Streamlit frontend
├── requirements.txt
└── README.md
How Persona Memory Works
When a persona is used in a debate:

It loads the last 3 responses from its memory file in memory/<Persona>.json.

This memory is included in the prompt to Ollama (LLaMA3) for context.

The new response is appended back to that memory file.

Example: memory/Lawyer.json

json
Copy
Edit
[
  {
    "timestamp": "2025-07-14T10:00:00",
    "topic": "Should I leave my job?",
    "response": "Consider your financial stability and long-term goals before making the decision."
  }
]
Future Roadmap
Add new personas (e.g., Therapist, Philosopher, Startup Mentor)

Visualize memory evolution over time

Suggest follow-up questions based on debate context

Deploy to Hugging Face Spaces or Streamlit Community Cloud

