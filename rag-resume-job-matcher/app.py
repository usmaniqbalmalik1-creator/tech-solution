import os
from pathlib import Path
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from openai import OpenAI

load_dotenv()
st.title("🧑‍💻 RAG Resume & Job Matcher")
st.caption("Retrieves resume evidence before generating a grounded match analysis.")

resume = st.text_area("Paste resume", height=240)
job = st.text_area("Paste job description", height=240)

if st.button("Analyze", type="primary"):
    if not resume.strip() or not job.strip():
        st.warning("Paste both the resume and job description."); st.stop()
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Set OPENAI_API_KEY in .env."); st.stop()

    sections = [x.strip() for x in resume.split("\n\n") if x.strip()]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = model.encode(sections, normalize_embeddings=True)
    q = model.encode([job], normalize_embeddings=True)[0]
    scores = np.asarray(vectors) @ q
    ids = np.argsort(scores)[::-1][:min(5, len(sections))]
    evidence = "\n\n".join(f"[{n+1}] {sections[i]}" for n,i in enumerate(ids))

    client = OpenAI()
    r = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0,
        messages=[{"role":"system","content":"Analyze only the evidence supplied from the resume. Identify supported matches, missing evidence, and questions for the candidate. Do not infer protected traits or make hiring decisions. Cite evidence as [1], [2], etc."},
                  {"role":"user","content":f"Job description:\n{job}\n\nRetrieved resume evidence:\n{evidence}"}])
    st.subheader("Evidence-based analysis")
    st.write(r.choices[0].message.content)
    st.subheader("Retrieved resume sections")
    for n,i in enumerate(ids,1):
        st.write(f"**[{n}] Similarity {scores[i]:.2f}** — {sections[i]}")
