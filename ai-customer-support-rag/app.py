"""Streamlit interface for the document-grounded support assistant."""
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from rag import Retriever, answer_question, read_documents

load_dotenv()
st.set_page_config(page_title="RAG Support Assistant", page_icon="📚")
st.title("📚 RAG Customer Support Assistant")
st.caption("Ask questions about your documents and inspect the retrieved sources.")

directory = st.sidebar.text_input("Knowledge-base folder", "data")
top_k = st.sidebar.slider("Retrieved passages", 1, 5, 3)
st.sidebar.info("Supports .md, .txt and text-based .pdf files.")

@st.cache_resource(show_spinner="Loading embedding model and documents...")
def build_retriever(folder: str, file_signature: tuple):
    return Retriever(read_documents(folder))

try:
    base = Path(directory)
    signature = tuple(
        (str(p), p.stat().st_mtime_ns, p.stat().st_size)
        for p in sorted(base.rglob("*"))
        if p.is_file() and p.suffix.lower() in {".md", ".txt", ".pdf"}
    ) if base.is_dir() else ()
    retriever = build_retriever(directory, signature)
    st.success(f"Loaded {len(retriever.chunks)} document passages.")
except (ValueError, OSError) as exc:
    st.error(str(exc))
    st.stop()

question = st.text_input("Your question", placeholder="What is the return policy?")
if st.button("Ask", type="primary"):
    if not question.strip():
        st.warning("Enter a question first.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY in your .env file before asking questions.")
    else:
        try:
            with st.spinner("Retrieving and generating an answer..."):
                answer, results = answer_question(question, retriever, top_k)
            st.subheader("Answer")
            st.write(answer)
            st.subheader("Retrieved sources")
            for i, (chunk, score) in enumerate(results, start=1):
                with st.expander(f"[{i}] {chunk.source} · similarity {score:.2f}"):
                    st.write(chunk.text)
        except Exception as exc:
            st.error(f"Could not generate an answer: {exc}")
