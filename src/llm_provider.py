"""
LLM Provider - Abstraction layer for LLM API calls.

This module is PRE-BUILT. You do not need to modify it.

Provides a MockProvider (uses pre-recorded responses) and a GeminiProvider
(calls the live Gemini API). The orchestrator doesn't know or care which
provider it's using -- this is a key orchestrator design pattern.
"""

import os
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class MockProvider:
    """Returns pre-recorded responses from mock_responses.json.

    This lets you develop and test the entire pipeline without an API key.
    Some mock responses are deliberately flawed to trigger validation and
    safety checks -- this is intentional for learning purposes.
    """

    def __init__(self):
        with open(DATA_DIR / "mock_responses.json") as f:
            self.responses = json.load(f)

    def generate(self, system_prompt: str, user_prompt: str,
                 work_log_id: str = None, is_retry: bool = False) -> str:
        """Return a pre-recorded response as a JSON string."""
        key = f"{work_log_id}_retry" if is_retry else work_log_id

        if key in self.responses:
            return json.dumps(self.responses[key])

        # Fall back to the non-retry version
        if work_log_id in self.responses:
            return json.dumps(self.responses[work_log_id])

        return json.dumps({"error": f"No mock response for {work_log_id}"})


class GeminiProvider:
    """Calls the Google Gemini API.

    Requires GEMINI_API_KEY environment variable to be set.
    Get a free key at: https://aistudio.google.com/apikey
    """

    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set.\n"
                "Get a free key at: https://aistudio.google.com/apikey\n"
                "Then run: export GEMINI_API_KEY=your-key-here"
            )
        from google import genai
        self.client = genai.Client(api_key=api_key)
        self.model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(self, system_prompt: str, user_prompt: str,
                 work_log_id: str = None, is_retry: bool = False) -> str:
        """Call Gemini and return the raw text response."""
        from google.genai import types

        response = self.client.models.generate_content(
            model=self.model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        return response.text


def get_provider(name: str = "mock"):
    """Factory function to create the requested LLM provider.

    Args:
        name: "mock" for pre-recorded responses, "gemini" for live API

    Returns:
        A provider instance with a .generate() method
    """
    providers = {
        "mock": MockProvider,
        "gemini": GeminiProvider,
    }
    if name not in providers:
        available = ", ".join(providers.keys())
        raise ValueError(f"Unknown provider '{name}'. Available: {available}")
    return providers[name]()
