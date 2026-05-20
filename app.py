import streamlit as st
import google.generativeai as genai

# Set up the visual layout of the app
st.set_page_config(page_title="BA Accelerator POC", layout="wide")
st.title("AI Business Analyst Accelerator")
st.write ("Convert messy stakeholder notes into a structured Functional Requirements Document (FRD).")

# Securly ask for the PI key in the sidebar (so it isn't hardcoded)
with st.sidebar:
  st.header("settings")
  api_key = st.text_input("Enter Gemini API Key:", type="password")
  st.write("*(Get a free key from Google AI Studio)*")

# The System prompt we designed earlier
sys_prompt = """
You are a Senior Business Analyst expert. Convert the user's raw notes into a standard FRD format.
Rules:
1. No Hallucinations. Base requirements strictly on the provided context.
2. Use "The system shall..." for all requirements.
3. Assign a unique ID to every requirement (e.g., FR-01).

Output format must be Markdown:
# Functional Requirements Document (FRD)
## 1. Introduction (Purpose & Scope)
## 2. Assumptions & Dependencies
## 3. Functional Requirements (Table with ID, Description, Priority)
## 4. Non-Funtional Requirements (Table with ID, Description, Category)
## 5. Open Questions for Stakeholders
"""

# The main input aread for the BA
raw_notes = st.text_area(" Paste Stakeholder Meeting Notes Here:", height=200)

# The "Generate" button
if st.button ("Generate FRD"):
  if not api_key:
    st.error("Please enter your API key in the sidebar first.")
  elif not raw_notes:
     st.error("Please paste some meeting notes to process.")
  else:
       with st.spinner("Analyzing notes and drafting FRD..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-pro",
                    system_instruction=sys_prompt
                )
                response = model.generate_content(raw_notes)
                st.success("Draft Complete!")
                st.markdown("---")
                st.markdown(response.text)
      
            except Exception as e:
                st.error(f"An error occured: {e}")
