"""T017: Cluster naming — local LLM preferred, TF-IDF fallback.

Per research R-7. Each cluster gets a 1–4 word `label` and a 1-sentence
`description` plus a `naming_method` tag.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


CACHE_FILE = Path(__file__).parent / ".cluster_name_cache.json"


def _load_cache() -> dict[str, dict[str, str]]:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as fh:
                return json.load(fh)
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict[str, dict[str, str]]) -> None:
    with open(CACHE_FILE, "w") as fh:
        json.dump(cache, fh, indent=2, sort_keys=True)


def _fingerprint(texts: list[str]) -> str:
    sorted_txt = "\n".join(sorted(t.strip() for t in texts))
    return hashlib.sha256(sorted_txt.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Optional local LLM via llama-cpp-python
# ---------------------------------------------------------------------------

_LLM = None
_LLM_LOAD_ATTEMPTED = False


def _try_load_local_llm():
    global _LLM, _LLM_LOAD_ATTEMPTED
    if _LLM_LOAD_ATTEMPTED:
        return _LLM
    _LLM_LOAD_ATTEMPTED = True

    model_path = os.environ.get("EXPLORER_LLAMA_MODEL_PATH")
    if not model_path or not Path(model_path).exists():
        return None
    try:
        from llama_cpp import Llama
    except ImportError:
        return None
    try:
        _LLM = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=os.cpu_count() or 4,
            verbose=False,
            seed=42,
        )
        return _LLM
    except Exception:
        _LLM = None
        return None


def _llm_name(texts: list[str]) -> tuple[str, str] | None:
    llm = _try_load_local_llm()
    if llm is None:
        return None
    sample = "\n".join(f"- {t}" for t in texts[:8])
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n"
        "You assign short cluster labels to groups of student survey responses.\n"
        "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n"
        f"These responses cluster together:\n\n{sample}\n\n"
        "Return JSON with keys 'label' (1-4 words) and 'description' (one sentence). "
        "Output JSON only, no explanation.\n"
        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    )
    try:
        out = llm(prompt, max_tokens=128, temperature=0.0, stop=["<|eot_id|>"])
        text = out["choices"][0]["text"].strip()
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return None
        obj = json.loads(m.group(0))
        label = str(obj.get("label", "")).strip()
        desc = str(obj.get("description", "")).strip()
        if label and desc:
            return label, desc
    except Exception:
        return None
    return None


# ---------------------------------------------------------------------------
# Deterministic TF-IDF fallback
# ---------------------------------------------------------------------------


def _tfidf_name(texts: list[str]) -> tuple[str, str]:
    """Pick the top 2-3 keywords by TF-IDF as a label; build a generic description."""
    cleaned = [t for t in texts if t.strip()]
    if not cleaned:
        return "Uncategorized", "Empty cluster."
    try:
        vec = TfidfVectorizer(
            stop_words="english",
            max_features=2000,
            ngram_range=(1, 2),
            min_df=1,
            max_df=1.0,
        )
        mat = vec.fit_transform(cleaned)
        scores = mat.sum(axis=0).A1
        terms = vec.get_feature_names_out()
        # Filter out single-character tokens, very generic words
        candidates = [
            (terms[i], float(scores[i]))
            for i in scores.argsort()[::-1]
            if len(terms[i]) > 2 and not terms[i].isdigit()
        ]
        # Build a 1-3 token label from the top non-overlapping unigrams
        label_parts: list[str] = []
        for term, _ in candidates:
            tokens = term.split()
            if any(any(t in lp for lp in label_parts) for t in tokens):
                continue
            label_parts.append(term)
            if len(label_parts) >= 3:
                break
        label = ", ".join(label_parts) or "Mixed responses"
        # description: use the prevailing first sentence
        first = cleaned[0].split(".")[0].strip()[:140]
        desc = (
            f"Responses centered on {label.lower()}. " +
            (f"Example: \"{first}\"" if first else "")
        ).strip()
        return label.title(), desc
    except Exception:
        return "Mixed responses", "A general grouping of responses."


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def name_cluster(representative_texts: list[str]) -> tuple[str, str, str]:
    """Return (label, description, naming_method).

    naming_method ∈ {'local_llm', 'tfidf_fallback'}
    """
    cache = _load_cache()
    fp = _fingerprint(representative_texts)
    if fp in cache:
        c = cache[fp]
        return c["label"], c["description"], c["naming_method"]

    llm_result = _llm_name(representative_texts)
    if llm_result is not None:
        label, desc = llm_result
        method = "local_llm"
    else:
        label, desc = _tfidf_name(representative_texts)
        method = "tfidf_fallback"

    cache[fp] = {
        "label": label,
        "description": desc,
        "naming_method": method,
    }
    _save_cache(cache)
    return label, desc, method


def cluster_namer_id() -> str:
    """Identifier for the cluster_namer in the bundle's model_versions field."""
    if _try_load_local_llm() is not None:
        return f"local_llm:{os.path.basename(os.environ.get('EXPLORER_LLAMA_MODEL_PATH', ''))}"
    return "tfidf_fallback:scikit-learn"
