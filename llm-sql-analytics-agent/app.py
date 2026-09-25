import os,re,sqlite3,streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()
DB="analytics.db"
SCHEMA="sales(id, customer, product, category, quantity, revenue, month)"
def safe_sql(sql):
    sql=sql.strip().rstrip(";")
    if not re.match(r"^(SELECT|WITH)\\b",sql,re.I): raise ValueError("Only SELECT/WITH queries are allowed.")
    if re.search(r"\\b(INSERT|UPDATE|DELETE|DROP|ALTER|ATTACH|DETACH|REPLACE|VACUUM|PRAGMA|CREATE)\\b",sql,re.I): raise ValueError("Unsafe SQL rejected.")
    return sql
def generate(question):
    r=OpenAI().responses.create(model=os.getenv("OPENAI_MODEL","gpt-5.6-luna"),instructions="Return only one safe SQLite SELECT query using only the supplied schema. Never modify data.",input=f"Schema: {SCHEMA}\\nQuestion: {question}")
    return r.output_text
st.title("LLM SQL Analytics Agent")
q=st.text_input("Ask a business question","What is total revenue by category?")
if st.button("Run",type="primary"):
    if not os.getenv("OPENAI_API_KEY"): st.error("Set OPENAI_API_KEY."); st.stop()
    try:
        sql=safe_sql(generate(q))
        with sqlite3.connect(DB) as c:
            cur=c.execute(sql); rows=cur.fetchall(); cols=[x[0] for x in cur.description]
        st.code(sql,language="sql"); st.dataframe([dict(zip(cols,r)) for r in rows])
    except Exception as e: st.error(str(e))