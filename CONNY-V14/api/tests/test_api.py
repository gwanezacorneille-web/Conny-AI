from __future__ import annotations

import tempfile
import unittest
from pathlib import Path


class AuthContractTests(unittest.TestCase):

    def test_session_store_imports(self):
        from api.session_store import PersistentSessionStore

        with tempfile.TemporaryDirectory() as directory:
            store = PersistentSessionStore(
                Path(directory) / "sessions.db",
            )

            session = store.create(
                "user-1",
                "tester",
                "private",
            )

            self.assertTrue(session.token)

            validated = store.validate(
                session.token
            )

            self.assertIsNotNone(validated)
            self.assertEqual(
                validated.user_id,
                "user-1",
            )

    def test_session_revoke(self):
        from api.session_store import PersistentSessionStore

        with tempfile.TemporaryDirectory() as directory:
            store = PersistentSessionStore(
                Path(directory) / "sessions.db",
            )

            session = store.create(
                "user-1",
                "tester",
                "private",
            )

            self.assertTrue(
                store.revoke(session.token)
            )

            self.assertIsNone(
                store.validate(session.token)
            )


if __name__ == "__main__":
    unittest.main()
