from dataclasses import dataclass

from integration.contracts.platform_contract import ClientContext
from integration.service import IntegrationService


@dataclass
class V14Runtime:
    integration: IntegrationService

    @classmethod
    def create(cls):
        return cls(
            integration=IntegrationService()
        )

    def connect_client(self, context: ClientContext):
        return self.integration.connect(context)

    def disconnect_client(self, context: ClientContext):
        return self.integration.disconnect(context)
