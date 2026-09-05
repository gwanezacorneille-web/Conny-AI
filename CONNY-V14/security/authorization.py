from security.exceptions import AuthorizationError
from security.roles import has_permission


class AuthorizationGuard:

    def require(self, account, permission):

        if not account:
            raise AuthorizationError(
                "Account required"
            )

        if not has_permission(
            account,
            permission,
        ):
            raise AuthorizationError(
                f"Permission denied: {permission}"
            )

        return True
