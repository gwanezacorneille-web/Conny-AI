from dataclasses import dataclass
from enum import Enum


class PlatformType(str, Enum):
    WINDOWS = "windows"
    LINUX = "linux"
    ANDROID = "android"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class PlatformContext:
    platform: PlatformType
    app_version: str
    device_id: str

    @property
    def is_supported(self):
        return self.platform in {
            PlatformType.WINDOWS,
            PlatformType.LINUX,
            PlatformType.ANDROID,
        }
