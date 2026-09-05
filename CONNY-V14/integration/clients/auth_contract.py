from __future__ import annotations


AUTH_VERSION = "v14"

REGISTER_ENDPOINT = "/auth/register"
LOGIN_ENDPOINT = "/auth/login"
GUEST_ENDPOINT = "/auth/guest"
LOGOUT_ENDPOINT = "/auth/logout"
SESSION_ENDPOINT = "/auth/session"

SUPPORTED_CLIENTS = (
    "web",
    "windows",
    "linux",
    "android",
)


def authorization_header(token: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {token}",
    }
