"""
Prompt Registry - Loads and manages prompt templates from JSON.

This module is PRE-BUILT. You do not need to modify it.

The registry loads prompt templates from prompts/templates.json and provides
lookup by template name. Each template has a version, system prompt, and
user prompt with Jinja2 template variables.
"""

import json
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class PromptRegistry:
    """Manages a collection of prompt templates loaded from JSON."""

    def __init__(self, templates_path=None):
        if templates_path is None:
            templates_path = PROMPTS_DIR / "templates.json"
        with open(templates_path) as f:
            self.templates = json.load(f)

    def get_template(self, name: str) -> dict:
        """
        Retrieve a prompt template by name.

        Args:
            name: Template name (e.g., "summarize_v1", "summarize_v2")

        Returns:
            Dict with keys: version, name, system, user

        Raises:
            KeyError: If template name not found
        """
        if name not in self.templates:
            available = ", ".join(self.templates.keys())
            raise KeyError(f"Template '{name}' not found. Available: {available}")
        return self.templates[name]

    def list_templates(self) -> list:
        """Return list of available template names."""
        return list(self.templates.keys())
