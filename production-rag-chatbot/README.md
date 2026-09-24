# Production-Style RAG Chatbot with Evaluation

A production-oriented Retrieval-Augmented Generation chatbot demonstrating ingestion, chunking, OpenAI embeddings, FAISS retrieval, grounded generation, source inspection, and evaluation.

## Highlights
- FAISS semantic retrieval
- OpenAI embeddings
- Grounded answers with source IDs
- Conversation history
- Recall@K and MRR retrieval evaluation
- Optional LLM answer-quality evaluation
- Streamlit UI
- Structured configuration and tests
- Clear production hardening checklist

## Architecture
Documents -> chunks -> embeddings -> FAISS -> top-k retrieval -> grounded LLM -> answer + sources

Evaluation:
gold questions -> retrieval metrics -> Recall@1/3/5 + MRR

## Setup
Python 3.10+ recommended.

    pip install -r requirements.txt
    Copy-Item .env.example .env
    streamlit run app.py

Set OPENAI_API_KEY in .env. Never commit the real key.

Run tests with:

    pytest -q

Run retrieval evaluation with:

    python evaluate.py

The evaluation dataset contains expected source IDs and reference answers. Retrieval is evaluated independently from generation so failures can be diagnosed.

## Production checklist
For a real deployment, add persistent vector storage, authentication, document-level access control, ingestion queues, retries, rate limits, PII scanning, prompt-injection testing, tracing, feedback collection, CI evaluation gates, model/version pinning, and human escalation.

This project uses the OpenAI Responses API for generation and keeps the provider layer isolated so it can be replaced later.
