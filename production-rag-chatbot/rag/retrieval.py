import time
import faiss
import numpy as np
from .chunking import DocumentChunk

class VectorRetriever:
    def __init__(self, chunks: list[DocumentChunk], vectors: np.ndarray):
        if len(chunks) != len(vectors):
            raise ValueError("Chunk/vector counts must match.")
        self.chunks = chunks
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(np.asarray(vectors, dtype="float32"))

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        started = time.perf_counter()
        scores, ids = self.index.search(np.asarray(query_vector, dtype="float32"), min(top_k, len(self.chunks)))
        latency_ms = (time.perf_counter() - started) * 1000
        results = [
            {"chunk": self.chunks[int(i)], "score": float(score)}
            for score, i in zip(scores[0], ids[0]) if i >= 0
        ]
        return results, latency_ms
