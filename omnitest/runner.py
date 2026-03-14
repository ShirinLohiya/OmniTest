"""
runner.py
Orchestrates the test-run pipeline: load → execute → evaluate → collect.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

from omnitest.dataset_loader import load_dataset
from omnitest.llm_client import run_prompt
from omnitest.evaluator import evaluate
from omnitest.reporter import generate_report


def run_tests(
    dataset_path: str,
    results_dir: str = "results",
    model: str = "gpt-3.5-turbo",
) -> List[Dict[str, Any]]:
    """
    Execute the full OmniTest pipeline.

    1. Load test cases from the dataset.
    2. Execute each prompt via the LLM client.
    3. Run the evaluator on every response.
    4. Collect results into a flat list and save to a JSON log.

    Each result dict has the shape:
        {
            "id": "...",
            "prompt": "...",
            "response": "...",
            "pass": true/false,
            "score": 0.0–1.0,
            "latency": 0.4,
            "issues": []
        }

    Args:
        dataset_path: Path to the JSON dataset file.
        results_dir:  Directory where result logs are saved.
        model:        LLM model identifier.

    Returns:
        A list of result dictionaries (one per test case).
    """
    # 1. Load dataset -------------------------------------------------------
    test_cases = load_dataset(dataset_path)
    print(f"\n📋  Loaded {len(test_cases)} test case(s) from {dataset_path}\n")

    # 2–3. Execute prompts & evaluate ---------------------------------------
    results: List[Dict[str, Any]] = []

    for tc in test_cases:
        test_id = tc.get("id", "unknown")
        prompt = tc.get("prompt", "")
        print(f"  ▶ Running {test_id} …", end=" ")

        # Execute prompt
        llm_result = run_prompt(prompt, model=model)
        response = llm_result["response"]
        latency = llm_result["latency"]

        # Run evaluator
        eval_result = evaluate(tc, response, latency=latency)

        # Collect into flat output format
        result = {
            "id": test_id,
            "prompt": prompt,
            "response": response,
            "pass": eval_result["pass"],
            "score": eval_result["score"],
            "latency": latency,
            "issues": eval_result["issues"],
        }

        status = "✅ PASS" if result["pass"] else "❌ FAIL"
        print(status)

        results.append(result)

    # 4. Save results to JSON log -------------------------------------------
    os.makedirs(results_dir, exist_ok=True)
    log_path = Path(results_dir) / "results.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n💾  Results saved to {log_path}")

    # 5. Print summary report -----------------------------------------------
    generate_report(results)

    return results
