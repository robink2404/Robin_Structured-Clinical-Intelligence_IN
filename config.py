"""
Configuration & Provider settings for Clinical Document Intelligence Hub.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Default Model Provider Selection: "openai", "gemini", or "mock"
PREFERRED_PROVIDER = os.getenv("CLINICAL_AI_PROVIDER", "auto")


def get_active_provider() -> str:
    """Determine available provider based on API keys or fallback to mock."""
    if PREFERRED_PROVIDER != "auto":
        return PREFERRED_PROVIDER

    if OPENAI_API_KEY:
        return "openai"
    elif GEMINI_API_KEY:
        return "gemini"
    else:
        return "mock"
