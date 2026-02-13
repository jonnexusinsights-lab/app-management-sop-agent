# ADR-002: SOP Agent Architecture & Tech Stack

## Status

Accepted

## Context

We need to build a Generative AI agent to support managers with SOPs across various domains (HR, Technical, Client Mgmt). The system requires strict integrity, auditability, and the ability to process multi-modal data (text, video, audio).

## Decision

We will use the following technology stack and architecture:

1. **Core Framework**: **Python** with **LlamaIndex**.
   - _Why_: Python is the standard for AI/ML. LlamaIndex is chosen over LangChain for its superior handling of hierarchical data structures and "Agentic RAG" capabilities.

2. **Vector Database**: **LanceDB**.
   - _Why_: Native multi-modal support (text + image embeddings in one system), high performance, and embedded nature (simplifies deployment).

3. **LLM Provider**: **Ollama (Llama 3)** (Migrated from Gemini, see ADR-005).
   - _Why_: High performance/cost ratio, excellent context window, and multi-modal capabilities.

4. **Interfaces**: **Web App** and **CLI**.
   - _Why_: Web App (FastAPI) for general manager usage; CLI for administration, testing, and power users.

5. **Compliance & Integrity**:
   - **PII Masking**: **Microsoft Presidio**. Scrub active data before it leaves our perimeter.
   - **Observability**: **LangSmith** or **Arize Phoenix**. All agent actions/decisions must be logged for audit trails.

6. **Ingestion & Knowledge Base**:
   - **Inputs**: Notion text, Google Docs, PDFs, Video/Audio files.
   - **Chunking**: Semantic Chunking (based on headers/intent) rather than fixed-size sliding windows.

## Consequences

- **Positive**: Strong support for complex documents (SOPs), high integrity/security posture, and future-proofed for multi-modal data.
- **Negative**: LlamaIndex has a learning curve compared to simple LangChain chains. LanceDB is newer than Pinecone/Weaviate but offers better multi-modal alignment.

## Regressions Guards

- Any change to the PII masking layer must be verified with regression tests.
- Audit logging must never be disabled in production.
