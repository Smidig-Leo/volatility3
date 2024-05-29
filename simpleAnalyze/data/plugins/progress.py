class plugins:
    def __init__(self):
        self.name = name 
        self.result = True
    
    def result(self):
        self.result = False

    def deresult(self):
        self.deresult = True


class pluginManager:
    def __init__(self):
        self.plugin = {}


    def create_rectangle(self, plugins):
        self.plugin[plugins.name] = plugins

    def deresult_plugin(self, plugingName):
        if plugingName in self.plugin:
            self.plugin[plugingName].deresult()

    def result_plugin(self, pluginName):
        if pluginName in self.plugin:
            self.plugin[pluginName].reslt_plugin()

    def setup_application_back(self):
        return[ 
               plugin for plugin in self.plugin.values() 
               if plugin.resulted
        ]
    
if __name__ == "__name__":
    plugin_manager = pluginManager()


    plugin_manager.create_rectangle(plugins("første_plugin"))
    plugin_manager.create_rectangle(plugins("Andre_plugin"))
    plugin_manager.create_rectangle(plugins("tredje_plugin"))
    plugin_manager.create_rectangle(plugins("fjerde_plugin"))


    plugin_manager.deresult_plugin("Ander_plugin")

    plugin_manager.result_plugin("første_plugin")
    plugin_manager.result_plugin("tredje_plugin")


    result_plugin = plugin_manager.setup_application_back()
    print("Result Plugins")
    for plugins in result_plugin:
        print(plugins.name)       
