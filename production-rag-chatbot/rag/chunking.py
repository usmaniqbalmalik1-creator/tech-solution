from dataclasses import dataclass

@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source: str
    text: str

def chunk_text(text: str, source: str, size: int = 180, overlap: int = 40) -> list[DocumentChunk]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > 0 and 0 <= overlap < size.")
    words = " ".join(text.split()).split()
    chunks = []
    step = size - overlap
    for start in range(0, len(words), step):
        part = words[start:start + size]
        if not part:
            break
        chunks.append(DocumentChunk(f"{source}:{len(chunks)}", source, " ".join(part)))
        if start + size >= len(words):
            break
    return chunks
