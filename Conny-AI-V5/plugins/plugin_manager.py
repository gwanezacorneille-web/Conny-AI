class PluginManager:


    def __init__(self):

        self.plugins = []


    def register(self, plugin):

        self.plugins.append(plugin)



    def find_plugin(self, message):

        for plugin in self.plugins:

            if plugin.can_handle(message):

                return plugin


        return None
