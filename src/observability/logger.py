import logging
import os

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("sop_agent")

def setup_tracing():
    """
    Initializes tracing for LangSmith/Arize.
    Ensures environment variables are set.
    """
    if os.getenv("LANGCHAIN_API_KEY"):
        logger.info("LangSmith tracing enabled.")
    else:
        logger.warning("LANGCHAIN_API_KEY not found. Tracing disabled.")
