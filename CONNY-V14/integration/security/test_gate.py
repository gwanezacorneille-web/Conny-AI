import unittest

from integration.security.gate import IntegrationSecurityGate


class IntegrationSecurityGateTests(unittest.TestCase):

    def setUp(self):
        self.gate = IntegrationSecurityGate()

    def test_missing_account_rejected(self):
        self.assertFalse(
            self.gate.validate_session(None, "token")
        )

    def test_missing_token_rejected(self):
        class Account:
            is_active = True

        self.assertFalse(
            self.gate.validate_session(Account(), "")
        )

    def test_inactive_account_rejected(self):
        class Account:
            is_active = False

        self.assertFalse(
            self.gate.validate_session(Account(), "token")
        )

    def test_account_isolation(self):
        self.assertTrue(
            self.gate.validate_account_boundary("A", "A")
        )

        self.assertFalse(
            self.gate.validate_account_boundary("A", "B")
        )


if __name__ == "__main__":
    unittest.main()
