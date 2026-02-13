import os

def load_prompt(prompt_name: str) -> str:
    """
    Loads a prompt file from the prompts directory.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompt_path = os.path.join(current_dir, prompt_name)

    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
