"""Stable interface shared by CONNY AI V13 clients."""

from .models import ConnyRequest, ConnyResponse


def validate_request(request: ConnyRequest) -> bool:
    return bool(request.message.strip())


def create_response(text: str, success: bool = True) -> ConnyResponse:
    return ConnyResponse(
        text=text,
        success=success,
    )
