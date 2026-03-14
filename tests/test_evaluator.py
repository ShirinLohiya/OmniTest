"""
test_evaluator.py
Unit tests for the evaluator module.
"""

import unittest
from omnitest.evaluator import evaluate


class TestExpectedKeywords(unittest.TestCase):

    def test_keyword_found(self):
        tc = {"id": "t1", "expected_keywords": ["hello"]}
        result = evaluate(tc, "Hello world!")
        self.assertTrue(result["pass"])
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["issues"], [])

    def test_keyword_missing(self):
        tc = {"id": "t2", "expected_keywords": ["banana"]}
        result = evaluate(tc, "Hello world!")
        self.assertFalse(result["pass"])
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(len(result["issues"]), 1)
        self.assertIn("Missing expected keywords", result["issues"][0])

    def test_keyword_case_insensitive(self):
        tc = {"id": "t3", "expected_keywords": ["PARIS"]}
        result = evaluate(tc, "The capital is paris.")
        self.assertTrue(result["pass"])


class TestForbiddenKeywords(unittest.TestCase):

    def test_no_forbidden_found(self):
        tc = {"id": "t4", "forbidden_keywords": ["error", "bug"]}
        result = evaluate(tc, "Everything works fine.")
        self.assertTrue(result["pass"])
        self.assertEqual(result["score"], 1.0)

    def test_forbidden_detected(self):
        tc = {"id": "t5", "forbidden_keywords": ["step 1", "click here"]}
        result = evaluate(tc, "Step 1: click here to begin.")
        self.assertFalse(result["pass"])
        self.assertIn("Forbidden keywords detected", result["issues"][0])

    def test_forbidden_case_insensitive(self):
        tc = {"id": "t6", "forbidden_keywords": ["SECRET"]}
        result = evaluate(tc, "This is a secret message.")
        self.assertFalse(result["pass"])


class TestLatencyCheck(unittest.TestCase):

    def test_within_limit(self):
        tc = {"id": "t7", "max_latency": 2.0}
        result = evaluate(tc, "Fast response.", latency=0.5)
        self.assertTrue(result["pass"])
        self.assertEqual(result["score"], 1.0)

    def test_exceeds_limit(self):
        tc = {"id": "t8", "max_latency": 1.0}
        result = evaluate(tc, "Slow response.", latency=2.5)
        self.assertFalse(result["pass"])
        self.assertIn("exceeded limit", result["issues"][0])


class TestCombinedChecks(unittest.TestCase):

    def test_all_pass(self):
        tc = {
            "id": "t9",
            "expected_keywords": ["Paris"],
            "forbidden_keywords": ["London"],
            "max_latency": 2.0,
        }
        result = evaluate(tc, "The capital of France is Paris.", latency=0.3)
        self.assertTrue(result["pass"])
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["issues"], [])

    def test_partial_failure(self):
        tc = {
            "id": "t10",
            "expected_keywords": ["Paris"],
            "forbidden_keywords": ["France"],
            "max_latency": 2.0,
        }
        result = evaluate(tc, "The capital of France is Paris.", latency=0.3)
        self.assertFalse(result["pass"])
        # 2 out of 3 checks pass → score ≈ 0.67
        self.assertAlmostEqual(result["score"], 0.67, places=2)
        self.assertEqual(len(result["issues"]), 1)

    def test_all_fail(self):
        tc = {
            "id": "t11",
            "expected_keywords": ["Berlin"],
            "forbidden_keywords": ["Paris"],
            "max_latency": 0.1,
        }
        result = evaluate(tc, "The capital of France is Paris.", latency=1.0)
        self.assertFalse(result["pass"])
        self.assertEqual(result["score"], 0.0)
        self.assertEqual(len(result["issues"]), 3)

    def test_no_checks_defined(self):
        tc = {"id": "t12"}
        result = evaluate(tc, "Any response.")
        self.assertTrue(result["pass"])
        self.assertEqual(result["score"], 1.0)
        self.assertEqual(result["issues"], [])


if __name__ == "__main__":
    unittest.main()
