from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from cloud.models import SyncRecord


class CloudSyncProvider(ABC):
    """
    Provider abstraction for V14 cloud synchronization.

    V14.4 intentionally contains no vendor-specific cloud credentials.
    """

    @abstractmethod
    def push(
        self,
        user_id: str,
        records: Iterable[SyncRecord],
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def pull(
        self,
        user_id: str,
        cursor: Optional[float] = None,
    ) -> List[SyncRecord]:
        raise NotImplementedError
