# RAG Customer Support Assistant

A portfolio-ready **Retrieval-Augmented Generation (RAG)** app that answers customer-support questions using your own documents. It retrieves relevant passages using **local sentence embeddings** and asks an OpenAI model to answer using only those passages, with numbered source citations.

## Features

- Upload knowledge by adding Markdown, TXT or text-based PDF files to the `data/` folder.
- Overlapping document chunks to preserve context.
- Semantic retrieval using `all-MiniLM-L6-v2` and in-memory cosine similarity.
- Grounded answers with `[1]`-style references and a fallback for unknown answers.
- Streamlit interface showing retrieved passages and similarity scores.
- Example FAQ and unit tests.

## Architecture

```text
Documents (.md / .txt / .pdf)
       |
       v
Text extraction -> overlapping chunks -> local embeddings
                                             |
User question -> question embedding -> cosine similarity -> top-k passages
                                                           |
                                                           v
                                           OpenAI grounded generation
                                                           |
                                                           v
                                             Answer + cited sources
```

## Quick start

Requires Python 3.10+ and an OpenAI API key. API usage may incur charges.

```bash
git clone https://github.com/usmaniqbalmalik1-creator/tech-solution.git
cd tech-solution/ai-customer-support-rag
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Windows PowerShell: Copy-Item .env.example .env
# Edit .env and set OPENAI_API_KEY
streamlit run app.py
```

The embedding model downloads on first run. Add your own documents to `data/`, then refresh the app. The included FAQ is fictional demonstration data.

## Example

**Question:** How long does standard shipping take?

**Expected behavior:** The assistant retrieves the sample shipping policy and responds that standard shipping takes 3–5 business days, citing the relevant passage. Actual wording varies by model.

## Tests

```bash
pytest -q
```

Tests cover document loading and chunking without requiring an API key or downloading the embedding model.

## Project layout

```text
ai-customer-support-rag/
├── app.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
├── data/sample_faq.md
└── tests/test_rag.py
```

## Limitations and next steps

- Retrieval is in memory; use FAISS or a hosted vector database for larger collections.
- Scanned PDFs require OCR, which is not included.
- Citation labels refer to retrieved passages; always verify consequential answers against original documents.
- For production: add authentication, upload validation, prompt-injection evaluation, monitoring, rate limits, and a human-support escalation path.

**Security:** Never commit your real `.env` file or API keys. Documents may be sent to the configured OpenAI model when generating answers.
