import tempfile
import unittest
from pathlib import Path

from account.database.store import AccountStore
from account.models import AccountType
from account.service import AccountService


class AccountTests(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()

        db = Path(self.temp.name) / "accounts.db"

        self.service = AccountService(
            AccountStore(db)
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_guest(self):
        account = self.service.guest()

        self.assertEqual(
            account.account_type,
            AccountType.GUEST,
        )

    def test_private_register_login(self):

        account = self.service.register_private(
            "testuser",
            "test-password-123",
        )

        self.assertTrue(
            account.is_private
        )

        result = self.service.login_private(
            "testuser",
            "test-password-123",
        )

        self.assertIsNotNone(result)

        account, session = result

        self.assertTrue(
            account.is_private
        )

        self.assertIsNotNone(
            session.token
        )

    def test_wrong_password(self):

        self.service.register_private(
            "testuser",
            "test-password-123",
        )

        result = self.service.login_private(
            "testuser",
            "wrong-password",
        )

        self.assertIsNone(result)

    def test_logout(self):

        self.service.register_private(
            "testuser",
            "test-password-123",
        )

        _, session = self.service.login_private(
            "testuser",
            "test-password-123",
        )

        self.assertIsNotNone(
            self.service.validate_session(
                session.token
            )
        )

        self.assertTrue(
            self.service.logout(
                session.token
            )
        )

        self.assertIsNone(
            self.service.validate_session(
                session.token
            )
        )


if __name__ == "__main__":
    unittest.main()
