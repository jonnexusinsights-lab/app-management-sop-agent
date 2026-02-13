import sys
import os
import unittest
from unittest.mock import patch
import logging

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.observability.logger import setup_tracing

class TestAuditTrails(unittest.TestCase):
    @patch.dict(os.environ, {"LANGCHAIN_API_KEY": "test-key"}, clear=True)
    def test_tracing_enabled(self):
        with self.assertLogs("sop_agent", level="INFO") as cm:
            setup_tracing()
            self.assertTrue(any("LangSmith tracing enabled" in o for o in cm.output))
            print("\n✅ Audit Trail Config (Enabled): Verified")

    @patch.dict(os.environ, {}, clear=True)
    def test_tracing_disabled(self):
        # Remove key if present
        if "LANGCHAIN_API_KEY" in os.environ:
            del os.environ["LANGCHAIN_API_KEY"]

        with self.assertLogs("sop_agent", level="WARNING") as cm:
            setup_tracing()
            self.assertTrue(any("Tracing disabled" in o for o in cm.output))
            print("✅ Audit Trail Config (Disabled): Verified")

if __name__ == "__main__":
    print("Running Audit Trail Verification...")
    unittest.main()
