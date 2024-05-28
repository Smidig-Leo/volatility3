class Plugin:
    def __init__(self, name, command, description):
        self.name = name
        self.command = command
        self.description = description

    def execute(self, file_path):
        command = self.command.format(file_path=file_path, name=self.name)
        print(f"Executing command: {command}")
        return f"Simulated execution of {self.name} with {file_path}"
