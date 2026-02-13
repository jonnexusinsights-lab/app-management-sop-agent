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

        # Create Index from Vector Store
        # This allows LlamaIndex to query LanceDB
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store
        )

        # Create Query Engine
        # similarity_top_k=5 retrieves the 5 most relevant chunks
        self.query_engine = self.index.as_query_engine(
            llm=self.llm,
            similarity_top_k=5
        )

    def query(self, query_text: str) -> str:
        """
        Executes a RAG query.
        1. Retrieves relevant context from LanceDB.
        2. Sends context + query to Gemini.
        3. Returns the response.
        """
        response = self.query_engine.query(query_text)
        return str(response)

# Singleton instance
rag_engine = RAGEngine()
