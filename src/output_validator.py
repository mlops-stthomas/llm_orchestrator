"""
Output Validator - Validates LLM responses using Pydantic.

This is TODO 2. You need to:
  a) Define a BillingCategory enum
  b) Define a WorkLogSummary Pydantic model with a word count validator
  c) Implement the validate_response() function

Pydantic lets us define exactly what shape the LLM's output must have.
If the LLM returns something that doesn't match (wrong type, missing field,
summary too long), Pydantic catches it with a clear error message.
"""

import json
from typing import Optional

from pydantic import BaseModel, ValidationError, field_validator
from enum import Enum


# =============================================
# TODO 2a: Define the BillingCategory enum
#
# Create a string enum with exactly these values:
#   "Development", "Analysis", "Consultation", "Infrastructure", "Support"
#
# Example:
#   class BillingCategory(str, Enum):
#       SOME_VALUE = "Some Value"
#       ...
# =============================================

# Replace this placeholder with your enum:
BillingCategory = None


# =============================================
# TODO 2b: Define the WorkLogSummary Pydantic model
#
# Fields:
#   - summary: str
#   - billing_category: BillingCategory  (uses your enum above)
#   - next_steps: str
#   - flagged: bool
#   - flag_reason: Optional[str] = None
#
# Add a @field_validator for 'summary' that:
#   - Counts the words (len(v.split()))
#   - If over 50 words, raises ValueError with the count
#   - Otherwise returns v unchanged
#
# Example validator:
#   @field_validator('summary')
#   @classmethod
#   def check_word_count(cls, v):
#       ...do your check here...
#       return v
# =============================================

# Replace this placeholder with your model:
WorkLogSummary = None


def validate_response(raw_response: str) -> tuple:
    """
    Parse and validate the LLM's raw text response.

    Args:
        raw_response: Raw string from the LLM (should be JSON)

    Returns:
        Tuple of (result_dict or None, list of error strings)
        Examples:
          - Valid:   ({"summary": "...", ...}, [])
          - Invalid: ({"summary": "...", ...}, ["Summary exceeds 50 words (got 65)"])
          - Bad JSON: (None, ["Failed to parse JSON: ..."])
    """
    # =============================================
    # TODO 2c: Implement validation
    #
    # Steps:
    #   1. Try to parse raw_response as JSON using json.loads()
    #      - If it fails, return (None, ["Failed to parse JSON: <error>"])
    #
    #   2. Try to create a WorkLogSummary from the parsed dict
    #      - result = WorkLogSummary(**parsed_data)
    #      - If valid, return (result.model_dump(), [])
    #
    #   3. If Pydantic raises ValidationError:
    #      - Extract error messages from e.errors()
    #      - Return (parsed_data, [list of error message strings])
    #
    # Hint: Pydantic's ValidationError has .errors() that returns a list
    #       of dicts, each with a "msg" key containing the error message.
    #
    # This should be about 15 lines of code.
    # =============================================

    raise NotImplementedError("TODO 2: Implement validate_response()")
