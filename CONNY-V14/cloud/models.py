from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SyncRecord:
    sync_id: str
    user_id: str
    memory_id: str
    content: str
    updated_at: float
    version: int
    deleted: bool = False


@dataclass(frozen=True)
class SyncResult:
    pushed: int
    pulled: int
    conflicts: int
    rejected: int
    cursor: Optional[float]
