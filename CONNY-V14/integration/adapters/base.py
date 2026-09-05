from abc import ABC, abstractmethod

from integration.contracts.platform_contract import (
    ClientContext,
    IntegrationResult,
)


class PlatformIntegrationAdapter(ABC):

    @abstractmethod
    def connect(self, context: ClientContext) -> IntegrationResult:
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, context: ClientContext) -> IntegrationResult:
        raise NotImplementedError
