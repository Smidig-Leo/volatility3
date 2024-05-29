class Plugin:
    def __init__(self, name, select = False):
        self.name = name
        self.select = select

class PluginManager:

    def __init__(self):
        self.plugin = []

    def register_plugin(self, name):
        self.plugin.append(Plugin(name))

    def deactivate_cronjob_plugin(self, name):
        for plugin in self.plugin:
            if plugin.name == name:
                plugin.select = True
   
    
    def activate_cronjob_plugin(self, name):
        for plugin in self.plugin:
            if plugin.name == name:
                plugin.select = False
    

    def get_activate_plugins(self):
        return[Plugin for plugin in self.plugin if plugin.select]
    

    plugin_manager = pluginManager()


    plugin_manager.register_plugin("første_plugin")
    plugin_manager.register_plugin("andre_plugin")
    plugin_manager.register_plugin("tredje_pligin")


    activate_cronjob_plugin = plugin_manager.select()
    print("Select Plugins")