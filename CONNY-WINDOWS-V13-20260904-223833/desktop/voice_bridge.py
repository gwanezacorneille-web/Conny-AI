"""
CONNY AI V13 — Voice Bridge

Speech/text
    ↓
ConnyVoiceBridge
    ↓
V13 ConnyRequest
    ↓
Real ConnyBridge
    ↓
Real Brain
    ↓
ConnyResponse
    ↓
Voice/UI
"""

from __future__ import annotations

import inspect
from typing import Any

from bridge import get_bridge
from shared.models import ConnyRequest


class ConnyVoiceBridge:
    """Connects voice input to the real V13 bridge."""

    def __init__(self, bridge=None):
        self.bridge = bridge if bridge is not None else get_bridge()

    @staticmethod
    def _build_request(text: str) -> ConnyRequest:
        """
        Construct ConnyRequest using the ACTUAL model contract.

        This intentionally adapts to the existing V13 model instead
        of modifying the core/shared model.
        """
        signature = inspect.signature(ConnyRequest)
        parameters = signature.parameters

        # Prefer the actual field names exposed by the model.
        candidates = (
            "message",
            "query",
            "prompt",
            "input",
            "user_input",
            "content",
            "text",
        )

        for name in candidates:
            parameter = parameters.get(name)

            if parameter is not None:
                return ConnyRequest(**{name: text})

        # Last compatibility fallback for a single positional field.
        positional = [
            p
            for p in parameters.values()
            if p.name != "self"
            and p.kind in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
            and p.default is inspect.Parameter.empty
        ]

        if len(positional) == 1:
            return ConnyRequest(text)

        raise TypeError(
            "Unable to construct ConnyRequest. "
            f"Available parameters: {list(parameters)}"
        )

    def process_text(self, text: str) -> Any:
        """Send recognized text to the real CONNY bridge."""
        text = (text or "").strip()

        if not text:
            return None

        request = self._build_request(text)
        return self.bridge.handle(request)

    def process(self, text: str) -> Any:
        """Compatibility alias."""
        return self.process_text(text)


__all__ = ["ConnyVoiceBridge"]
