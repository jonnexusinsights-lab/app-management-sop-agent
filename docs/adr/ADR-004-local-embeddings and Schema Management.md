# ADR-004: Local Embeddings and Schema Management

## Status

Accepted

## Date

2026-02-12

## Context

The project initially used Google Gemini's embedding models (`models/text-embedding-004`). We identified a need to decouple the core retrieval loop from external API dependencies to ensure:

1.  **Reliability:** Removing network latency and potential API downtime from the embedding generation process.
2.  **Privacy:** ensuring vector embeddings are generated locally.
3.  **Schema Flexibility:** Manually defining a Pydantic model (`SOPDocument`) for LanceDB caused friction with LlamaIndex's internal expectations (e.g., metadata serialization).

## Decision

### 1. Switch to Local Embeddings

We replaced Gemini embeddings with **HuggingFace's `BAAI/bge-small-en-v1.5`**.

- **Pros:**
  - **Zero Latency:** Embeddings generated on-device.
  - **Privacy:** Data never leaves the environment for vectorization.
  - **Cost:** No API usage fees.
- **Cons:**
  - **Initial Setup:** Requires downloading the model (~130MB) on first run.

### 2. Automated Schema Management

We removed the custom `SOPDocument` class. We now rely entirely on LlamaIndex's `LanceDBVectorStore` to automatically manage the table schema.

- **Pros:**
  - Eliminates type mismatch errors between Python objects and Arrow tables.
  - Reduces boilerplate code.
  - Future-proofs against LlamaIndex updates.
- **Cons:**
  - Less explicit control over physical column types.

## Consequences

- **Breaking Change:** The database schema has changed. Existing data in `data/lancedb` must be deleted (`rm -rf data/lancedb`) before restarting.
- **Dependency:** Added `llama-index-embeddings-huggingface` to `pyproject.toml`.
- **Configuration:** `src/rag/engine.py` is updated to initialize `HuggingFaceEmbedding`.
