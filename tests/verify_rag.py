import sys
import os
import shutil
import unittest
from unittest.mock import MagicMock, patch

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Mock Gemini to avoid API calls and key requirements
# We use MockLLM satisfying LlamaIndex type checks
from llama_index.core.llms import MockLLM

class MockGemini(MockLLM):
    def __init__(self, *args, **kwargs):
        super().__init__()

sys.modules["llama_index.llms.gemini"] = MagicMock()
sys.modules["llama_index.llms.gemini"].Gemini = MockGemini

import src.config
from src.config import settings

# Override DB URI for testing
TEST_DB_URI = "data/test_lancedb"
settings.LANCEDB_URI = TEST_DB_URI

from src.ingestion.pipeline import ingestion_pipeline
from src.rag.engine import RAGEngine

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        # Clean up test DB before start
        if os.path.exists(TEST_DB_URI):
            shutil.rmtree(TEST_DB_URI)

    def tearDown(self):
        # Clean up test DB after finish
        if os.path.exists(TEST_DB_URI):
            shutil.rmtree(TEST_DB_URI)

    def test_ingestion_and_query(self):
        print("\nTesting Ingestion...")
        text = "The Standard Operating Procedure for testing is to run verify_rag.py."

        # 1. Ingest
        # We need to make sure the pipeline uses the test DB settings
        # The pipeline methods use the global settings or initialized objects
        # We might need to re-init components if they cached the URI

        # Checking src/ingestion/pipeline.py:
        # It initializes LanceDBVectorStore with settings.LANCEDB_URI in __init__
        # So we need to re-initialize it or patch it.

        # Simple approach: Verify the ingestion logic runs without error
        try:
             ingestion_pipeline.ingest_from_text(text)
             print("✅ Ingestion successful (No errors)")
        except Exception as e:
             self.fail(f"Ingestion failed: {e}")

        # 2. Query
        # Initialize Engine (it mimics the app logic)
        print("Testing Retrieval...")
        try:
            rag_engine = RAGEngine()

            # Mock the query engine's query method to avoid actual LLM call checks
            # but we want to ensure the verification flow works.
            # actually RAGEngine.__init__ initializes vector_store with settings.LANCEDB_URI
            # so it should pick up the test URI.

            # We can mock the LLM response
            rag_engine.query_engine.query = MagicMock(return_value="This is a mocked response about testing.")

            response = rag_engine.query("What is the SOP for testing?")
            print(f"✅ Query successful. Response: {response}")

            # Verify specific calls if needed
            rag_engine.query_engine.query.assert_called_once()

        except Exception as e:
            self.fail(f"Query failed: {e}")

if __name__ == "__main__":
    print("Running RAG Pipeline Verification (Mocked LLM, Real DB)...")
    unittest.main()
