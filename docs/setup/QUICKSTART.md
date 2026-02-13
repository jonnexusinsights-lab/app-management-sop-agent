# Developer Quickstart

Get up and running with the App Management SOP Agent in under 5 minutes.

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## 1. Clone & Setup

```bash
# Clone repository
git clone https://github.com/jonnexusinsights-lab/app-management-sop-agent.git
cd app-management-sop-agent

# Create virtual environment (Recommended)
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# Install dependencies (Editable mode)
pip install -e .
```

## 2. Configure Environment

```bash
# Copy example config
cp .env.example .env
# Windows Command Prompt: copy .env.example .env
```

Edit `.env` and add your API keys:

- **Ollama**: Ensure [Ollama](https://ollama.com/) is installed and running (`ollama serve`). Run `ollama pull llama3` to get the model.

## 3. Run Application

### Option A: Web Interface (FastAPI)

This is the primary interface for testing RAG and Chat.

```bash
uvicorn src.api.main:app --reload
```

_Access at: http://localhost:8000_

### Option B: CLI

Useful for automated testing or headless interactions.

```bash
python src/cli/main.py --help
```

## 4. Verification

Ingest a test document to verify the pipeline:

1.  Open the Web App (`http://localhost:8000`).
2.  Go to **Ingest**.
3.  Paste some text (e.g., "The release process requires approval from QA.").
4.  Click **Ingest**.
    - _Note: The first time, it will download the embedding model (~130MB)._
5.  Go to **Chat** and ask: "Who approves releases?"

## Troubleshooting

- **Embeddings Error / Download Failed?**
  Ensure you have an active internet connection. The system needs to download `BAAI/bge-small-en-v1.5` from Hugging Face on the first run.

- **"Table not initialized" or Schema Errors?**
  If you see errors related to `LanceDB` or schema mismatches, reset the local database:
  ```bash
  # Windows PowerShell
  Remove-Item -Recurse -Force data/lancedb
  ```
  Then restart the app and ingest a document.
