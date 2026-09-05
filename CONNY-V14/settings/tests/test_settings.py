import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from settings.exceptions import (
    SettingsAuthorizationError,
    SettingsValidationError,
)
from settings.service import SettingsService
from settings.store import SettingsStore


class FakeSecurity:

    def authorize(
        self,
        account,
        permission,
    ):
        return bool(
            account
            and account.is_active
            and permission.startswith("settings.")
        )


class SettingsTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

        self.store = SettingsStore(
            str(Path(self.tmp.name) / "settings.db")
        )

        self.audit_events = []

        self.service = SettingsService(
            self.store,
            FakeSecurity(),
            lambda event, user_id: self.audit_events.append(
                (event, user_id)
            ),
        )

        self.account_a = SimpleNamespace(
            user_id="user-a",
            is_active=True,
        )

        self.account_b = SimpleNamespace(
            user_id="user-b",
            is_active=True,
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_defaults(self):
        result = self.service.get(
            self.account_a,
            "theme",
        )

        self.assertEqual(
            result.value,
            "dark",
        )

    def test_set_and_get(self):
        self.service.set(
            self.account_a,
            "theme",
            "light",
        )

        result = self.service.get(
            self.account_a,
            "theme",
        )

        self.assertEqual(
            result.value,
            "light",
        )

    def test_boolean_setting(self):
        self.service.set(
            self.account_a,
            "voice_enabled",
            False,
        )

        result = self.service.get(
            self.account_a,
            "voice_enabled",
        )

        self.assertIs(
            result.value,
            False,
        )

    def test_account_isolation(self):
        self.service.set(
            self.account_a,
            "language",
            "rw",
        )

        result = self.service.get(
            self.account_b,
            "language",
        )

        self.assertEqual(
            result.value,
            "en",
        )

    def test_reset(self):
        self.service.set(
            self.account_a,
            "theme",
            "light",
        )

        result = self.service.reset(
            self.account_a,
            "theme",
        )

        self.assertEqual(
            result.value,
            "dark",
        )

    def test_invalid_key(self):
        with self.assertRaises(
            SettingsValidationError
        ):
            self.service.get(
                self.account_a,
                "not-a-real-setting",
            )

    def test_invalid_type(self):
        with self.assertRaises(
            SettingsValidationError
        ):
            self.service.set(
                self.account_a,
                "voice_enabled",
                "false",
            )

    def test_inactive_account_rejected(self):
        inactive = SimpleNamespace(
            user_id="inactive",
            is_active=False,
        )

        with self.assertRaises(
            SettingsAuthorizationError
        ):
            self.service.get(
                inactive,
                "theme",
            )


if __name__ == "__main__":
    unittest.main()
