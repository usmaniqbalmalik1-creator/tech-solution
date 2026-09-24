import os
from pathlib import Path
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()
st.title("🏢 RAG Company Knowledge Agent")

text = Path("knowledge_base.md").read_text(encoding="utf-8")
parts = [p.strip() for p in text.split("\n## ") if p.strip()]
model = SentenceTransformer("all-MiniLM-L6-v2")
vectors = model.encode(parts, normalize_embeddings=True)

q = st.text_input("Ask the knowledge agent", "What is required before merging a pull request?")
if st.button("Ask", type="primary"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY in .env."); st.stop()
    qv = model.encode([q], normalize_embeddings=True)[0]
    scores = vectors @ qv
    ids = np.argsort(scores)[::-1][:3]
    context = "\n\n".join(f"[{n+1}] {parts[i]}" for n,i in enumerate(ids))
    client = OpenAI()
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0,
        messages=[{"role":"system","content":"You are an internal knowledge assistant. Use only the supplied context. If the answer is absent, say you do not know. Cite relevant sections as [1], [2], etc."},
                  {"role":"user","content":f"Context:\n{context}\n\nQuestion: {q}"}])
    st.subheader("Answer")
    st.write(r.choices[0].message.content)
    st.subheader("Retrieved knowledge")
    for n,i in enumerate(ids,1):
        st.write(f"**[{n}] {scores[i]:.2f}**")
        st.write(parts[i])
