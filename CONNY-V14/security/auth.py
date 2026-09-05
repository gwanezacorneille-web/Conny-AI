from security.exceptions import AuthenticationError


class AuthenticationGuard:

    def __init__(self, account_service):
        self.account_service = account_service

    def authenticate(self, token):

        if not token:
            raise AuthenticationError(
                "Authentication required"
            )

        session = self.account_service.validate_session(
            token
        )

        if session is None:
            raise AuthenticationError(
                "Invalid or expired session"
            )

        return session
