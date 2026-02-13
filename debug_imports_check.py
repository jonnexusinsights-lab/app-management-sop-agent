try:
    print("Attempting to import llama_index.llms.gemini...")
    from llama_index.llms.gemini import Gemini
    print("Successfully imported Gemini.")
except ImportError as e:
    print(f"Failed to import Gemini: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

try:
    print("Attempting to import src.agent.core.sop_agent...")
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
    from src.agent.core import sop_agent
    print("Successfully imported sop_agent.")
except Exception as e:
    print(f"Failed to import sop_agent: {e}")
