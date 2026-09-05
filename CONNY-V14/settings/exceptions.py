class SettingsError(Exception):
    pass


class SettingsAuthorizationError(SettingsError):
    pass


class SettingsValidationError(SettingsError):
    pass


class SettingsIsolationError(SettingsError):
    pass
