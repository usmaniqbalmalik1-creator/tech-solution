from rag.chunking import chunk_text

def test_chunking():
    chunks = chunk_text(" ".join(["word"] * 100), "doc.md", size=30, overlap=10)
    assert len(chunks) > 1
    assert chunks[0].chunk_id == "doc.md:0"

def test_invalid_overlap():
    try:
        chunk_text("hello", "doc.md", size=10, overlap=10)
        assert False
    except ValueError:
        assert True
