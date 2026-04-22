"""
Context Builder - Assembles context from multiple data sources.

This is TODO 1. You need to implement the build_context() method.

The context builder is responsible for:
  - Looking up project metadata from projects.json
  - Loading validation rules from rules.json
  - Combining everything into a single dict that the prompt template needs

Think of this as the "data gathering" step -- before we can render a prompt,
we need to collect all the information the template references.
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


class ContextBuilder:
    """Builds template context by combining work log data with project and rule info."""

    def __init__(self):
        with open(DATA_DIR / "projects.json") as f:
            # Index projects by their code for easy lookup
            self.projects = {p["code"]: p for p in json.load(f)}
        with open(DATA_DIR / "rules.json") as f:
            self.rules = json.load(f)

    def build_context(self, work_log: dict) -> dict:
        """
        Build the template context by combining work log data, project info, and rules.

        Args:
            work_log: A dict from work_logs.json with keys:
                id, consultant, project_code, date, hours, raw_description

        Returns:
            A dict with ALL of these keys (the prompt template needs every one):
                - consultant: str (from work_log)
                - project_name: str (from projects.json, the "name" field)
                - client_name: str (from projects.json, the "client" field)
                - date: str (from work_log)
                - hours: float (from work_log)
                - raw_description: str (from work_log)
                - max_words: int (from rules.json)
                - forbidden_words: str (comma-separated, e.g. "hack, janky, clueless")
                - internal_tools: str (comma-separated, e.g. "Slack, Jira, Confluence")
                - internal_names: str (comma-separated staff names from rules.json)
                - billing_categories: str (comma-separated, e.g. "Development, Analysis, ...")

        Raises:
            KeyError: If the work log's project_code doesn't match any project
        """
        # =============================================
        # TODO 1: Implement this method
        #
        # Steps:
        #   1. Look up the project using work_log["project_code"]
        #      Hint: self.projects is a dict keyed by project code
        #
        #   2. Build and return a dict with all the keys listed above
        #      - Some come from work_log (consultant, date, hours, raw_description)
        #      - Some come from the project (project_name, client_name)
        #      - Some come from self.rules (max_words, forbidden_words, etc.)
        #
        #   3. Convert list fields to comma-separated strings
        #      Example: ["Slack", "Jira"] -> "Slack, Jira"
        #      Hint: ", ".join(some_list)
        #
        #   4. For internal_names, use the "internal_staff" key from rules
        #
        # This should be about 15 lines of code.
        # =============================================

        raise NotImplementedError("TODO 1: Implement build_context()")
