import hashlib
import hmac
import os


ITERATIONS = 310_000


def hash_password(password: str) -> str:
    if not isinstance(password, str) or len(password) < 8:
        raise ValueError("Password must contain at least 8 characters")

    salt = os.urandom(16)

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        ITERATIONS,
    )

    return (
        f"pbkdf2_sha256${ITERATIONS}$"
        f"{salt.hex()}${digest.hex()}"
    )


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_hex, digest_hex = encoded.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            bytes.fromhex(salt_hex),
            int(iterations),
        )

        return hmac.compare_digest(
            candidate.hex(),
            digest_hex,
        )

    except Exception:
        return False
