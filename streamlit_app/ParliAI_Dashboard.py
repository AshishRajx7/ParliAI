import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.personas import get_persona_response
from src.llm_utils import summarize_debate
from src.debate_engine import DebateManager
from src.report_utils import generate_debate_pdf

st.set_page_config(page_title="ParliAI - Debate with AI Personas (I run it on OLLAMA)", layout="wide")
st.title(" ParliAI: Simulate a Debate with Expert Personas")
st.markdown("Describe your decision or dilemma. Let AI personas help you reason through it.")

if "responses" not in st.session_state:
    st.session_state.responses = None
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area(
    " Describe your situation or decision",
    value=st.session_state.user_input,
    height=200
)

available_personas = ["Lawyer", "Investor", "Parent"]
selected_personas = st.multiselect(
    " Choose personas to debate:",
    options=available_personas,
    default=available_personas,
)

if st.button("Run Debate") and st.session_state.user_input.strip():
    if not selected_personas:
        st.warning(" Please select at least one persona to start the debate.")
    else:
        st.subheader(" Persona Opinions")

        manager = DebateManager(topic=st.session_state.user_input, personas=selected_personas)
        responses = manager.run_debate()
        summary = manager.get_summary_verdict()

        # Store in session
        st.session_state.responses = responses
        st.session_state.summary = summary

        for persona, response in responses.items():
            with st.expander(f"{persona}'s Argument"):
                st.write(response)

        st.subheader(" Summary Verdict")
        st.success(summary)

st.subheader(" Download Report")
pdf_filename = "ParliAI_Report.pdf"

if st.button(" Generate PDF Report"):
    try:
        if st.session_state.responses and st.session_state.summary:
            generate_debate_pdf(
                pdf_filename,
                st.session_state.user_input,
                st.session_state.responses,
                st.session_state.summary
            )
            st.success(" PDF generated successfully!")

            with open(pdf_filename, "rb") as f:
                st.download_button(
                    label=" Click to Download Report",
                    data=f,
                    file_name=pdf_filename,
                    mime="application/pdf",
                )
        else:
            st.warning(" Please run a debate first before generating the report.")
    except Exception as e:
        st.error(f" Failed to generate PDF: {e}")
