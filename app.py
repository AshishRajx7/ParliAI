import os
import sys
os.environ["STREAMLIT_HOME"] = "/tmp"
sys.path.append(os.path.join(os.path.dirname(__file__), "streamlit_app"))
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from streamlit_app import ParliAI_Dashboard
