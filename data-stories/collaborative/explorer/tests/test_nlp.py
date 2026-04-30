"""T026: nlp.py determinism + shape checks.

Note: these tests download models on first run (cached locally afterwards).
"""

from __future__ import annotations

import numpy as np

from pipeline import nlp


SAMPLE = [
    "I had a really fun time at the event!",
    "It was boring and I didn't learn anything new.",
    "It was okay I guess.",
]


def test_sentiment_deterministic():
    s1, l1 = nlp.score_sentiment(SAMPLE)
    s2, l2 = nlp.score_sentiment(SAMPLE)
    assert l1 == l2
    assert np.allclose(s1, s2, atol=1e-6), f"non-deterministic sentiment: {s1} vs {s2}"
    assert s1.shape == (3,)
    assert all(-1.0 <= v <= 1.0 for v in s1)


def test_sentiment_has_expected_polarity():
    s, l = nlp.score_sentiment(SAMPLE)
    # First should be most positive, second most negative
    assert l[0] == "positive", f"expected positive, got {l[0]}"
    assert l[1] == "negative", f"expected negative, got {l[1]}"


def test_embedding_shape_and_dtype():
    e = nlp.embed(SAMPLE)
    assert e.shape == (3, 384)
    assert e.dtype == np.float16


def test_umap_seeded_determinism():
    e = nlp.embed(SAMPLE)
    # Need more points than min n_neighbors for UMAP to actually run
    big = np.tile(e, (10, 1)).astype(np.float32)
    big += np.random.RandomState(0).normal(scale=0.01, size=big.shape).astype(np.float32)
    c1 = nlp.project_2d(big)
    c2 = nlp.project_2d(big)
    assert np.allclose(c1, c2, atol=1e-3), "UMAP non-deterministic with fixed seed"
