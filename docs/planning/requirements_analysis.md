# Requirements Analysis: SOP Agent for Managers

## Goal Description

Develop a Generative AI agent to function as a Standard Operating Procedure (SOP) support system for managers. The agent will assist with people management, client/stakeholder management, new business, and technical proficiency evaluation across multiple projects and stacks.

**Key capabilities:**

1.  **Agentic RAG**: Learns from "Live" SOPs (Notion, Google Docs) with minute-level freshness.
2.  **Multi-modal Ingestion**: Handles text, transcripts, podcasts, videos, and PDFs.
3.  **Semantic Understanding**: Uses semantic chunking to preserve context (e.g., keeping "Conflict Resolution" as one unit).
4.  **Compliance & Integrity**: Includes PII masking and strict audit trails.

## Functional Requirements

1.  **Interfaces**:
    - **CLI**: For quick admin tasks and testing.
    - **Web App**: Primary interface for managers.
2.  **Multi-Domain Support**:
    - People Management
    - Client/Stakeholder Management
    - New Business Development
    - Technical Proficiency Evaluation
3.  **Knowledge Base (Agentic RAG)**:
    - **Vector DB**: LanceDB to handle multi-modal/multi-vector data (text + image embeddings).
    - **Ingestion Pipeline**: API integrations for Notion/Google Docs.
    - **Chunking Strategy**: Semantic chunking based on headers and intent.
4.  **Security & Compliance**:
    - **Audit Trails**: Log every "Manager Action" suggestion (LangSmith / Arize Phoenix).
    - **PII Masking**: Middleware layer (Presidio) to scrub sensitive data before LLM inference.
5.  **LLM**: Ollama (Llama 3).

## Proposed Architecture Logic

- **Framework**: Python + LlamaIndex (for superior hierarchical data handling).
- **Frontend**: Web App (Framework TBD) + CLI.
- **Backend API**: Python (FastAPI/Flask) to expose agent capabilities.
- **RAG Engine**:
  - **Orchestrator**: LlamaIndex workflows for routing (e.g., "Technical Eval" vs "HR Issue").
  - **Storage**: LanceDB embedded database.
  - **Middleware**: Presidio for PII scrubbing -> Audit Log -> LLM.
- **LLM Interface**: Ollama (Llama 3).

## Next Steps

1.  Formalize architecture in `docs/planning/implementation_plan.md`.
2.  Create `ADR-001` for the Tech Stack.
3.  Set up the development environment.
