class V14Application:

    def __init__(self, platform_adapter):
        self.platform = platform_adapter

    def authenticate(self, token, platform_context):
        return self.platform.authenticate(token, platform_context)

    def logout(self, token):
        return self.platform.logout(token)

    def read_memory(self, account):
        return self.platform.memory_read(account)

    def write_memory(self, account, content):
        return self.platform.memory_write(account, content)

    def delete_memory(self, account, memory_id):
        return self.platform.memory_delete(account, memory_id)

    def read_settings(self, account):
        return self.platform.settings_read(account)

    def write_setting(self, account, key, value):
        return self.platform.settings_write(account, key, value)

    def reset_setting(self, account, key):
        return self.platform.settings_reset(account, key)
