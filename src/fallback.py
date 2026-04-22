"""
Fallback & Retry - Handles validation failures by asking the LLM to fix its output.

This is TODO 4. You need to implement retry_with_feedback().

When the output validator or safety checker finds problems, we don't just
give up. Instead, we send the LLM its original response along with the
specific errors, and ask it to fix them. This is a common production pattern.

The correction prompt looks something like:
  "Your previous response had these errors:
   - Summary exceeds 50 words (got 65)
   - Forbidden word found: 'hack'
   Please fix these issues and return corrected JSON."
"""

from src.output_validator import validate_response


class FallbackHandler:
    """Retries LLM calls with error feedback when validation fails."""

    def __init__(self, provider, max_retries=1):
        self.provider = provider
        self.max_retries = max_retries

    def retry_with_feedback(self, system_prompt: str, original_prompt: str,
                            raw_response: str, errors: list,
                            work_log_id: str = None) -> tuple:
        """
        Retry the LLM call with error feedback.

        Args:
            system_prompt: The original system prompt
            original_prompt: The original user prompt
            raw_response: The LLM's response that failed validation
            errors: List of error strings (from validator + safety checker)
            work_log_id: ID for mock provider lookup

        Returns:
            Tuple of (result_dict or None, list of remaining error strings)
        """
        # =============================================
        # TODO 4: Implement retry logic
        #
        # Steps:
        #   1. Build a correction prompt string that includes:
        #      a) The original user prompt
        #      b) The LLM's previous (failed) response
        #      c) The list of errors
        #      d) Clear instruction to return corrected JSON only
        #
        #      Example format:
        #        "{original_prompt}\n\n"
        #        "Your previous response was:\n{raw_response}\n\n"
        #        "That response had these errors:\n"
        #        "- error 1\n- error 2\n\n"
        #        "Please fix ALL of these errors and return ONLY corrected JSON."
        #
        #   2. Call self.provider.generate() with:
        #      - system_prompt (same as original)
        #      - your correction prompt (as the user prompt)
        #      - work_log_id=work_log_id
        #      - is_retry=True
        #
        #   3. Validate the new response using validate_response()
        #      (imported at the top of this file)
        #
        #   4. Return the (result, errors) tuple from validate_response()
        #
        # This should be about 15 lines of code.
        # =============================================

        raise NotImplementedError("TODO 4: Implement retry_with_feedback()")
