"""Fast unit tests; no model download or API key required."""
from pathlib import Path

import pytest

from rag import read_documents


def test_loads_markdown_and_splits_long_text(tmp_path: Path):
    (tmp_path / "faq.md").write_text(" ".join(["shipping"] * 400), encoding="utf-8")
    chunks = read_documents(tmp_path)
    assert len(chunks) > 1
    assert all(chunk.source == "faq.md" for chunk in chunks)
    assert all(len(chunk.text.split()) <= 160 for chunk in chunks)


def test_ignores_unsupported_files(tmp_path: Path):
    (tmp_path / "image.png").write_bytes(b"not a document")
    assert read_documents(tmp_path) == []


def test_missing_directory_raises(tmp_path: Path):
    with pytest.raises(ValueError, match="does not exist"):
        read_documents(tmp_path / "missing")
