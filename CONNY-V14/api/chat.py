from __future__ import annotations

import sys
from pathlib import Path

V14_ROOT = Path(__file__).resolve().parents[1]
ROOT = V14_ROOT.parent

V13_CANDIDATES = [
    ROOT / "Conny-AI-V5" / "v13",
    ROOT / "CONNY-WINDOWS-V13-20260904-223833",
]


def load_v13_bridge():
    for path in V13_CANDIDATES:
        if not path.is_dir():
            continue

        value = str(path)

        if value not in sys.path:
            sys.path.insert(0, value)

        try:
            from bridge import get_bridge
            return get_bridge()
        except Exception:
            continue

    return None


_bridge = None


def authenticated_chat(session, message: str):
    global _bridge

    if not message.strip():
        return {
            "response": "Please enter a message.",
            "success": False,
            "source": "v14",
        }

    if _bridge is None:
        _bridge = load_v13_bridge()

    if _bridge is None:
        return {
            "response": "CONNY V14 authentication is active, but the V13 intelligence bridge is not available to this API process.",
            "success": False,
            "source": "v14-auth",
        }

    try:
        from shared.models import ConnyRequest

        response = _bridge.handle(
            ConnyRequest(
                message=message,
                source="v14",
            )
        )

        return {
            "response": response.text,
            "success": response.success,
            "source": response.source,
        }

    except Exception as exc:
        return {
            "response": f"CONNY could not process the request: {exc}",
            "success": False,
            "source": "v14",
        }
