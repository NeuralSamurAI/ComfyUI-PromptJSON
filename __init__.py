from .prompt_json import PromptJSON
from .token_counter import TokenCounter

NODE_CLASS_MAPPINGS = {
    "PromptJSON": PromptJSON,
    "TokenCounter": TokenCounter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptJSON": "Prompt JSON",
    "TokenCounter": "Token Counter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']