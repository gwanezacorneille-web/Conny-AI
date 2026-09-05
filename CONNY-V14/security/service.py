from security.audit import audit
from security.exceptions import AuthenticationError
from security.roles import has_permission


class SecurityService:

    def __init__(
        self,
        account_service,
        audit_logger,
    ):

        self.account_service = account_service
        self.audit_logger = audit_logger

    def authenticate(self, token):

        session = self.account_service.validate_session(
            token
        )

        if session is None:

            audit(
                self.audit_logger,
                "AUTHENTICATION_FAILED",
            )

            raise AuthenticationError(
                "Invalid or expired session"
            )

        audit(
            self.audit_logger,
            "AUTHENTICATION_SUCCESS",
            session.user_id,
        )

        return session

    def authorize(
        self,
        account,
        permission,
    ):

        allowed = has_permission(
            account,
            permission,
        )

        if allowed:

            audit(
                self.audit_logger,
                f"AUTHORIZATION_ALLOWED {permission}",
                account.user_id,
            )

        else:

            user_id = (
                account.user_id
                if account
                else None
            )

            audit(
                self.audit_logger,
                f"AUTHORIZATION_DENIED {permission}",
                user_id,
            )

        return allowed

    def logout(self, token):

        result = self.account_service.logout(
            token
        )

        if result:
            audit(
                self.audit_logger,
                "LOGOUT",
            )

        return result
