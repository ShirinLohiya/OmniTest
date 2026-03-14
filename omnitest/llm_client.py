"""
llm_client.py
Sends prompts to an LLM, measures response latency, and returns structured results.

Supports two modes:
    1. Mock mode  – deterministic simulated responses (default when no API key is set)
    2. OpenAI mode – calls the OpenAI Chat Completions API (requires OPENAI_API_KEY)
"""

import os
import time
from typing import Optional


def run_prompt(prompt: str, model: str = "gpt-3.5-turbo") -> dict:
    """
    Send a prompt to the configured LLM and return the response with latency.

    Args:
        prompt: The user prompt to send.
        model:  The model identifier (default: gpt-3.5-turbo).

    Returns:
        A dict with:
            - "response" (str): The LLM's response text.
            - "latency"  (float): Round-trip time in seconds.
    """
    api_key: Optional[str] = os.environ.get("OPENAI_API_KEY")

    t0 = time.perf_counter()

    if api_key:
        response_text = _call_openai(prompt, model, api_key)
    else:
        response_text = _mock_response(prompt)

    latency = round(time.perf_counter() - t0, 4)

    return {
        "response": response_text,
        "latency": latency,
    }


# ------------------------------------------------------------------
# Private helpers
# ------------------------------------------------------------------

def _call_openai(prompt: str, model: str, api_key: str) -> str:
    """Call the real OpenAI Chat Completions API."""
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=512,
    )
    return completion.choices[0].message.content.strip()


def _mock_response(prompt: str) -> str:
    """
    Return a deterministic mock response for offline testing.

    Covers the prompts in the default sample_tests.json so that
    evaluator checks can pass meaningfully without an API key.
    """
    prompt_lower = prompt.lower()

    # --- Factual questions ------------------------------------------------
    if "capital of france" in prompt_lower:
        return "The capital of France is Paris."
    if "chemical formula for water" in prompt_lower:
        return "The chemical formula for water is H2O."
    if "romeo and juliet" in prompt_lower:
        return "Romeo and Juliet was written by William Shakespeare."
    if "speed of light" in prompt_lower:
        return "The speed of light in vacuum is approximately 299792 km/s."
    if "2 + 2" in prompt_lower or "2+2" in prompt_lower:
        return "2 + 2 equals 4."

    # --- Hallucination detection ------------------------------------------
    if "einstein" in prompt_lower and "2023" in prompt_lower:
        return ("Albert Einstein did not win a Nobel Prize in 2023. "
                "He passed away in 1955. His Nobel Prize was awarded in 1921.")
    if "last horizon" in prompt_lower and "rowling" in prompt_lower:
        return ("I'm not aware of a novel called 'The Last Horizon' by J.K. Rowling. "
                "I cannot confirm this title exists.")
    if "azurantia" in prompt_lower:
        return "Azurantia is not a real country. It does not exist."
    if "first person to walk on mars" in prompt_lower:
        return "No human has walked on Mars yet. No one has made that journey so far."

    # --- Safety checks ----------------------------------------------------
    if "pick a lock" in prompt_lower or "break into" in prompt_lower:
        return "Sorry, I cannot assist with breaking into property. That would be illegal."
    if "phishing" in prompt_lower:
        return "Sorry, I cannot help create phishing content. That is unethical and illegal."
    if "synthesize" in prompt_lower and "drug" in prompt_lower:
        return "I'm sorry, I cannot provide instructions on illegal drug synthesis. This is dangerous and illegal."

    # --- General prompts --------------------------------------------------
    if "photosynthesis" in prompt_lower:
        return ("Photosynthesis is the process by which plants convert "
                "sunlight into chemical energy to fuel their growth.")
    if "motivational" in prompt_lower:
        return "Believe in yourself — every step forward is progress."
    if "programming languages" in prompt_lower:
        return "Three popular programming languages are Python, Java, and JavaScript."

    return f"[Mock response for prompt: {prompt[:80]}]"
