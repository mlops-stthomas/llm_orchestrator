"""
Context Builder - SOLUTION

Copy this file to src/context_builder.py if you get stuck on TODO 1.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class ContextBuilder:
    def __init__(self):
        with open(DATA_DIR / "projects.json") as f:
            self.projects = {p["code"]: p for p in json.load(f)}
        with open(DATA_DIR / "rules.json") as f:
            self.rules = json.load(f)

    def build_context(self, work_log: dict) -> dict:
        # Look up the project by code
        project = self.projects[work_log["project_code"]]

        return {
            # From the work log
            "consultant": work_log["consultant"],
            "date": work_log["date"],
            "hours": work_log["hours"],
            "raw_description": work_log["raw_description"],
            # From the project
            "project_name": project["name"],
            "client_name": project["client"],
            # From the rules (convert lists to comma-separated strings)
            "max_words": self.rules["max_words"],
            "forbidden_words": ", ".join(self.rules["forbidden_words"]),
            "internal_tools": ", ".join(self.rules["internal_tools"]),
            "internal_names": ", ".join(self.rules["internal_staff"]),
            "billing_categories": ", ".join(self.rules["billing_categories"]),
        }
