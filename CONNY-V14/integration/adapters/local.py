from integration.adapters.base import PlatformIntegrationAdapter
from integration.contracts.platform_contract import (
    ClientContext,
    IntegrationResult,
)


class LocalPlatformAdapter(PlatformIntegrationAdapter):

    def connect(self, context: ClientContext) -> IntegrationResult:
        return IntegrationResult(
            True,
            "connect",
            f"{context.platform.value} client connected",
        )

    def disconnect(self, context: ClientContext) -> IntegrationResult:
        return IntegrationResult(
            True,
            "disconnect",
            f"{context.platform.value} client disconnected",
        )
