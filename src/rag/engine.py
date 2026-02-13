from typing import List, Optional
from llama_index.llms.gemini import Gemini
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from src.config import settings
from src.rag.storage import db_manager

class RAGEngine:
    """
    Manages the Retrieval-Augmented Generation process.
    Connects Gemini (LLM) with LanceDB (Vector Store).
    """
    def __init__(self):
        print("Initializing RAGEngine...")

        # Initialize LLM
        # Note: Ensure the API key and model name are correct in config
        self.llm = Gemini(
            model=settings.MODEL_NAME,
            api_key=settings.GOOGLE_API_KEY
        )

        # Configure Embeddings globally to avoid OpenAI defaults
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        Settings.embed_model = self.embed_model
        Settings.llm = self.llm

        # Connect to LanceDB Vector Store
        # We reuse the connection from db_manager
        self.vector_store = LanceDBVectorStore(
            uri=settings.LANCEDB_URI,
            table_name=db_manager.table_name
        )

        self.index = None
        self.query_engine = None
        self._initialize_index()

    def _initialize_index(self):
        """Attempts to initialize the index and query engine."""
        try:
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=self.vector_store
            )
            self.query_engine = self.index.as_query_engine(
                llm=self.llm,
                similarity_top_k=5
            )
            print("RAGEngine initialized successfully.")
        except Exception as e:
            print(f"RAGEngine initialization deferred: {e}")
            # It's okay if this fails initially (e.g. table doesn't exist yet)
            # We will retry on first query

    def reload(self):
        """Forces a reload of the index and query engine."""
        print("Reloading RAGEngine...")
        self._initialize_index()

    def query(self, query_text: str) -> str:
        """
        Executes a RAG query.
        1. Retrieves relevant context from LanceDB.
        2. Sends context + query to Gemini.
        3. Returns the response.
        """
        if self.query_engine is None:
            self._initialize_index()

        if self.query_engine is None:
             return "Error: Knowledge Base not initialized. Please ingest a document first."

        response = self.query_engine.query(query_text)
        return str(response)

# Singleton instance
rag_engine = RAGEngine()
