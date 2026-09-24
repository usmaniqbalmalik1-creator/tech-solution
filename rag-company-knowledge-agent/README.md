# RAG Company Knowledge Agent

A lightweight internal knowledge assistant that answers questions from company policies, product documentation, and onboarding material.

## Architecture
Documents -> chunking -> local embeddings -> top-k retrieval -> grounded response

## Use cases
- Employee onboarding
- Product documentation
- Internal policy lookup
- Technical FAQ

## Stack
Python, Sentence Transformers, NumPy, OpenAI, Streamlit

The project is intentionally designed so the in-memory index can later be replaced with FAISS, Chroma, Qdrant, or another vector database.
