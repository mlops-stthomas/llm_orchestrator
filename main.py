"""
LLM Orchestrator Lab - Main Entry Point

Usage:
    python main.py                          # Process all work logs (mock provider)
    python main.py --id WL-001             # Process a single work log
    python main.py --provider gemini       # Use Gemini API (needs GEMINI_API_KEY)
    python main.py --template summarize_v1 # Use the v1 prompt template
"""

import json
import argparse
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()  # Loads .env file automatically if it exists

from src.orchestrator import Orchestrator

DATA_DIR = Path(__file__).parent / "data"


def load_work_logs():
    with open(DATA_DIR / "work_logs.json") as f:
        return json.load(f)


def print_result(result):
    """Pretty-print a single processing result."""
    wl_id = result["work_log_id"]

    if result["result"]:
        r = result["result"]
        print(f"\n  --- {wl_id} Result ---")
        print(f"  Summary:    {r.get('summary', 'N/A')}")
        print(f"  Category:   {r.get('billing_category', 'N/A')}")
        print(f"  Next Steps: {r.get('next_steps', 'N/A')}")
        print(f"  Flagged:    {r.get('flagged', 'N/A')}")
        if r.get("flagged"):
            print(f"  Flag Reason: {r.get('flag_reason', 'N/A')}")
    else:
        print(f"\n  --- {wl_id} Result ---")
        print(f"  No valid result produced")

    if result["errors"]:
        print(f"  UNRESOLVED ERRORS: {result['errors']}")
    if result["retried"]:
        print(f"  (required retry)")


def main():
    parser = argparse.ArgumentParser(description="LLM Orchestrator Lab")
    parser.add_argument(
        "--id", type=str,
        help="Process a specific work log ID (e.g., WL-001)",
    )
    parser.add_argument(
        "--provider", type=str, default="mock",
        choices=["mock", "gemini"],
        help="LLM provider to use (default: mock)",
    )
    parser.add_argument(
        "--template", type=str, default="summarize_v2",
        choices=["summarize_v1", "summarize_v2"],
        help="Prompt template version (default: summarize_v2)",
    )
    args = parser.parse_args()

    print("LLM Orchestrator Lab")
    print(f"Provider: {args.provider} | Template: {args.template}")
    print("=" * 60)

    orchestrator = Orchestrator(
        provider_name=args.provider,
        template_name=args.template,
    )

    work_logs = load_work_logs()

    if args.id:
        # Process a single work log
        work_log = next((wl for wl in work_logs if wl["id"] == args.id), None)
        if not work_log:
            valid_ids = ", ".join(wl["id"] for wl in work_logs)
            print(f"Error: Work log '{args.id}' not found.")
            print(f"Valid IDs: {valid_ids}")
            return
        result = orchestrator.process_work_log(work_log)
        print_result(result)
    else:
        # Process all work logs
        results = []
        for work_log in work_logs:
            result = orchestrator.process_work_log(work_log)
            print_result(result)
            results.append(result)

        # Print summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        total = len(results)
        passed = sum(1 for r in results if not r["errors"])
        retried = sum(1 for r in results if r["retried"])
        flagged = sum(
            1 for r in results
            if r["result"] and r["result"].get("flagged")
        )
        print(f"  Total processed:    {total}")
        print(f"  Passed validation:  {passed}/{total}")
        print(f"  Required retry:     {retried}/{total}")
        print(f"  Flagged for review: {flagged}/{total}")


if __name__ == "__main__":
    main()
