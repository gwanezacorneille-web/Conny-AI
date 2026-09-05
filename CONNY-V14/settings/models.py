from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SettingDefinition:
    key: str
    default: Any
    value_type: type


@dataclass(frozen=True)
class SettingValue:
    user_id: str
    key: str
    value: Any
