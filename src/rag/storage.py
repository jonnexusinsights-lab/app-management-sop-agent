import os
import lancedb
from src.config import settings

class LanceDBManager:
    """
    Manages LanceDB connection.
    """
    def __init__(self, uri: str = settings.LANCEDB_URI):
        self.uri = uri
        self.db = lancedb.connect(self.uri)
        self.table_name = "sop_knowledge_base"

# Singleton instance
db_manager = LanceDBManager()
