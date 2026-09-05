import unittest

from release.manifest import version, validate_structure


class ReleaseCandidateTests(unittest.TestCase):

    def test_version(self):
        self.assertEqual(version(), "14.14.0")

    def test_structure(self):
        self.assertEqual(validate_structure(), [])


if __name__ == "__main__":
    unittest.main()
