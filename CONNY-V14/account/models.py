from dataclasses import dataclass
from enum import Enum


class AccountType(str, Enum):
    GUEST = "guest"
    PRIVATE = "private"
    VIP = "vip"


@dataclass(frozen=True)
class Account:
    user_id: str
    account_type: AccountType
    username: str
    is_active: bool = True

    @property
    def is_guest(self):
        return self.account_type == AccountType.GUEST

    @property
    def is_private(self):
        return self.account_type == AccountType.PRIVATE

    @property
    def is_vip(self):
        return self.account_type == AccountType.VIP
