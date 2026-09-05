import time
import uuid
from typing import Optional

from cloud.exceptions import (
    SyncAuthenticationError,
    SyncAuthorizationError,
    SyncIsolationError,
)
from cloud.models import SyncRecord, SyncResult


class CloudSyncService:
    """
    Secure synchronization boundary between V14 local memory and a
    cloud provider.

    The service never accepts an arbitrary user_id from the caller.
    The authenticated account determines the synchronization namespace.
    """

    SYNC_PERMISSION = "memory.sync"

    def __init__(
        self,
        memory_store,
        security_service,
        provider,
        audit_logger,
    ):
        self.memory_store = memory_store
        self.security_service = security_service
        self.provider = provider
        self.audit_logger = audit_logger

    def _authorize(self, account):
        if account is None:
            raise SyncAuthenticationError(
                "Account required for cloud synchronization"
            )

        if not account.is_active:
            raise SyncAuthorizationError(
                "Active account required for cloud synchronization"
            )

        allowed = self.security_service.authorize(
            account,
            self.SYNC_PERMISSION,
        )

        if not allowed:
            raise SyncAuthorizationError(
                "Account is not authorized for cloud synchronization"
            )

    def make_record(
        self,
        account,
        memory_id,
        content,
        version=1,
        deleted=False,
        updated_at=None,
    ):
        self._authorize(account)

        if updated_at is None:
            updated_at = time.time()

        return SyncRecord(
            sync_id=str(uuid.uuid4()),
            user_id=account.user_id,
            memory_id=str(memory_id),
            content=content,
            updated_at=float(updated_at),
            version=int(version),
            deleted=bool(deleted),
        )

    def push(self, account, records):
        self._authorize(account)

        records = list(records)

        for record in records:
            if record.user_id != account.user_id:
                self.audit_logger(
                    "SYNC_ISOLATION_REJECTED",
                    account.user_id,
                )
                raise SyncIsolationError(
                    "Cannot synchronize another account's data"
                )

        count = self.provider.push(
            account.user_id,
            records,
        )

        self.audit_logger(
            "SYNC_PUSH",
            account.user_id,
        )

        return count

    def pull(self, account, cursor: Optional[float] = None):
        self._authorize(account)

        records = self.provider.pull(
            account.user_id,
            cursor,
        )

        self.audit_logger(
            "SYNC_PULL",
            account.user_id,
        )

        return records

    def synchronize(
        self,
        account,
        records,
        cursor: Optional[float] = None,
    ):
        self._authorize(account)

        records = list(records)

        pushed = self.push(
            account,
            records,
        )

        pulled_records = self.pull(
            account,
            cursor,
        )

        new_cursor = cursor

        if pulled_records:
            new_cursor = max(
                record.updated_at
                for record in pulled_records
            )

        return SyncResult(
            pushed=pushed,
            pulled=len(pulled_records),
            conflicts=0,
            rejected=0,
            cursor=new_cursor,
        )
