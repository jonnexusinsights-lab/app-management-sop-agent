import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")

try:
    import llama_index.core
    print(f"Llama Index Core Version: {llama_index.core.__version__}")
except Exception as e:
    print(f"Error importing llama_index.core: {e}")

try:
    from llama_index.core import Settings
    print("Successfully imported Settings from llama_index.core")
except ImportError as e:
    print(f"Error importing Settings: {e}")
    try:
        from llama_index.core import ServiceContext
        print("ServiceContext found (older version?)")
    except:
        pass

try:
    import torch
    print(f"Torch Version: {torch.__version__}")
except ImportError:
    print("Torch not found")
