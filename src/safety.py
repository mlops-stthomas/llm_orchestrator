"""
Safety Layer - Checks LLM output for policy violations.

This is TODO 3. You need to implement check_output().

The safety layer runs AFTER Pydantic validation. Even if the response has
the right structure and types, it might still contain content that shouldn't
appear in a client-facing summary:
  - Forbidden words (unprofessional language)
  - Internal tool names (Slack, Jira, etc.)
  - Internal staff names

In a production system, this layer would also check for PII, toxicity,
prompt injection attempts, and more. Here we focus on the basics.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class SafetyChecker:
    """Checks LLM output for forbidden content."""

    def __init__(self):
        with open(DATA_DIR / "rules.json") as f:
            rules = json.load(f)
        self.forbidden_words = [w.lower() for w in rules["forbidden_words"]]
        self.internal_tools = [t.lower() for t in rules["internal_tools"]]
        self.internal_staff = [s.lower() for s in rules["internal_staff"]]

    def check_output(self, result: dict) -> list:
        """
        Check the validated output for safety violations.

        Args:
            result: Dict with keys: summary, billing_category,
                    next_steps, flagged, flag_reason

        Returns:
            List of error strings. Empty list = output is safe.
            Example errors:
              - "Forbidden word found in summary: 'hack'"
              - "Internal tool mentioned in next_steps: 'jira'"
              - "Internal staff name found in summary: 'sarah kim'"
        """
        # =============================================
        # TODO 3: Implement safety checking
        #
        # Check BOTH the 'summary' and 'next_steps' fields for violations.
        #
        # For each field, check three things:
        #
        #   1. Forbidden words (self.forbidden_words)
        #      - For each forbidden word, check if it appears in the text
        #      - Use case-insensitive comparison (convert text to lowercase)
        #      - Add: "Forbidden word found in {field}: '{word}'"
        #
        #   2. Internal tool names (self.internal_tools)
        #      - Check if any tool name appears in the text
        #      - Add: "Internal tool mentioned in {field}: '{tool}'"
        #
        #   3. Internal staff names (self.internal_staff)
        #      - Check if any staff name appears in the text
        #      - Add: "Internal staff name found in {field}: '{name}'"
        #
        # Hint: Loop over the two fields ["summary", "next_steps"]
        # Hint: text_lower = result[field].lower()
        # Hint: `if word in text_lower` works for substring matching
        #
        # This should be about 20 lines of code.
        # =============================================

        raise NotImplementedError("TODO 3: Implement check_output()")
