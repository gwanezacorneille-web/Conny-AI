from integration.adapters.local import LocalPlatformAdapter
from integration.contracts.platform_contract import (
    ClientContext,
    ClientPlatform,
    IntegrationResult,
)


class IntegrationService:

    SUPPORTED = {
        ClientPlatform.WINDOWS,
        ClientPlatform.LINUX,
        ClientPlatform.ANDROID,
        ClientPlatform.WEB,
    }

    def __init__(self):
        self.adapter = LocalPlatformAdapter()

    def connect(self, context: ClientContext) -> IntegrationResult:
        if context.platform not in self.SUPPORTED:
            raise ValueError("Unsupported client platform")

        if not context.client_version:
            raise ValueError("Client version required")

        if not context.device_id:
            raise ValueError("Device ID required")

        return self.adapter.connect(context)

    def disconnect(self, context: ClientContext) -> IntegrationResult:
        return self.adapter.disconnect(context)
