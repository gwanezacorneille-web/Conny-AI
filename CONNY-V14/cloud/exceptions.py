class CloudSyncError(Exception):
    """Base exception for V14 cloud synchronization."""


class SyncAuthenticationError(CloudSyncError):
    """Raised when synchronization is attempted without valid authentication."""


class SyncAuthorizationError(CloudSyncError):
    """Raised when an account is not authorized to synchronize."""


class SyncConflictError(CloudSyncError):
    """Raised when synchronization detects a conflicting record."""


class SyncIsolationError(CloudSyncError):
    """Raised when a record belongs to another account."""
