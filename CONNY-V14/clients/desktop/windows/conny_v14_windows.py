from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request


API_BASE = os.getenv(
    "CONNY_V14_API",
    "http://127.0.0.1:8000",
)


def request(path, method="GET", payload=None, token=None):
    url = API_BASE.rstrip("/") + path

    data = None

    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request_object = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(
        request_object,
        timeout=15,
    ) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


def guest():
    return request(
        "/auth/guest",
        method="POST",
    )


def login(username, password):
    return request(
        "/auth/login",
        method="POST",
        payload={
            "username": username,
            "password": password,
            "account_type": "private",
        },
    )


def logout(token):
    return request(
        "/auth/logout",
        method="POST",
        token=token,
    )


def validate(token):
    return request(
        "/auth/session",
        method="GET",
        token=token,
    )


def main():
    print("CONNY AI V14 Authentication")
    print("===========================")
    print("1. Guest")
    print("2. Sign in")
    print("3. Exit")

    choice = input("> ").strip()

    try:
        if choice == "1":
            result = guest()

        elif choice == "2":
            username = input("Username: ").strip()
            password = input("Password: ")

            result = login(
                username,
                password,
            )

        else:
            return 0

        print()
        print("Authentication successful.")
        print("User:", result.get("username"))
        print("Account:", result.get("account_type"))
        print("Token received.")

        return 0

    except urllib.error.URLError as exc:
        print("V14 API unavailable:", exc)
        return 1

    except Exception as exc:
        print("Authentication failed:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
