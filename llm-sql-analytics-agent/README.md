# LLM SQL Analytics Agent

Natural language -> validated read-only SQL -> SQLite -> results.

Features: schema-aware SQL generation, SQL safety validation, result display, Streamlit UI, demo sales database.

Run: `pip install -r requirements.txt`, `python seed.py`, then `streamlit run app.py`.

Only SELECT/WITH statements are accepted. Never expose production database credentials to an LLM.