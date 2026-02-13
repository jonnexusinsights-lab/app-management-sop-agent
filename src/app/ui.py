import streamlit as st
import os
import sys

# Pre-load torch to avoid Streamlit watcher issues
import torch

# Monkeypatch Streamlit watcher to ignore torch classes
# Fixes: RuntimeError: Tried to instantiate class '__path__._path', but it does not exist!
from streamlit.watcher import local_sources_watcher
from streamlit.watcher.local_sources_watcher import get_module_paths

def patched_get_module_paths(module):
    # Explicitly warn/skip torch.classes to avoid C++ runtime error
    if getattr(module, '__name__', '') == 'torch.classes':
        return []
    try:
        return get_module_paths(module)
    except Exception:
        # Catch generic exceptions to be safe (RuntimeError, AttributeError, etc.)
        return []

local_sources_watcher.get_module_paths = patched_get_module_paths

# Ensure project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.agent.core import sop_agent
from src.ingestion.pipeline import ingestion_pipeline
from src.config import settings

# Page Config
st.set_page_config(page_title=settings.PROJECT_NAME, layout="wide")

st.title("Managerial SOP Assistant")

# Tabs for different functions
tab1, tab2 = st.tabs(["💬 Chat with Agent", "📂 Document Ingestion"])

# --- TAB 1: Chat Interface ---
with tab1:
    st.header("SOP Guidance Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about internal SOPs..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = sop_agent.process_request(prompt)
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {e}")

# --- TAB 2: Ingestion Interface ---
with tab2:
    st.header("Ingest New SOPs")

    ingestion_type = st.radio("Source Type", ["Text", "File Upload (Coming Soon)"])

    if ingestion_type == "Text":
        sop_text = st.text_area("Paste SOP Content Here", height=300)
        source_name = st.text_input("Source Name (e.g., 'Conflict Resolution Policy v2')")

        if st.button("Ingest Document"):
            if sop_text and source_name:
                with st.spinner("Chunking and Indexing..."):
                    try:
                        ingestion_pipeline.ingest_from_text(sop_text, source=source_name)
                        # Reload RAGEngine to see new data immediately
                        from src.rag.engine import rag_engine
                        if hasattr(rag_engine, 'reload'):
                            rag_engine.reload()
                        else:
                            st.warning("Backend updated. Please restart the app to apply changes.")
                        st.success(f"Successfully ingested '{source_name}'!")
                    except Exception as e:
                        st.error(f"Ingestion failed: {e}")
            else:
                st.warning("Please provide both content and a source name.")
    else:
        st.info("File upload (PDF/Docx) will be implemented in the next iteration.")

# Sidebar for debug/info
with st.sidebar:
    st.subheader("System Info")
    st.write(f"**Model**: {settings.MODEL_NAME}")
    st.write(f"**LanceDB URI**: {settings.LANCEDB_URI}")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.experimental_rerun()
