import json

from settings.exceptions import (
    SettingsAuthorizationError,
    SettingsIsolationError,
    SettingsValidationError,
)
from settings.models import (
    SettingDefinition,
    SettingValue,
)


class SettingsService:

    DEFINITIONS = {
        "theme": SettingDefinition(
            "theme",
            "dark",
            str,
        ),
        "language": SettingDefinition(
            "language",
            "en",
            str,
        ),
        "voice_enabled": SettingDefinition(
            "voice_enabled",
            True,
            bool,
        ),
        "notifications_enabled": SettingDefinition(
            "notifications_enabled",
            True,
            bool,
        ),
        "memory_enabled": SettingDefinition(
            "memory_enabled",
            True,
            bool,
        ),
        "sync_enabled": SettingDefinition(
            "sync_enabled",
            True,
            bool,
        ),
    }

    def __init__(
        self,
        store,
        security_service,
        audit_logger,
    ):
        self.store = store
        self.security_service = security_service
        self.audit_logger = audit_logger

    def _authorize(
        self,
        account,
        permission="settings.read",
    ):
        if account is None or not account.is_active:
            raise SettingsAuthorizationError(
                "Active account required for settings"
            )

        if not self.security_service.authorize(
            account,
            permission,
        ):
            raise SettingsAuthorizationError(
                f"Account is not authorized for {permission}"
            )

    def _definition(self, key):
        definition = self.DEFINITIONS.get(key)

        if definition is None:
            raise SettingsValidationError(
                f"Unknown setting: {key}"
            )

        return definition

    def _serialize(self, value, value_type):
        if value_type is bool:
            return json.dumps(value)

        return str(value)

    def _deserialize(self, raw, value_type):
        if value_type is bool:
            return bool(json.loads(raw))

        return value_type(raw)

    def _validate_value(
        self,
        definition,
        value,
    ):
        if type(value) is not definition.value_type:
            raise SettingsValidationError(
                f"{definition.key} requires "
                f"{definition.value_type.__name__}"
            )

    def get(
        self,
        account,
        key,
    ):
        self._authorize(
            account,
            "settings.read",
        )

        definition = self._definition(key)
        stored = self.store.get(
            account.user_id,
            key,
        )

        if stored is None:
            value = definition.default
        else:
            value = self._deserialize(
                stored["value"],
                definition.value_type,
            )

        return SettingValue(
            account.user_id,
            key,
            value,
        )

    def get_all(self, account):
        self._authorize(
            account,
            "settings.read",
        )

        result = {}

        for key, definition in self.DEFINITIONS.items():
            result[key] = self.get(
                account,
                key,
            ).value

        return result

    def set(
        self,
        account,
        key,
        value,
    ):
        self._authorize(
            account,
            "settings.write",
        )

        definition = self._definition(key)
        self._validate_value(
            definition,
            value,
        )

        self.store.set(
            account.user_id,
            key,
            self._serialize(
                value,
                definition.value_type,
            ),
            definition.value_type.__name__,
        )

        self.audit_logger(
            "SETTING_UPDATED",
            account.user_id,
        )

        return SettingValue(
            account.user_id,
            key,
            value,
        )

    def reset(
        self,
        account,
        key,
    ):
        self._authorize(
            account,
            "settings.reset",
        )

        definition = self._definition(key)

        self.store.delete(
            account.user_id,
            key,
        )

        self.audit_logger(
            "SETTING_RESET",
            account.user_id,
        )

        return SettingValue(
            account.user_id,
            key,
            definition.default,
        )
