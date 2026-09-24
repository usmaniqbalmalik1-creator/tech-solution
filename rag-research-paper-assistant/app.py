import os
from pathlib import Path
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()
st.title("📄 RAG Research Paper Assistant")
st.caption("Ask questions and inspect the paper passages used to answer them.")

@st.cache_resource
def load_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks, sources = [], []
    data = Path("data")
    for path in sorted(data.glob("*")):
        if path.suffix.lower() == ".pdf":
            text = "\n".join(p.extract_text() or "" for p in PdfReader(str(path)).pages)
        elif path.suffix.lower() in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8")
        else:
            continue
        words = " ".join(text.split()).split()
        for start in range(0, len(words), 130):
            part = words[start:start+160]
            if part:
                chunks.append(" ".join(part)); sources.append(path.name)
            if start + 160 >= len(words): break
    if not chunks: raise ValueError("Add PDF, TXT or MD files to data/.")
    vectors = model.encode(chunks, normalize_embeddings=True)
    return model, chunks, sources, np.asarray(vectors)

try:
    model, chunks, sources, vectors = load_index()
    st.success(f"Indexed {len(chunks)} passages.")
except ValueError as e:
    st.error(str(e)); st.stop()

q = st.text_input("Question", "What is the main contribution of the paper?")
if st.button("Ask", type="primary"):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY in .env."); st.stop()
    qv = model.encode([q], normalize_embeddings=True)[0]
    scores = vectors @ qv
    ids = np.argsort(scores)[::-1][:4]
    context = "\n\n".join(f"[{i+1}] {sources[i]}\n{chunks[i]}" for i in ids)
    client = OpenAI()
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0,
        messages=[{"role":"system","content":"Answer only from the supplied paper passages. If evidence is insufficient, say so. Cite sources as [1], [2], etc."},
                  {"role":"user","content":f"Passages:\n{context}\n\nQuestion: {q}"}])
    st.subheader("Answer"); st.write(r.choices[0].message.content)
    st.subheader("Retrieved passages")
    for rank,i in enumerate(ids,1):
        with st.expander(f"[{rank}] {sources[i]} · {scores[i]:.2f}"):
            st.write(chunks[i])
