# Pinned model versions

For reproducibility. If any of these change, the bundle's
`model_versions` field (see `contracts/data-bundle.schema.json`) updates
to match, and the build's deterministic outputs may shift.

## Embedding model

- **Name**: `sentence-transformers/all-MiniLM-L6-v2`
- **Revision** (Hugging Face commit, recorded at first download): `8b3219a92973c328a8e22fadcfa821b5dc75636a` (verified via `huggingface-cli download <repo> --revision <rev>`)
- **Dimensionality**: 384
- **Storage in bundle**: float16

## Sentiment model

- **Name**: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- **Revision**: `4ba3d4463bd152039f4bc6db4d20b0489d488e02`
- **Output classes**: negative / neutral / positive (probabilities → continuous score in [-1, +1])

## UMAP

- **Library**: `umap-learn==0.5.7`
- **Params**: `n_neighbors=15, min_dist=0.05, metric='cosine', random_state=42`

## HDBSCAN

- **Library**: `hdbscan==0.8.40`
- **Params**: `min_cluster_size=8, min_samples=4`

## Cluster namer (preferred)

- **Name**: `Llama-3.1-8B-Instruct` (quantized GGUF Q4_K_M)
- **Source**: `bartowski/Meta-Llama-3.1-8B-Instruct-GGUF`
- **File**: `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`
- **Library**: `llama-cpp-python==0.3.5`
- **Sampling**: `temperature=0.0` (deterministic), `max_tokens=64`

## Cluster namer (fallback)

- **Method**: scikit-learn TF-IDF top-3-phrase summarizer
- **Library**: `scikit-learn==1.5.2`

## Determinism seeds

- `numpy.random.seed(42)`
- `torch.manual_seed(42)`
- UMAP `random_state=42`
- HDBSCAN: not seedable, but its inputs (UMAP coords) are deterministic so its outputs are too
