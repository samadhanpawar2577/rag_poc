# app.py
import streamlit as st
from services.rag_service import answer_question
from ui.layout import render_header, render_input_form, render_answer

def main():
    st.set_page_config(page_title="Databricks RAG App", layout="centered")
    render_header()

    query = render_input_form()
    if query:
        with st.spinner("Thinking..."):
            response = answer_question(query)
            render_answer("response")

if __name__ == "__main__":
    main()
