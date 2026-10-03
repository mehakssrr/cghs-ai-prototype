
import streamlit as st
import os
PROJECT_DIR = "/content/drive/MyDrive/cghs-ai-prototype"
os.chdir(PROJECT_DIR)

from rag_utils.cghs_qa import answer_cghs_question

st.set_page_config(page_title="CGHS FAQ Chatbot", layout="wide")
st.title("CGHS – FAQ Chatbot (Prototype)")

st.markdown("""
Ask questions about CGHS (eligibility, benefits, rates, claims, etc.).
Answers are generated from **official CGHS PDFs** loaded locally.

This is a **student prototype**, not an official CGHS service.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask a CGHS question (e.g., 'Who is eligible for CGHS?'):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = answer_cghs_question(prompt)
                answer = result["answer"]
                sources = result["sources"]

                st.write(answer)

                if sources:
                    with st.expander("Sources (from CGHS PDFs)"):
                        for i, src in enumerate(sources, start=1):
                            st.write(f"**Source {i}:** {src['source']} (page {src['page']})")
                            st.text(src["text"])
            except Exception as e:
                st.error(f"Error while answering: {e}")
                st.info("Make sure you have built the FAISS index.")

    st.session_state.messages.append({"role": "assistant", "content": answer})
