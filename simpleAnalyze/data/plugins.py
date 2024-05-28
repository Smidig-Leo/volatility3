class Plugin:
    def __init__(self, name):
        self.name = name
    
    def analyze_data(self, data):
        pass

class PluginArguments:
    def __init__(self):
        self.plugins = []
    
    def register_plugin(self, plugin):
        self.plugins.append(plugin)
    
    def get_plugins(self):
        return self.plugins

class PluginName(Plugin):
    def __init__(self, name):
        super().__init__(name)
    
    def analyze_data(self, data):
        if self.name =="første_plugin":
            pass

        elif self.name == "andre_plugin":
            pass

        elif self.name == "tredje_plugin":
            pass

        elif self.name == "fjerde_plugin":
            pass

if __name__ == "_main_":
    Plugin_arguments = PluginArguments()
    
    PluginArguments.register_plugin(PluginName("første_plugin"))
    PluginArguments.register_plugin(PluginName("andre_plugin"))
    PluginArguments.register_plugin(PluginName("tredje_plugin"))
    PluginArguments.register_plugin(PluginName("fjerde_plugin"))
    
    data = [...] 
    for plugin in PluginArguments.get_plugins():
        plugin.analyze_data(data)