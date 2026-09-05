import tempfile
import unittest
from pathlib import Path

from account.database.store import AccountStore
from account.service import AccountService
from memory.store import MemoryStore
from memory.service import MemoryService


class MemoryTests(unittest.TestCase):

    def setUp(self):

        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)

        self.accounts = AccountService(
            AccountStore(root / "accounts.db")
        )

        self.memory = MemoryService(
            MemoryStore(root / "memory.db")
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_guest_memory(self):

        guest = self.accounts.guest()

        self.memory.remember(
            guest,
            "Guest memory",
        )

        memories = self.memory.recall(guest)

        self.assertEqual(len(memories), 1)
        self.assertEqual(
            memories[0]["content"],
            "Guest memory",
        )

    def test_private_memory_isolation(self):

        alice = self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        bob = self.accounts.register_private(
            "bob",
            "bob-password-123",
        )

        self.memory.remember(
            alice,
            "Alice memory",
        )

        self.memory.remember(
            bob,
            "Bob memory",
        )

        alice_memories = self.memory.recall(alice)
        bob_memories = self.memory.recall(bob)

        self.assertEqual(
            [m["content"] for m in alice_memories],
            ["Alice memory"],
        )

        self.assertEqual(
            [m["content"] for m in bob_memories],
            ["Bob memory"],
        )

    def test_cannot_delete_other_account_memory(self):

        alice = self.accounts.register_private(
            "alice",
            "alice-password-123",
        )

        bob = self.accounts.register_private(
            "bob",
            "bob-password-123",
        )

        memory = self.memory.remember(
            alice,
            "Alice private memory",
        )

        result = self.memory.forget(
            bob,
            memory["memory_id"],
        )

        self.assertFalse(result)

        self.assertEqual(
            len(self.memory.recall(alice)),
            1,
        )

    def test_guest_and_private_are_isolated(self):

        guest = self.accounts.guest()

        private = self.accounts.register_private(
            "private",
            "private-password-123",
        )

        self.memory.remember(
            guest,
            "Guest only",
        )

        self.memory.remember(
            private,
            "Private only",
        )

        self.assertEqual(
            self.memory.recall(guest)[0]["content"],
            "Guest only",
        )

        self.assertEqual(
            self.memory.recall(private)[0]["content"],
            "Private only",
        )


if __name__ == "__main__":
    unittest.main()
