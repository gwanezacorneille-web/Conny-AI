import os
import importlib


class PluginLoader:


    def __init__(self):

        self.plugins = []



    def load_plugins(self):

        plugin_folder = "plugins"


        for file in os.listdir(plugin_folder):

            if file.endswith("_plugin.py"):

                module_name = (
                    file[:-3]
                )


                module = importlib.import_module(
                    f"plugins.{module_name}"
                )


                for item in dir(module):

                    obj = getattr(
                        module,
                        item
                    )


                    if (
                        isinstance(obj, type)
                        and item.endswith("Plugin")
                        and item != "PluginLoader"
                    ):

                        self.plugins.append(
                            obj()
                        )


        return self.plugins
