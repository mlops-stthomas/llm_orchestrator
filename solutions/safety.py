"""
Safety Layer - SOLUTION

Copy this file to src/safety.py if you get stuck on TODO 3.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class SafetyChecker:
    def __init__(self):
        with open(DATA_DIR / "rules.json") as f:
            rules = json.load(f)
        self.forbidden_words = [w.lower() for w in rules["forbidden_words"]]
        self.internal_tools = [t.lower() for t in rules["internal_tools"]]
        self.internal_staff = [s.lower() for s in rules["internal_staff"]]

    def check_output(self, result: dict) -> list:
        errors = []

        for field in ["summary", "next_steps"]:
            text_lower = result[field].lower()

            # Check forbidden words
            for word in self.forbidden_words:
                if word in text_lower:
                    errors.append(
                        f"Forbidden word found in {field}: '{word}'"
                    )

            # Check internal tool names
            for tool in self.internal_tools:
                if tool in text_lower:
                    errors.append(
                        f"Internal tool mentioned in {field}: '{tool}'"
                    )

            # Check internal staff names
            for name in self.internal_staff:
                if name in text_lower:
                    errors.append(
                        f"Internal staff name found in {field}: '{name}'"
                    )

        return errors
