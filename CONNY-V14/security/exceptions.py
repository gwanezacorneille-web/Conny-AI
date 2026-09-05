class AuthenticationError(Exception):
    pass


class AuthorizationError(Exception):
    pass


class InvalidSessionError(AuthenticationError):
    pass
