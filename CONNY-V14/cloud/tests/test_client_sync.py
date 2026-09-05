from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from cloud.api import ClientSyncStore


class ClientSyncTests(unittest.TestCase):

    def test_push_and_pull_are_account_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ClientSyncStore(
                Path(directory) / "cloud.db"
            )

            store.push(
                "user-a",
                "memory-1",
                "hello",
            )

            store.push(
                "user-b",
                "memory-2",
                "private",
            )

            result = store.pull(
                "user-a"
            )

            self.assertEqual(
                len(result),
                1,
            )

            self.assertEqual(
                result[0]["content"],
                "hello",
            )

            self.assertEqual(
                result[0]["user_id"],
                "user-a",
            )


if __name__ == "__main__":
    unittest.main()
