"""
Output Validator - SOLUTION

Copy this file to src/output_validator.py if you get stuck on TODO 2.
"""

import json
from typing import Optional

from pydantic import BaseModel, ValidationError, field_validator
from enum import Enum


class BillingCategory(str, Enum):
    DEVELOPMENT = "Development"
    ANALYSIS = "Analysis"
    CONSULTATION = "Consultation"
    INFRASTRUCTURE = "Infrastructure"
    SUPPORT = "Support"


class WorkLogSummary(BaseModel):
    summary: str
    billing_category: BillingCategory
    next_steps: str
    flagged: bool
    flag_reason: Optional[str] = None

    @field_validator("summary")
    @classmethod
    def check_word_count(cls, v):
        word_count = len(v.split())
        if word_count > 50:
            raise ValueError(
                f"Summary exceeds 50 words (got {word_count})"
            )
        return v


def validate_response(raw_response: str) -> tuple:
    # Step 1: Parse JSON
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError as e:
        return None, [f"Failed to parse JSON: {e}"]

    # Step 2: Validate with Pydantic
    try:
        result = WorkLogSummary(**data)
        return result.model_dump(), []
    except ValidationError as e:
        errors = [err["msg"] for err in e.errors()]
        return data, errors
