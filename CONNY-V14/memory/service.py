class MemoryService:

    def __init__(self, store):
        self.store = store

    def remember(self, account, content):

        if not account.is_active:
            raise PermissionError(
                "Inactive account cannot store memory"
            )

        return self.store.add(
            account.user_id,
            account.account_type.value,
            content,
        )

    def recall(self, account):

        if not account.is_active:
            raise PermissionError(
                "Inactive account cannot access memory"
            )

        return self.store.list_for_user(
            account.user_id
        )

    def forget(self, account, memory_id):

        if not account.is_active:
            raise PermissionError(
                "Inactive account cannot delete memory"
            )

        return self.store.delete_for_user(
            account.user_id,
            memory_id,
        )
