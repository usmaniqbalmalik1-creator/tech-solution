from evaluate import retrieval_metrics

def test_metrics():
    result = retrieval_metrics(["a", "b", "c"], ["b"])
    assert result["recall@1"] == 0.0
    assert result["recall@3"] == 1.0
    assert result["mrr"] == 0.5
