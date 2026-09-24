# RAG Research Paper Assistant

A document-grounded research assistant that retrieves relevant passages from research papers and generates concise answers with source references.

## Stack
Python, Sentence Transformers, NumPy, OpenAI, Streamlit

## Pipeline
PDF/TXT -> chunking -> embeddings -> semantic retrieval -> grounded LLM answer

## Run
```bash
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Put research papers in `data/`. Never commit API keys.

## Portfolio highlights
- Semantic search over papers
- Top-k retrieval
- Source-aware answers
- Designed for literature review workflows
- Clear separation between retrieval and generation
