from typing import List, Dict, Any
from llama_index.core import Document, Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from src.config import settings
from src.rag.storage import db_manager

class IngestionPipeline:
    """
    Handles the ingestion of SOP documents from various sources.
    Uses Semantic Chunking to preserve context.
    """
    def __init__(self):
        # Configure HuggingFace Embeddings (Local, Low Cost)
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )
        # Set global settings to avoid default OpenAI lookups
        Settings.embed_model = self.embed_model

        # Initialize Vector Store
        self.vector_store = LanceDBVectorStore(
            uri=settings.LANCEDB_URI,
            table_name=db_manager.table_name,
        )

        # Initialize Semantic Splitter
        # This splitter uses the embedding model to identify breakpoints based on semantic similarity
        self.splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=95, embed_model=self.embed_model
        )

    def process_document(self, content: str, metadata: Dict[str, Any]):
        """
        Processes a raw document:
        1. Creates a LlamaIndex Document object.
        2. Chunks it using SemanticSplitter.
        3. Generates embeddings.
        4. Stores in LanceDB.
        """
        document = Document(text=content, metadata=metadata)

        # split document into nodes
        nodes = self.splitter.get_nodes_from_documents([document])

        # Explicitly generate embeddings for each node
        # LanceDBVectorStore.add requires embeddings to be present
        for node in nodes:
            node_embedding = self.embed_model.get_text_embedding(node.get_content())
            node.embedding = node_embedding

        # Batch insert into LanceDB using VectorStore
        # This handles metadata serialization and schema creation automatically
        self.vector_store.add(nodes)

    def ingest_from_text(self, text: str):
        """
        Convenience method for testing/CLI.
        """
        self.process_document(text, {"source_type": "text"})

# Singleton instance
ingestion_pipeline = IngestionPipeline()
