# LLM Orchestrator Lab: Work Log Summarizer

## Overview

In this lab you'll build a working LLM orchestrator pipeline that transforms messy, internal consultant work logs into clean, client-facing summaries. The system enforces strict rules: word limits, forbidden words, no internal names or tools leaking through, and professional tone.

You'll implement four core orchestrator components, each in its own file, then run the full pipeline and observe how the pieces work together.

**Time:** ~45 minutes

## Learning Objectives

- Understand the role of each component in an LLM orchestrator pipeline
- Build a **context builder** that assembles data from multiple sources
- Use **Pydantic** to validate LLM output as structured data
- Implement a **safety layer** that catches policy violations
- Build **fallback/retry logic** that asks the LLM to fix its own mistakes
- See how prompt template design affects output quality

## Prerequisites

- Python 3.10+
- A Google account (optional, for free Gemini API access)

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd llm_orchestrator

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Optional: Get a Free Gemini API Key

The lab works fully in **mock mode** (no API key needed). To also try it with a live LLM:

1. Go to [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the example env file and add your key:

```bash
cp .env.example .env
# Edit .env and replace "your-api-key-here" with your actual key
```

The `.env` file is loaded automatically when you run `main.py` (via python-dotenv). No need to export variables in your terminal.

5. Verify which models are available on your free tier at [https://ai.dev/rate-limit](https://ai.dev/rate-limit). The default model is `gemini-2.5-flash`. If you need a different model, set `GEMINI_MODEL` in your `.env` file.

## The Scenario

You work for a consulting firm. Consultants write work logs like this:

> "Spent most of the morning debugging the janky ETL pipeline. Turns out their API was sending garbage null values. Had to hack together a workaround. Pinged Mike on Slack about it."

Your orchestrator must produce client-facing summaries like this:

```json
{
  "summary": "Debugged ETL pipeline issues caused by null values in external API responses. Implemented coalesce functions to ensure proper data handling.",
  "billing_category": "Infrastructure",
  "next_steps": "Monitor API response quality and implement permanent null handling solution.",
  "flagged": false,
  "flag_reason": null
}
```

**Rules enforced:**
- Summary must be under 50 words
- No forbidden words ("hack", "janky", "garbage", "stupid", etc.)
- No internal staff names or tool names (Slack, Jira, etc.)
- Professional, third-person tone
- Billing category must be a valid enum value
- Flagged if original log had unprofessional content

## Architecture

```
                        work_logs.json
                             |
                             v
                    +------------------+
                    | Prompt Registry  |  <-- prompts/templates.json
                    +------------------+
                             |
                             v
projects.json --> +------------------+
rules.json   --> | Context Builder  |  <-- TODO 1
                    +------------------+
                             |
                             v
                    +------------------+
                    | Prompt Renderer  |  (Jinja2 templates)
                    +------------------+
                             |
                             v
                    +------------------+
                    |   LLM Provider   |  (Mock or Gemini)
                    +------------------+
                             |
                             v
                    +------------------+
                    | Output Validator |  <-- TODO 2 (Pydantic)
                    +------------------+
                             |
                             v
                    +------------------+
                    |  Safety Checker  |  <-- TODO 3
                    +------------------+
                             |
                        errors? ----yes----> +------------------+
                             |               | Fallback Handler |  <-- TODO 4
                             no              +------------------+
                             |                       |
                             v                       v
                    +------------------+     (retry LLM call)
                    |   Final Result   |
                    +------------------+
```

## Project Structure

```
llm_orchestrator/
├── main.py                     # Entry point (run this)
├── requirements.txt
├── .env.example
├── data/
│   ├── work_logs.json          # 10 messy consultant work logs
│   ├── projects.json           # Project metadata (client names, codes)
│   ├── rules.json              # Validation rules (forbidden words, limits)
│   └── mock_responses.json     # Pre-recorded LLM responses for mock mode
├── prompts/
│   └── templates.json          # v1 and v2 prompt templates
├── src/
│   ├── orchestrator.py         # Main pipeline (pre-built, connects everything)
│   ├── prompt_registry.py      # Template loader (pre-built)
│   ├── prompt_renderer.py      # Jinja2 renderer (pre-built)
│   ├── llm_provider.py         # Mock + Gemini providers (pre-built)
│   ├── context_builder.py      # TODO 1: You implement this
│   ├── output_validator.py     # TODO 2: You implement this
│   ├── safety.py               # TODO 3: You implement this
│   └── fallback.py             # TODO 4: You implement this
└── solutions/                  # Complete solutions (don't peek yet!)
    ├── context_builder.py
    ├── output_validator.py
    ├── safety.py
    └── fallback.py
```

## Lab Instructions

You can run the pipeline at any point during the lab. Unimplemented TODOs will be skipped with a message so you can test incrementally.

```bash
# Run the full pipeline (will show SKIPPED for unfinished TODOs)
python main.py

# Run a single work log
python main.py --id WL-001
```

---

### TODO 1: Context Builder (~10 minutes)

**File:** `src/context_builder.py`

The context builder gathers data from multiple sources and assembles it into a single dictionary that the prompt template needs. This is the "data gathering" step of the orchestrator.

**Your task:** Implement `build_context()` which:
1. Looks up the project from `projects.json` using the work log's `project_code`
2. Loads rules from `rules.json`
3. Returns a dict with all template variables (see docstring for the full list)
4. Converts list fields to comma-separated strings

**Test it:**
```bash
python main.py --id WL-001
# Should show: [2] Context built: Data Migration Platform (Acme Corporation)
# Instead of: [2] SKIPPED
```

---

### TODO 2: Output Validator (~10 minutes)

**File:** `src/output_validator.py`

The output validator uses Pydantic to enforce that the LLM's response has the exact structure and values we expect. This is how you turn unstructured LLM text into reliable, typed data.

**Your task:**
1. Define a `BillingCategory` string enum with the 5 valid categories
2. Define a `WorkLogSummary` Pydantic model with a word-count validator on `summary`
3. Implement `validate_response()` that parses JSON and validates with Pydantic

**Test it:**
```bash
python main.py --id WL-005
# WL-005 has a mock response that's deliberately too long (>50 words)
# Should show: [5] Validation FAILED: ["Summary exceeds 50 words (got ...)"]
```

---

### TODO 3: Safety Layer (~10 minutes)

**File:** `src/safety.py`

Even after Pydantic validation passes, the content might still violate policies. The safety layer catches forbidden words, internal tool references, and staff names that shouldn't appear in client-facing output.

**Your task:** Implement `check_output()` which scans the `summary` and `next_steps` fields for:
- Forbidden words (from `rules.json`)
- Internal tool names (Slack, Jira, etc.)
- Internal staff names

**Test it:**
```bash
python main.py --id WL-002
# WL-002's mock response contains "hack" -- should trigger safety
# Should show: [6] Safety FAILED: ["Forbidden word found in summary: 'hack'"]

python main.py --id WL-004
# WL-004's mock response mentions "Jira" and "Confluence"
# Should show: [6] Safety FAILED: ["Internal tool mentioned in summary: 'jira'", ...]
```

---

### TODO 4: Fallback Handler (~10 minutes)

**File:** `src/fallback.py`

When validation or safety checks fail, the fallback handler sends the errors back to the LLM and asks it to fix its response. This retry pattern is critical in production -- LLMs are probabilistic, and a second attempt with specific error feedback usually succeeds.

**Your task:** Implement `retry_with_feedback()` which:
1. Builds a correction prompt that includes the original prompt, the failed response, and the specific errors
2. Calls the LLM provider again (with `is_retry=True`)
3. Validates the new response

**Test it:**
```bash
python main.py --id WL-002
# Should show:
#   [6] Safety FAILED: [...]
#   [7] Retrying with 1 error(s)...
#   [7] Retry successful!

python main.py --id WL-005
# Should show:
#   [5] Validation FAILED: [...]
#   [7] Retrying with 1 error(s)...
#   [7] Retry successful!
```

---

### Run the Full Pipeline (~5 minutes)

Once all TODOs are implemented, process all 10 work logs:

```bash
python main.py
```

**Expected output:**
- **7 work logs** pass cleanly on the first try
- **3 work logs** (WL-002, WL-004, WL-005) fail validation/safety and get retried
- **2 work logs** (WL-003, WL-007) are flagged for human review
- All 10 should produce valid results after retries

Look at the summary at the bottom:
```
SUMMARY
  Total processed:    10
  Passed validation:  10/10
  Required retry:     3/10
  Flagged for review: 2/10
```

## Try It with Gemini (Optional)

If you set up a Gemini API key:

```bash
export GEMINI_API_KEY=your-key-here
python main.py --provider gemini --id WL-002
```

Compare the live Gemini output with the mock responses. Does it pass validation on the first try? Do the v1 and v2 templates produce different results?

```bash
# Compare prompt template versions
python main.py --provider gemini --template summarize_v1 --id WL-007
python main.py --provider gemini --template summarize_v2 --id WL-007
```

## Stretch Goals

If you finish early, try these:

1. **Add a new forbidden word** to `rules.json` that causes a previously-passing work log to fail safety. Run the pipeline and see it trigger a retry.

2. **Add a new work log** to `work_logs.json` with tricky content. Process it with the Gemini provider and see how well the orchestrator handles it.

3. **Tighten the word limit** in `rules.json` (e.g., 30 words instead of 50). How many more retries does this cause?

4. **Compare v1 vs v2 templates** with Gemini. The v1 template is intentionally weaker. How does it affect compliance rates?

5. **Add a new prompt template** (v3) to `prompts/templates.json`. Can you write a prompt that gets 100% compliance on the first try?

## What's Next?

This lab built a **single pipeline** -- one input type, one processing path. Next week we'll extend this into an **agent** that can:
- **Route** different types of requests to different pipelines
- **Use tools** to look up information dynamically
- **Loop** autonomously until a task is complete
- **Manage state** across multi-turn conversations

The orchestrator you built today becomes one component inside a larger agent system.

## Troubleshooting

**"ModuleNotFoundError: No module named 'pydantic'"**
Make sure you activated your virtual environment and ran `pip install -r requirements.txt`.

**"GEMINI_API_KEY environment variable not set"**
You're using `--provider gemini` without setting the key. Either set it or use the default mock mode.

**"429 RESOURCE_EXHAUSTED" or "quota exceeded"**
The model you're using isn't available on your free tier. Check which models have quota at [https://ai.dev/rate-limit](https://ai.dev/rate-limit), then set the model:
```bash
export GEMINI_MODEL=gemini-2.5-flash
```

**A TODO shows SKIPPED**
That TODO hasn't been implemented yet. Open the corresponding file in `src/` and look for the TODO comment.

**Stuck on a TODO?**
Solution files are in the `solutions/` directory. You can copy a solution into `src/` to unblock yourself:
```bash
cp solutions/context_builder.py src/context_builder.py
```
