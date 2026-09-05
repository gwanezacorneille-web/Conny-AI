from v14_platform.models import PlatformContext, PlatformType


class PlatformAdapter:
    """
    V14 cross-platform boundary.

    Platform applications communicate with V14 through this
    boundary instead of importing V13 internals.
    """

    SUPPORTED = {
        PlatformType.WINDOWS,
        PlatformType.LINUX,
        PlatformType.ANDROID,
    }

    def __init__(
        self,
        account_service,
        memory_service,
        security_service,
        cloud_service=None,
        settings_service=None,
    ):
        self.account_service = account_service
        self.memory_service = memory_service
        self.security_service = security_service
        self.cloud_service = cloud_service
        self.settings_service = settings_service

    def validate_platform(self, context):
        if not isinstance(context, PlatformContext):
            return False

        return (
            context.is_supported
            and context.platform in self.SUPPORTED
            and bool(context.app_version)
            and bool(context.device_id)
        )

    def authenticate(self, token, context):
        if not self.validate_platform(context):
            raise ValueError("Invalid V14 platform context")

        return self.security_service.authenticate(token)

    def logout(self, token):
        return self.security_service.logout(token)

    def memory_read(self, account):
        return self.memory_service.recall(account)

    def memory_write(self, account, content):
        return self.memory_service.remember(account, content)

    def memory_delete(self, account, memory_id):
        return self.memory_service.forget(account, memory_id)

    def settings_read(self, account):
        if self.settings_service is None:
            raise RuntimeError("Settings service unavailable")

        return self.settings_service.get_all(account)

    def settings_write(self, account, key, value):
        if self.settings_service is None:
            raise RuntimeError("Settings service unavailable")

        return self.settings_service.set(account, key, value)

    def settings_reset(self, account, key):
        if self.settings_service is None:
            raise RuntimeError("Settings service unavailable")

        return self.settings_service.reset(account, key)
