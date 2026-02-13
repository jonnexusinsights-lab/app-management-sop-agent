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

- `GOOGLE_API_KEY`: **Required**. Get it from [Google AI Studio](https://aistudio.google.com/).

## 3. Run Application

### Option A: Web Interface (Streamlit)

This is the primary interface for testing RAG and Chat.

```bash
streamlit run src/app/ui.py
```

_Access at: http://localhost:8501_

### Option B: CLI

Useful for automated testing or headless interactions.

```bash
python src/cli/main.py --help
```

## 4. Verification

Ingest a test document to verify the pipeline:

1.  Open the Streamlit App.
2.  Go to **Ingest Document**.
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
