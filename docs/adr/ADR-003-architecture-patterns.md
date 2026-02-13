# ADR-003: Architectural Patterns & Agent Implementation

## Status

Accepted

## Context

Following the technology selection in ADR-001 and ADR-002, we have implemented the core infrastructure. We need to formalize the specific architectural patterns used in the implementation to ensure consistency, scalability, and adherence to the "Agentic" requirements.

## Decision

We have adopted the following architectural patterns:

### 1. Agentic RAG with Semantic Chunking

**Decision**: Instead of standard fixed-size chunking, we use **Semantic Chunking** (via LlamaIndex `SemanticSplitterNodeParser`).
**Reasoning**: Managerial SOPs often contain distinct sections (e.g., "Conflict Resolution", "Hiring Process") that must be retrieved as complete units. Fixed-size chunking risks splitting context mid-sentence or mid-policy, leading to hallucinated or incomplete advice.

### 2. Privacy-First Middleware Pipeline

**Decision**: All user input passes through a **PII Sanitization Layer** (`src/security/sanitization.py`) _before_ reaching the logging system or the Query Engine.
**Reasoning**: To comply with "Agent Integrity" requirements, we ensure that sensitive employee or client data is stripped at the edge. This decoupling allows us to change LLM providers without leaking PII.

### 3. Embedded Multi-Modal Storage

**Decision**: We utilize **LanceDB** in embedded mode.
**Reasoning**:

- **Embedded**: Removes the need for managing a separate Docker container for a Vector, simplifying the deployment to a CLI/Local App.
- **Multi-Modal**: Prepares the system for future video/audio ingestion without schema migrations.

### 4. Router-Solver Pattern

**Decision**: The Agent (`src/agent/core.py`) is designed to use a **Router** (classifier) to determine the domain (HR, Tech, Business) before delegating to specific retrieval tools.
**Reasoning**: Generalist RAG often fails on specific domain jargon. By routing first, we can (in the future) swap in specialized prompts or indices for specific domains.

## Consequences

- **Positive**: Higher quality responses due to context preservation; strict PII compliance; robust local deployment capability.
- **Negative**: Semantic chunking is more computationally expensive during ingestion.

## Compliance Verification

- Tests must verify that the `PIISanitizer` is invoked in `process_request`.
- Ingestion logs must confirm the use of `SemanticSplitterNodeParser`.
