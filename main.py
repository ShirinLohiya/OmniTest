"""
main.py
CLI entry point for the OmniTest framework.

Usage:
    python main.py data/sample_tests.json
    python main.py data/sample_tests.json --results-dir results
    python main.py data/sample_tests.json --model gpt-4
"""

import argparse
import sys

from omnitest.runner import run_tests


def main() -> None:
    parser = argparse.ArgumentParser(
        description="OmniTest — Automated Testing Framework for AI Applications",
    )
    parser.add_argument(
        "dataset",
        help="Path to the JSON test-case dataset (e.g. data/sample_tests.json)",
    )
    parser.add_argument(
        "--results-dir",
        default="results",
        help="Directory to store result logs (default: results)",
    )
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="LLM model identifier (default: gpt-3.5-turbo)",
    )
    args = parser.parse_args()

    results = run_tests(
        dataset_path=args.dataset,
        results_dir=args.results_dir,
        model=args.model,
    )

    if not results:
        sys.exit(1)


if __name__ == "__main__":
    main()
