import hmac
import os


VIP_USERNAME = os.getenv(
    "CONNY_VIP_USERNAME",
    "creator",
)

VIP_SECRET = os.getenv(
    "CONNY_VIP_SECRET",
)


def verify_vip_login(username, secret):
    if not VIP_SECRET:
        return False

    return (
        hmac.compare_digest(
            username.strip(),
            VIP_USERNAME,
        )
        and
        hmac.compare_digest(
            secret,
            VIP_SECRET,
        )
    )
