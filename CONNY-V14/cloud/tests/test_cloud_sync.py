import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from cloud.exceptions import (
    SyncAuthorizationError,
    SyncIsolationError,
)
from cloud.local_provider import LocalCloudProvider
from cloud.service import CloudSyncService
from cloud.models import SyncRecord


class FakeSecurity:
    def authorize(self, account, permission):
        return (
            account.is_active
            and permission == "memory.sync"
        )


class TestCloudSync(unittest.TestCase):

    def setUp(self):
        self.audit_events = []

        def audit(event, user_id=None):
            self.audit_events.append(
                (event, user_id)
            )

        self.provider = LocalCloudProvider()

        self.service = CloudSyncService(
            memory_store=None,
            security_service=FakeSecurity(),
            provider=self.provider,
            audit_logger=audit,
        )

        self.account_a = SimpleNamespace(
            user_id="user-a",
            is_active=True,
        )

        self.account_b = SimpleNamespace(
            user_id="user-b",
            is_active=True,
        )

    def test_push_and_pull_isolated(self):
        record = self.service.make_record(
            self.account_a,
            "memory-1",
            "hello",
            updated_at=100.0,
        )

        self.assertEqual(
            self.service.push(
                self.account_a,
                [record],
            ),
            1,
        )

        pulled_a = self.service.pull(
            self.account_a
        )

        pulled_b = self.service.pull(
            self.account_b
        )

        self.assertEqual(len(pulled_a), 1)
        self.assertEqual(len(pulled_b), 0)
        self.assertEqual(
            pulled_a[0].user_id,
            "user-a",
        )

    def test_cross_account_push_rejected(self):
        record = SyncRecord(
            sync_id="foreign",
            user_id="user-b",
            memory_id="memory-foreign",
            content="private",
            updated_at=100.0,
            version=1,
        )

        with self.assertRaises(SyncIsolationError):
            self.service.push(
                self.account_a,
                [record],
            )

    def test_inactive_account_rejected(self):
        inactive = SimpleNamespace(
            user_id="inactive",
            is_active=False,
        )

        with self.assertRaises(
            SyncAuthorizationError
        ):
            self.service.pull(inactive)

    def test_cursor_pull(self):
        first = self.service.make_record(
            self.account_a,
            "memory-1",
            "first",
            updated_at=100.0,
        )

        second = self.service.make_record(
            self.account_a,
            "memory-2",
            "second",
            updated_at=200.0,
        )

        self.service.push(
            self.account_a,
            [first, second],
        )

        result = self.service.pull(
            self.account_a,
            cursor=100.0,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(
            result[0].memory_id,
            "memory-2",
        )


if __name__ == "__main__":
    unittest.main()
