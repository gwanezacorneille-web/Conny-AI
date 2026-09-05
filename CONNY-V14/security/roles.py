from account.models import AccountType


ROLE_PERMISSIONS = {
    AccountType.GUEST: {
        "chat",
        "memory.read",
        "memory.write",
        "memory.delete",
        "memory.sync",
    },

    AccountType.PRIVATE: {
        "chat",
        "memory.read",
        "memory.write",
        "memory.delete",
        "memory.sync",
    },

    AccountType.VIP: {
        "chat",
        "memory.read",
        "memory.write",
        "memory.delete",
        "memory.sync",
        "vip",
    },
}


def has_permission(account, permission):

    if not account or not account.is_active:
        return False

    return permission in ROLE_PERMISSIONS.get(
        account.account_type,
        set(),
    )
