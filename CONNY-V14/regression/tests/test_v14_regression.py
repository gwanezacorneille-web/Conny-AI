import unittest
from pathlib import Path


class V14RegressionTests(unittest.TestCase):

    def setUp(self):
        self.root = Path(__file__).resolve().parents[2]

    def test_version_exists(self):
        version = (
            self.root / "VERSION"
        ).read_text().strip()

        self.assertTrue(
            version.startswith("14.")
        )

    def test_required_packages_exist(self):
        required = [
            "account",
            "memory",
            "security",
            "cloud",
            "settings",
        ]

        for package in required:
            self.assertTrue(
                (self.root / package).is_dir(),
                package,
            )

    def test_v13_is_not_inside_v14(self):
        self.assertFalse(
            (self.root / "v13").exists()
        )

    def test_security_document_exists(self):
        self.assertTrue(
            (
                self.root
                / "security"
                / "SECURITY.md"
            ).is_file()
        )


if __name__ == "__main__":
    unittest.main()
