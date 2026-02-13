# ADR-005: Migration to Local LLM (Ollama)

## Status

Accepted

## Context

The project initially used Google Gemini 2.0 Flash as the LLM provider. However, during development and testing, we encountered the following issues:

1. **Rate Limiting**: The free tier of Gemini API has strict rate limits (RPM/TPM), leading to `429 Too Many Requests` errors during ingestion and chat.
2. **Privacy Concerns**: Sending sensitive SOP data to an external API (even with Zero Data Retention policies) may not be suitable for all enterprise use cases.
3. **Dependency on Connectivity**: The application required constant internet access to function.

## Decision

We have decided to migrate from Google Gemini to a **local LLM execution using [Ollama](https://ollama.com/)**.

The chosen default model is **Llama 3** (via `ollama pull llama3`), but the system is configurable to use any model supported by Ollama.

## Consequences

### Positive

- **Unlimited Quota**: Local execution removes API rate limits, allowing for unrestricted testing and usage.
- **Data Privacy**: No data leaves the local machine. All processing happens within the user's infrastructure.
- **Offline Capability**: The agent can fully function without an internet connection (after initial model download).
- **Cost**: Eliminates potential future API costs.

### Negative

- **Hardware Requirements**: Running LLMs locally requires significant system resources (valid RAM and CPU/GPU).
- **Setup Complexity**: Users must install Ollama and pull models manually, adding a step to the setup process.
- **Performance**: Inference speed depends heavily on local hardware and may be slower than cloud-based APIs on lower-end machines.

## Implementation Details

- **Dependency**: Replaced `llama-index-llms-gemini` with `llama-index-llms-ollama`.
- **Configuration**: Added `OLLAMA_BASE_URL` (default: `http://localhost:11434`) to `src/config.py`.
- **Engine**: Refactored `src/rag/engine.py` to initialize `Ollama` instead of `Gemini`.
