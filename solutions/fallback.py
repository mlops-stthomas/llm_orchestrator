"""
Fallback & Retry - SOLUTION

Copy this file to src/fallback.py if you get stuck on TODO 4.
"""

from src.output_validator import validate_response


class FallbackHandler:
    def __init__(self, provider, max_retries=1):
        self.provider = provider
        self.max_retries = max_retries

    def retry_with_feedback(self, system_prompt: str, original_prompt: str,
                            raw_response: str, errors: list,
                            work_log_id: str = None) -> tuple:
        # Build the error list as bullet points
        error_list = "\n".join(f"- {e}" for e in errors)

        # Build correction prompt
        correction_prompt = (
            f"{original_prompt}\n\n"
            f"Your previous response was:\n{raw_response}\n\n"
            f"That response had these errors:\n{error_list}\n\n"
            f"Please fix ALL of these errors and return ONLY valid JSON. "
            f"No markdown, no code fences, just the corrected JSON object."
        )

        # Call the LLM again with the correction prompt
        new_response = self.provider.generate(
            system_prompt,
            correction_prompt,
            work_log_id=work_log_id,
            is_retry=True,
        )

        # Validate the new response
        return validate_response(new_response)
