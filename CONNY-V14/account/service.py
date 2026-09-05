from account.guest import create_guest
from account.models import Account, AccountType
from account.security.sessions import SessionManager
from config.vip import verify_vip_login


class AccountService:

    def __init__(self, store):
        self.store = store
        self.sessions = SessionManager()

    def guest(self):
        return create_guest()

    def register_private(
        self,
        username,
        password,
    ):

        user_id = self.store.create_private(
            username,
            password,
        )

        return Account(
            user_id=user_id,
            account_type=AccountType.PRIVATE,
            username=username.strip(),
        )

    def login_private(
        self,
        username,
        password,
    ):

        row = self.store.authenticate_private(
            username,
            password,
        )

        if row is None:
            return None

        account = Account(
            user_id=row["user_id"],
            account_type=AccountType.PRIVATE,
            username=row["username"],
        )

        session = self.sessions.create(
            account.user_id
        )

        return account, session

    def login_vip(
        self,
        username,
        secret,
    ):

        if not verify_vip_login(
            username,
            secret,
        ):
            return None

        account = Account(
            user_id="vip-creator",
            account_type=AccountType.VIP,
            username=username.strip(),
        )

        session = self.sessions.create(
            account.user_id
        )

        return account, session

    def validate_session(self, token):
        return self.sessions.validate(token)

    def logout(self, token):
        return self.sessions.revoke(token)
