"""
dataset_loader.py
Loads test cases from a JSON dataset file.
"""

import json
from pathlib import Path
from typing import List, Dict, Any


def load_dataset(filepath: str) -> List[Dict[str, Any]]:
    """
    Load test cases from a JSON file.

    Args:
        filepath: Path to the JSON dataset file.

    Returns:
        A list of test-case dictionaries.

    Raises:
        FileNotFoundError: If the dataset file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Dataset JSON must be a top-level array of test cases.")

    return data
