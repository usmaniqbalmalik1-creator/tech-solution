import time
from pathlib import Path
import streamlit as st
from config import settings
from rag.chunking import chunk_text
from rag.embeddings import OpenAIEmbedder
from rag.retrieval import VectorRetriever
from rag.generation import Generator

st.set_page_config(page_title="Production RAG", page_icon="🤖", layout="wide")
st.title("🤖 Production-Style RAG Chatbot")
st.caption("FAISS retrieval • grounded generation • source inspection • evaluation-ready")

@st.cache_resource
def build_pipeline():
    text = Path("data/knowledge_base.md").read_text(encoding="utf-8")
    chunks = chunk_text(text, "knowledge_base.md", settings.chunk_size, settings.chunk_overlap)
    embedder = OpenAIEmbedder(settings.embedding_model, settings.api_key)
    vectors = embedder.embed([c.text for c in chunks])
    return embedder, VectorRetriever(chunks, vectors), Generator(settings.chat_model, settings.api_key)

if not settings.api_key:
    st.error("Set OPENAI_API_KEY in .env before starting.")
    st.stop()

embedder, retriever, generator = build_pipeline()
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about the knowledge base...")
if question:
    with st.chat_message("user"):
        st.markdown(question)

    started = time.perf_counter()
    query_vector = embedder.embed([question])
    results, retrieval_ms = retriever.search(query_vector, settings.top_k)
    answer = generator.answer(question, results, st.session_state.messages)
    total_ms = (time.perf_counter() - started) * 1000

    with st.chat_message("assistant"):
        st.markdown(answer)
        with st.expander(f"Retrieved sources · {retrieval_ms:.1f} ms retrieval · {total_ms:.1f} ms total"):
            for result in results:
                chunk = result["chunk"]
                st.markdown(f"**{chunk.chunk_id}** · similarity {result['score']:.3f}")
                st.write(chunk.text)

    st.session_state.messages.extend([
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ])
