from dataclasses import dataclass
from enum import Enum


class ClientPlatform(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    ANDROID = "android"
    WEB = "web"


@dataclass(frozen=True)
class ClientContext:
    platform: ClientPlatform
    client_version: str
    device_id: str
    session_token: str | None = None


@dataclass(frozen=True)
class IntegrationResult:
    success: bool
    operation: str
    message: str
