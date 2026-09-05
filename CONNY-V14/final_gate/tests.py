import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FinalV14GateTests(unittest.TestCase):

    def test_version(self):
        version = (ROOT / "VERSION").read_text().strip()
        self.assertEqual(version, "14.14.0")

    def test_required_components(self):
        required = [
            "account",
            "memory",
            "security",
            "cloud",
            "settings",
            "v14_platform",
            "integration",
            "app",
            "release",
        ]

        for name in required:
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).exists())

    def test_no_old_platform_package(self):
        self.assertFalse((ROOT / "platform").exists())

    def test_security_document(self):
        self.assertTrue(
            (ROOT / "security" / "SECURITY.md").exists()
        )


if __name__ == "__main__":
    unittest.main()
