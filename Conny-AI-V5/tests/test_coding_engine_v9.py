import unittest

from brain.coding_engine import CodingEngine


class TestCodingEngineV9(unittest.TestCase):

    def setUp(self):
        self.c = CodingEngine()

    def test_print_parenthesis_fix(self):
        result = self.c.fix(
            "fix this Python code: print(x"
        )

        self.assertTrue(result["fixed"])
        self.assertEqual(
            result["code"],
            "x = 5\nprint(x)"
        )

    def test_if_colon_fix(self):
        result = self.c.fix(
            "fix this Python code: if x == 5"
        )

        self.assertTrue(result["fixed"])
        self.assertIn(
            "if x == 5:",
            result["code"]
        )

    def test_for_colon_fix(self):
        result = self.c.fix(
            "fix this Python code: for i in range(5)"
        )

        self.assertTrue(result["fixed"])
        self.assertIn(
            "for i in range(5):",
            result["code"]
        )

    def test_while_colon_fix(self):
        result = self.c.fix(
            "fix this Python code: while x < 5"
        )

        self.assertTrue(result["fixed"])
        self.assertIn(
            "while x < 5:",
            result["code"]
        )

    def test_function_colon_fix(self):
        result = self.c.fix(
            "fix this Python code: def hello()"
        )

        self.assertTrue(result["fixed"])
        self.assertIn(
            "def hello():",
            result["code"]
        )
        self.assertIn(
            "pass",
            result["code"]
        )

    def test_quote_detection(self):
        result = self.c.analyze(
            'debug this Python code: print("hello)'
        )

        self.assertTrue(result["has_issues"])
        self.assertIn(
            "Unbalanced quotation marks.",
            result["issues"]
        )

    def test_parenthesis_detection(self):
        result = self.c.analyze(
            "debug this Python code: print(x"
        )

        self.assertTrue(result["has_issues"])
        self.assertIn(
            "Unbalanced parentheses.",
            result["issues"]
        )

    def test_bracket_detection(self):
        result = self.c.analyze(
            "debug this Python code: values = [1, 2, 3"
        )

        self.assertTrue(result["has_issues"])
        self.assertIn(
            "Unbalanced square brackets.",
            result["issues"]
        )

    def test_curly_brace_detection(self):
        result = self.c.analyze(
            "debug this Python code: data = {'x': 1"
        )

        self.assertTrue(result["has_issues"])
        self.assertIn(
            "Unbalanced curly braces.",
            result["issues"]
        )


if __name__ == "__main__":
    unittest.main()
