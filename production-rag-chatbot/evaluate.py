import json
from pathlib import Path
from config import settings
from rag.chunking import chunk_text
from rag.embeddings import OpenAIEmbedder
from rag.retrieval import VectorRetriever

BASE = Path(__file__).parent

def retrieval_metrics(retrieved_ids, expected_ids, ks=(1, 3, 5)):
    expected = set(expected_ids)
    first = next((i + 1 for i, value in enumerate(retrieved_ids) if value in expected), None)
    return {
        **{f"recall@{k}": float(bool(expected.intersection(retrieved_ids[:k]))) for k in ks},
        "mrr": 0.0 if first is None else 1.0 / first,
    }

def main():
    dataset = json.loads((BASE / "evaluation/dataset.json").read_text(encoding="utf-8"))
    text = (BASE / "data/knowledge_base.md").read_text(encoding="utf-8")
    chunks = chunk_text(text, "knowledge_base.md", settings.chunk_size, settings.chunk_overlap)

    if not settings.api_key:
        raise SystemExit("Set OPENAI_API_KEY before running evaluation.")

    embedder = OpenAIEmbedder(settings.embedding_model, settings.api_key)
    vectors = embedder.embed([c.text for c in chunks])
    retriever = VectorRetriever(chunks, vectors)

    totals = {"recall@1": 0.0, "recall@3": 0.0, "recall@5": 0.0, "mrr": 0.0}
    for item in dataset:
        qv = embedder.embed([item["question"]])
        results, latency = retriever.search(qv, settings.top_k)
        ids = [r["chunk"].chunk_id for r in results]
        metrics = retrieval_metrics(ids, item["expected_sources"])
        for key in totals:
            totals[key] += metrics[key]
        print(item["id"], f"retrieval_ms={latency:.1f}", metrics)

    print("\nAverage retrieval metrics")
    for key, value in totals.items():
        print(f"{key}: {value / len(dataset):.3f}")

if __name__ == "__main__":
    main()
