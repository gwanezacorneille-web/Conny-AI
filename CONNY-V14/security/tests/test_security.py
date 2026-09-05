import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from account.database.store import AccountStore
from account.service import AccountService
from security.audit import create_audit_logger
from security.exceptions import AuthenticationError
from security.roles import has_permission
from security.service import SecurityService


class SecurityTests(unittest.TestCase):

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)

        self.accounts = AccountService(
            AccountStore(root / "accounts.db")
        )

        self.logger = create_audit_logger(
            root / "security.log"
        )

        self.security = SecurityService(
            self.accounts,
            self.logger,
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_valid_session(self):

        self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        _, session = self.accounts.login_private(
            "alice",
            "alice-password-123",
        )

        result = self.security.authenticate(
            session.token
        )

        self.assertEqual(
            result.user_id,
            session.user_id,
        )

    def test_invalid_session(self):

        with self.assertRaises(AuthenticationError):

            self.security.authenticate(
                "invalid-token"
            )

    def test_revoked_session(self):

        self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        _, session = self.accounts.login_private(
            "alice",
            "alice-password-123",
        )

        self.accounts.logout(
            session.token
        )

        with self.assertRaises(AuthenticationError):

            self.security.authenticate(
                session.token
            )

    def test_guest_cannot_use_vip_permission(self):

        guest = self.accounts.guest()

        self.assertFalse(
            has_permission(
                guest,
                "vip",
            )
        )

    def test_private_cannot_use_vip_permission(self):

        private = self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        self.assertFalse(
            has_permission(
                private,
                "vip",
            )
        )

    def test_vip_has_vip_permission(self):

        with patch(
            "config.vip.VIP_SECRET",
            "test-vip-secret",
        ):

            result = self.accounts.login_vip(
                "creator",
                "test-vip-secret",
            )

        self.assertIsNotNone(result)

        account, session = result

        self.assertTrue(
            account.is_vip
        )

        self.assertTrue(
            has_permission(
                account,
                "vip",
            )
        )

        self.assertIsNotNone(session)

    def test_authorization(self):

        private = self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        self.assertTrue(
            self.security.authorize(
                private,
                "memory.read",
            )
        )

        self.assertFalse(
            self.security.authorize(
                private,
                "vip",
            )
        )


if __name__ == "__main__":
    unittest.main()
