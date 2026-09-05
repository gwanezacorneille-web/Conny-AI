from dataclasses import dataclass


@dataclass(frozen=True)
class AppContext:
    app_name: str
    app_version: str
    platform: str
    device_id: str
