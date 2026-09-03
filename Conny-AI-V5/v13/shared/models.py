"""CONNY AI V13 shared data models."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ConnyRequest:
    message: str
    source: str = "unknown"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message": self.message,
            "source": self.source,
        }


@dataclass
class ConnyResponse:
    text: str
    success: bool = True
    source: str = "conny"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "success": self.success,
            "source": self.source,
        }
