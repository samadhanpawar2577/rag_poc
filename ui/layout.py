# ui/layout.py
import streamlit as st

def render_header():
    st.title("📄 Databricks RAG Demo")
    st.markdown("Ask a question and get answers from your uploaded PDFs.")

def render_input_form():
    with st.form("qa_form"):
        question = st.text_input("Enter your question")
        submitted = st.form_submit_button("Get Answer")
    return question if submitted else None

def render_answer(answer):
    st.markdown("### 🧠 Answer:")
    st.success(answer["result"])
