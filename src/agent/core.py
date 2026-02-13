from src.agent.prompts.loader import load_prompt
from src.rag.engine import rag_engine
from src.security.sanitization import PIISanitizer
from src.observability.logger import logger

class SOPAgent:
    """
    The main agent class that orchestrates the interaction.
    Handles PII sanitization, Logging, Routing, and Generation.
    """
    def __init__(self):
        self.sanitizer = PIISanitizer()
        # self.router = ... (Future implementation: load routing model/logic)

        # Load System Prompt
        # Note: We need to implement a simple prompt loader utility
        # self.system_prompt = load_prompt("system_prompt.txt")

    def process_request(self, user_query: str) -> str:
        """
        Main entry point for user queries.
        """
        # 1. Sanitize Input (Redact PII before it hits the logs or LLM)
        # Note: In a real scenario, we might want to keep the PII for the LLM
        # but strip it for logging. For strict compliance, we strip it early.
        safe_query = self.sanitizer.sanitize(user_query)

        # 2. Log the request (Audit Trail)
        logger.info(f"Received Query: {safe_query}")

        # 3. Route & Retrieve (Simple RAG for now)
        # Future: Use routing_prompt.txt to classify domain
        response = rag_engine.query(safe_query)

        # 4. Log the response
        logger.info(f"Generated Response: {response}")

        return response

# Singleton instance
sop_agent = SOPAgent()
