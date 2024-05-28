from .plugin import Plugin


class PluginManager:
    def __init__(self):
        self.plugins = []

    def load_plugins(self, os, file_path):
        plugin_data = [
            {
                "name": f"{os}.pslist",
                "command": "python ../vol.py -f {file_path} {name}",
                "description": "Displays a detailed list of all running processes on a system."
            },
            {
                "name": f"{os}.cmdline",
                "command": "python ../vol.py -f {file_path} {name}",
                "description": "Shows the command line arguments passed to each process."
            },
            {
                "name": f"{os}.dlllist",
                "command": "python ../vol.py -f {file_path} {name}",
                "description": "Lists the Dynamic Link Libraries (DLLs) loaded into each process's address space."
            },
            {
                "name": f"{os}.info",
                "command": "python ../vol.py -f {file_path} {name}",
                "description": "Provides detailed information about the operating system and kernel from a Windows memory dump."
            }
        ]

        self.plugins = [Plugin(**plugin) for plugin in plugin_data]

    def get_plugins(self):
        return self.plugins
