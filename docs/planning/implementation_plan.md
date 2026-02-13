# Implementation Plan: SOP Agent

## Goal Description

Build an Agentic RAG system that uses local Ollama (Llama 3) to provide SOP guidance to managers. The system will ingest multi-modal documentation from Notion/Google Docs, mask PII, and provide auditable answers via CLI and Web App.

## User Review Required

> [!IMPORTANT]
> **API Keys & Credentials**:
>
> - Ollama (Local)
> - LangSmith/Arize Phoenix API Key (for audit trails)
> - Notion API Token & Google Docs Service Account (for ingestion)

## Proposed Changes

### Core Infrastructure [Python]

#### [NEW] `pyproject.toml`

- Define project dependencies: `llama-index`, `lancedb`, `google-generativeai`, `presidio-analyzer`, `presidio-anonymizer`, `typer` (CLI), `fastapi` (API), `uvicorn`, `python-dotenv`.

#### [NEW] `src/config.py`

- Configuration management (Model selection, API keys, Paths).

#### [NEW] `src/security/sanitization.py`

- PII Masking logic using Presidio.
- Define custom recognizers if needed (e.g., internal project codes).

#### [NEW] `src/observability/logger.py`

- Integration with LangSmith or Arize Phoenix for audit trails.
- Middleware to log all LLM interactions.

### Knowledge Base & RAG [LlamaIndex + LanceDB]

#### [NEW] `src/ingestion/pipeline.py`

- Connectors for Notion and Google Docs.
- **Semantic Chunking**: Implement chunking logic based on headers and document structure.
- **Multi-modal capability**: Handle text and image/video references.

#### [NEW] `src/rag/storage.py`

- LanceDB initialization.
- Schema definition for multi-vector tables (Text Embedding, Image Embedding, Metadata).

#### [NEW] `src/rag/engine.py`

- Query engine setup using Ollama (Llama 3).
- Routing logic (Agentic behavior) to select the right retrieval strategy.

### Agentic Layer

#### [NEW] `src/agent/core.py`

- Main agent loop.
- Tool definitions (Retriever, Calculator, etc.).

#### [NEW] `src/agent/prompts/`

- Directory for curated system prompts (e.g., `manager_persona.txt`).

### Interfaces

#### [NEW] `src/cli/main.py`

- CLI entry point using Typer.
- Commands: `start`, `ingest`, `query`.

#### [NEW] `src/api/server.py`

- FastAPI server setup.
- Endpoints: `/chat`, `/ingest`, `/health`.

## Verification Plan

### Automated Tests

- **Unit Tests**: `pytest` for PII masking logic (ensure names/emails are scrubbed).
- **Integration Tests**: Verify the ingestion pipeline can read a mock Notion page.
- **Regression Tests**: Ensure previous answers to standard questions remain consistent.

### Manual Verification

1. **Ingest** a sample "Conflict Resolution" SOP (PDF/Markdown).
2. **Ask** via CLI: "How do I handle a dispute?"
3. **Verify**:
   - The answer cites the correct SOP section.
   - The PII (if any) in the logs is masked.
   - The interaction appears in the audit trail (LangSmith/Arize).
