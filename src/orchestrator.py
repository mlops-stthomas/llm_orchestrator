"""
LLM Orchestrator - Main pipeline that connects all components.

This module is PRE-BUILT. You do not need to modify it.

This is the "brain" of the system. It coordinates all the components
in the correct order:
  1. Prompt Registry   -- look up the right template
  2. Context Builder   -- assemble data for the template
  3. Prompt Renderer   -- fill in the template with data
  4. LLM Provider      -- send the prompt to the LLM
  5. Output Validator  -- check the response structure (Pydantic)
  6. Safety Checker    -- check for policy violations
  7. Fallback Handler  -- retry if anything failed

Each component is a separate module. You will implement components
2, 5, 6, and 7 as the lab TODOs.
"""

import re

from src.prompt_registry import PromptRegistry
from src.prompt_renderer import PromptRenderer
from src.context_builder import ContextBuilder
from src.llm_provider import get_provider
from src.output_validator import validate_response
from src.safety import SafetyChecker
from src.fallback import FallbackHandler


class Orchestrator:
    """Coordinates the full LLM processing pipeline."""

    def __init__(self, provider_name="mock", template_name="summarize_v2"):
        self.registry = PromptRegistry()
        self.renderer = PromptRenderer()
        self.context_builder = ContextBuilder()
        self.provider = get_provider(provider_name)
        self.safety = SafetyChecker()
        self.fallback = FallbackHandler(self.provider)
        self.template_name = template_name

    def process_work_log(self, work_log: dict) -> dict:
        """
        Process a single work log through the full pipeline.

        Args:
            work_log: Dict from work_logs.json

        Returns:
            Dict with keys: work_log_id, result, errors, retried
        """
        work_log_id = work_log["id"]
        print(f"\n{'='*60}")
        print(f"Processing: {work_log_id} - {work_log['consultant']}")
        print(f"{'='*60}")

        # Step 1: Get prompt template
        template = self.registry.get_template(self.template_name)
        print(f"  [1] Template: {template['name']}")

        # Step 2: Build context (TODO 1)
        try:
            context = self.context_builder.build_context(work_log)
            print(f"  [2] Context built: {context['project_name']} "
                  f"({context['client_name']})")
        except NotImplementedError:
            print(f"  [2] SKIPPED - TODO 1 not implemented yet")
            context = self._fallback_context(work_log)

        # Step 3: Render prompt
        system_prompt, user_prompt = self.renderer.render(template, context)
        print(f"  [3] Prompt rendered ({len(user_prompt)} chars)")

        # Step 4: Call LLM
        raw_response = self.provider.generate(
            system_prompt, user_prompt, work_log_id=work_log_id
        )
        print(f"  [4] LLM response received ({len(raw_response)} chars)")

        # Clean markdown code fences if present (LLMs often add these)
        raw_response = self._clean_response(raw_response)

        # Step 5: Validate output (TODO 2)
        try:
            result, validation_errors = validate_response(raw_response)
            if validation_errors:
                print(f"  [5] Validation FAILED: {validation_errors}")
            else:
                print(f"  [5] Validation passed")
        except NotImplementedError:
            print(f"  [5] SKIPPED - TODO 2 not implemented yet")
            import json
            result = json.loads(raw_response)
            validation_errors = []

        # Step 6: Safety check (TODO 3)
        safety_errors = []
        if result:
            try:
                safety_errors = self.safety.check_output(result)
                if safety_errors:
                    print(f"  [6] Safety FAILED: {safety_errors}")
                else:
                    print(f"  [6] Safety passed")
            except NotImplementedError:
                print(f"  [6] SKIPPED - TODO 3 not implemented yet")

        # Step 7: Retry if needed (TODO 4)
        all_errors = validation_errors + safety_errors
        if all_errors:
            try:
                print(f"  [7] Retrying with {len(all_errors)} error(s)...")
                result, remaining_errors = self.fallback.retry_with_feedback(
                    system_prompt, user_prompt, raw_response, all_errors,
                    work_log_id=work_log_id
                )
                if remaining_errors:
                    print(f"  [7] Retry still has errors: {remaining_errors}")
                else:
                    print(f"  [7] Retry successful!")
            except NotImplementedError:
                print(f"  [7] SKIPPED - TODO 4 not implemented yet")
                remaining_errors = all_errors
        else:
            remaining_errors = []
            print(f"  [7] No retry needed")

        return {
            "work_log_id": work_log_id,
            "result": result,
            "errors": remaining_errors,
            "retried": len(all_errors) > 0,
        }

    def _clean_response(self, raw_response: str) -> str:
        """Strip markdown code fences if the LLM wrapped its JSON in them."""
        text = raw_response.strip()
        # Remove ```json ... ``` or ``` ... ```
        text = re.sub(r"^```(?:json)?\s*\n?", "", text)
        text = re.sub(r"\n?```\s*$", "", text)
        return text.strip()

    def _fallback_context(self, work_log: dict) -> dict:
        """Minimal context when TODO 1 is not yet implemented."""
        return {
            "consultant": work_log["consultant"],
            "project_name": work_log["project_code"],
            "client_name": "Unknown Client",
            "date": work_log["date"],
            "hours": work_log["hours"],
            "raw_description": work_log["raw_description"],
            "max_words": 50,
            "forbidden_words": "",
            "internal_tools": "",
            "internal_names": "",
            "billing_categories": (
                "Development, Analysis, Consultation, Infrastructure, Support"
            ),
        }
