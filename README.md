# App Management SOP Agent

## Overview

The **App Management SOP Agent** is an AI-powered assistant designed to help managers retrieve and apply Standard Operating Procedures (SOPs). It uses a **Retrieval-Augmented Generation (RAG)** architecture to provide accurate, context-aware answers based on your internal documentation.

## Key Features

- **Agentic RAG:** Uses semantic chunking to preserve context.
- **Privacy-First:** All data is sanitized (PII masking) before processing.
- **Local Embeddings:** Uses **HuggingFace BAAI/bge-small-en-v1.5** for zero-cost, private vector generation.
- **Multi-Modal Storage:** Powered by **LanceDB** (embedded) for future support of text, images, and video.
- **Dual Interface:**
  - **CLI:** For administration and testing.
  - **FastAPI Web App:** For interactive chat and document ingestion (replaces Streamlit).

## Requirements

- Python 3.11+
- Google Gemini API Key (for LLM)

## Setup

> **Fast Track:** standard developers can skip to [docs/setup/QUICKSTART.md](docs/setup/QUICKSTART.md).

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/jonnexusinsights-lab/app-management-sop-agent.git
    cd app-management-sop-agent
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    # OR
    pip install -e .
    ```

3.  **Configure Environment:**
    Copy `.env.example` to `.env` and add your API keys:

    ```bash
    cp .env.example .env
    ```

    - `GOOGLE_API_KEY`: Required for Gemini 2.0 Flash.

4.  **Run the App:**

    ```bash
    # Run with uvicorn directly
    uvicorn src.api.main:app --reload

    # OR run via python script
    python src/api/main.py
    ```

    The application will be available at `http://localhost:8000`.

## Usage

### Ingestion

Go to the **Document Ingestion** tab in the Web App (`http://localhost:8000`). You can paste text directly.

- _Note: first run will download the embedding model (~130MB)._
- _Note: Creating the knowledge base happens automatically._

### Chat

Go to the **Chat with Agent** tab to ask questions about your SOPs.

## Architecture

See [docs/adr/](docs/adr/) for detailed Architectural Decision Records.

- **ADR-001:** ACE Framework Adoption
- **ADR-002:** Tech Stack
- **ADR-003:** Architectural Patterns
- **ADR-004:** Local Embeddings & Schema Management

## Troubleshooting

If you encounter "Table not initialized" errors, delete the `data/lancedb` folder and restart the app to allow the system to recreate the schema.
