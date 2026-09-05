import uuid

from account.models import Account, AccountType


def create_guest():
    return Account(
        user_id=f"guest-{uuid.uuid4()}",
        account_type=AccountType.GUEST,
        username="Guest",
    )
