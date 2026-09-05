from typing import Dict, List, Optional

from cloud.exceptions import SyncConflictError, SyncIsolationError
from cloud.models import SyncRecord
from cloud.provider import CloudSyncProvider


class LocalCloudProvider(CloudSyncProvider):
    """
    Deterministic local provider used by V14.4 tests.

    It models the cloud-provider contract without requiring an external
    service or credentials.
    """

    def __init__(self):
        self._records: Dict[str, SyncRecord] = {}

    def push(
        self,
        user_id: str,
        records,
    ) -> int:
        pushed = 0

        for record in records:
            if record.user_id != user_id:
                raise SyncIsolationError(
                    "Cannot push a record belonging to another account"
                )

            existing = self._records.get(record.sync_id)

            if existing is not None:
                if existing.user_id != user_id:
                    raise SyncIsolationError(
                        "Sync record belongs to another account"
                    )

                if record.version < existing.version:
                    raise SyncConflictError(
                        "Incoming record has an older version"
                    )

                if (
                    record.version == existing.version
                    and record != existing
                ):
                    raise SyncConflictError(
                        "Same-version records conflict"
                    )

                if record.version == existing.version:
                    continue

            self._records[record.sync_id] = record
            pushed += 1

        return pushed

    def pull(
        self,
        user_id: str,
        cursor: Optional[float] = None,
    ) -> List[SyncRecord]:
        records = []

        for record in self._records.values():
            if record.user_id != user_id:
                continue

            if cursor is not None and record.updated_at <= cursor:
                continue

            records.append(record)

        records.sort(
            key=lambda item: (item.updated_at, item.sync_id)
        )

        return records
