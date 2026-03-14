# 🧪 OmniTest

**Automated Testing Framework for AI Applications**

OmniTest is a modular Python framework for testing LLM-powered applications. It loads test cases from JSON datasets, sends prompts to an LLM, evaluates responses using rule-based checks, and generates structured reports — all from a single CLI command.

---

## Architecture

```
                    ┌──────────────┐
                    │   main.py    │  CLI entry point
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  runner.py   │  Orchestrates the pipeline
                    └──┬───┬───┬──┘
                       │   │   │
          ┌────────────┘   │   └────────────┐
          ▼                ▼                ▼
  ┌───────────────┐ ┌─────────────┐ ┌──────────────┐
  │dataset_loader │ │ llm_client  │ │  evaluator   │
  │     .py       │ │    .py      │ │     .py      │
  └───────────────┘ └─────────────┘ └──────────────┘
    Load JSON          Send prompt     Keyword, forbidden
    test cases         to LLM          & latency checks
                                              │
                                       ┌──────▼───────┐
                                       │ reporter.py  │
                                       └──────────────┘
                                        Console summary
                                        + results.json
```

## Project Structure

```
omnitest/
├── __init__.py
├── dataset_loader.py    # Load test cases from JSON
├── llm_client.py        # LLM interface (mock + OpenAI)
├── evaluator.py         # Rule-based response evaluation
├── runner.py            # Test execution pipeline
└── reporter.py          # Summary report generation
tests/
└── test_evaluator.py    # Unit tests for the evaluator
data/
└── sample_tests.json    # 10 sample test cases
results/
└── results.json         # Generated results (after run)
main.py                  # CLI entry point
requirements.txt         # Dependencies
```

---

## Features

| Feature | Description |
|---|---|
| **JSON-driven test cases** | Define prompts, expected/forbidden keywords, and latency limits in a simple JSON format |
| **Expected keyword checks** | Verify the LLM response contains at least one required keyword |
| **Forbidden keyword checks** | Ensure dangerous or incorrect content is absent from responses |
| **Latency enforcement** | Flag responses that exceed a configurable time limit |
| **Scoring system** | Each test receives a 0–1 score based on the fraction of checks passed |
| **Mock mode** | Run the full pipeline offline without an API key |
| **OpenAI integration** | Automatically uses the OpenAI API when `OPENAI_API_KEY` is set |
| **Structured JSON output** | Results saved to `results/results.json` for programmatic consumption |
| **Console reports** | Human-readable pass/fail summary with failure breakdown |

---

## Example Dataset

Each test case follows this format:

```json
{
  "id": "fact_001",
  "prompt": "What is the chemical formula for water?",
  "expected_keywords": ["H2O"],
  "forbidden_keywords": ["H3O", "HO2"],
  "max_latency": 2
}
```

The included `data/sample_tests.json` provides **10 test cases** across three categories:

| Category | Tests | Purpose |
|---|---|---|
| **Factual QA** | `fact_001` – `fact_003` | Verify correct factual answers |
| **Hallucination Detection** | `halluc_001` – `halluc_004` | Catch fabricated or false information |
| **Safety Guardrails** | `safety_001` – `safety_003` | Ensure refusal of harmful requests |

---

## How to Run

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run the test suite

```bash
python main.py data/sample_tests.json
```

### Options

```bash
python main.py data/sample_tests.json --model gpt-4          # Use a different model
python main.py data/sample_tests.json --results-dir output    # Custom output directory
```

### Run unit tests

```bash
python -m pytest tests/ -v
```

> **Note:** Without an `OPENAI_API_KEY` environment variable, OmniTest runs in **mock mode** with deterministic simulated responses. Set the variable to test against a real LLM:
> ```bash
> set OPENAI_API_KEY=sk-...
> python main.py data/sample_tests.json
> ```

---

## Example Output

### Console

```
📋  Loaded 10 test case(s) from data/sample_tests.json

  ▶ Running fact_001 … ✅ PASS
  ▶ Running fact_002 … ✅ PASS
  ▶ Running fact_003 … ✅ PASS
  ▶ Running halluc_001 … ✅ PASS
  ▶ Running halluc_002 … ✅ PASS
  ▶ Running halluc_003 … ✅ PASS
  ▶ Running halluc_004 … ✅ PASS
  ▶ Running safety_001 … ✅ PASS
  ▶ Running safety_002 … ✅ PASS
  ▶ Running safety_003 … ✅ PASS

💾  Results saved to results/results.json

OmniTest Report
────────────────────────────────────────
Total tests     : 10
Passed          : 10
Failed          : 0
Pass rate       : 100.0%
Average latency : 0.00s

Results
────────────────────────────────────────
  ✅ fact_001  (score: 100%)
  ✅ fact_002  (score: 100%)
  ✅ fact_003  (score: 100%)
  ✅ halluc_001  (score: 100%)
  ✅ halluc_002  (score: 100%)
  ✅ halluc_003  (score: 100%)
  ✅ halluc_004  (score: 100%)
  ✅ safety_001  (score: 100%)
  ✅ safety_002  (score: 100%)
  ✅ safety_003  (score: 100%)
────────────────────────────────────────
```

### results/results.json

```json
[
  {
    "id": "fact_001",
    "prompt": "What is the chemical formula for water?",
    "response": "The chemical formula for water is H2O.",
    "pass": true,
    "score": 1.0,
    "latency": 0.0001,
    "issues": []
  }
]
```

---

## Future Improvements

- **Semantic similarity scoring** — use embeddings to compare responses against reference answers
- **LLM-as-judge evaluation** — use a second LLM to grade open-ended responses
- **HTML/PDF reports** — export polished visual reports beyond console output
- **Parallel test execution** — run prompts concurrently for faster test suites
- **CI/CD integration** — GitHub Actions workflow with pass/fail exit codes
- **Additional LLM providers** — support for Anthropic, Google Gemini, and local models
- **Test case versioning** — track dataset changes and compare results over time
- **Regression detection** — automatically flag quality degradation across model updates

---

