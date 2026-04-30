"""T016: NLP pipeline — sentiment, embedding, projection, clustering.

All models are local; no network calls except first-time model download
to the local Hugging Face cache. Deterministic given fixed seeds.
"""

from __future__ import annotations

import os
import warnings

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import umap
import hdbscan


SEED = 42
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SENTIMENT_MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"
SENTIMENT_CLASS_ORDER = ("negative", "neutral", "positive")
SENTIMENT_WEIGHTS = np.array([-1.0, 0.0, 1.0], dtype=np.float32)


def seed_everything() -> None:
    np.random.seed(SEED)
    torch.manual_seed(SEED)


_EMBED_MODEL = None
_SENT_MODEL = None
_SENT_TOKENIZER = None


def get_embed_model():
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        seed_everything()
        _EMBED_MODEL = SentenceTransformer(EMBED_MODEL_NAME, device="cpu")
        _EMBED_MODEL.eval()
    return _EMBED_MODEL


def get_sentiment_model():
    global _SENT_MODEL, _SENT_TOKENIZER
    if _SENT_MODEL is None:
        seed_everything()
        _SENT_TOKENIZER = AutoTokenizer.from_pretrained(SENTIMENT_MODEL_NAME)
        _SENT_MODEL = AutoModelForSequenceClassification.from_pretrained(SENTIMENT_MODEL_NAME)
        _SENT_MODEL.eval()
    return _SENT_MODEL, _SENT_TOKENIZER


def embed(texts, batch_size=32):
    if not texts:
        return np.zeros((0, 384), dtype=np.float16)
    model = get_embed_model()
    with torch.no_grad():
        vecs = model.encode(
            list(texts),
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
    return vecs.astype(np.float16)


def score_sentiment(texts, batch_size=16):
    if not texts:
        return np.zeros(0, dtype=np.float32), []
    model, tokenizer = get_sentiment_model()
    scores = []
    labels = []
    for i in range(0, len(texts), batch_size):
        batch = list(texts[i:i + batch_size])
        enc = tokenizer(batch, padding=True, truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            logits = model(**enc).logits
        probs = torch.softmax(logits, dim=-1).cpu().numpy()
        for row in probs:
            cont = float(np.dot(row, SENTIMENT_WEIGHTS))
            scores.append(cont)
            labels.append(SENTIMENT_CLASS_ORDER[int(np.argmax(row))])
    return np.array(scores, dtype=np.float32), labels


def project_2d(vectors):
    if vectors.shape[0] == 0:
        return np.zeros((0, 2), dtype=np.float32)
    n = vectors.shape[0]
    if n < 4:
        out = np.zeros((n, 2), dtype=np.float32)
        for i in range(n):
            out[i, 0] = float(i)
        return out
    n_neighbors = max(2, min(15, n - 1))
    seed_everything()
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=n_neighbors,
        min_dist=0.05,
        metric="cosine",
        random_state=SEED,
    )
    coords = reducer.fit_transform(vectors.astype(np.float32))
    return coords.astype(np.float32)


def cluster(coords):
    n = coords.shape[0]
    if n == 0:
        return np.zeros(0, dtype=np.int32)
    if n < 8:
        return np.full(n, -1, dtype=np.int32)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=max(8, n // 50 or 8),
        min_samples=4,
    )
    labels = clusterer.fit_predict(coords)
    return labels.astype(np.int32)


def model_versions():
    return {
        "embedding": EMBED_MODEL_NAME,
        "sentiment": SENTIMENT_MODEL_NAME,
        "umap": "umap-learn random_state=" + str(SEED),
        "hdbscan": "hdbscan default (min_cluster_size>=8, min_samples=4)",
        "cluster_namer": "set by cluster_namer.py",
    }
