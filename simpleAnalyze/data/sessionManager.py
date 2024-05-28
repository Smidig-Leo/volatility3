import json
import simpleAnalyze.utils.fileUploader as fileUploader


class SessionManager:
    def __init__(self):
        self.session_file = "session_data.json"
        self.session_data = {}

    def save_session(self):
        with open(self.session_file, "w") as file:
            json.dump(self.session_data, file)

    def load_session(self):
        try:
            with open(self.session_file, "r") as file:
                self.session_data = json.load(file)
        except FileNotFoundError:
            pass

    def set_file_uploaded(self, file_path):
        self.session_data["file_uploaded"] = file_path

    def get_file_uploaded(self):
        return self.session_data.get("file_uploaded", "")

    def set_activated_plugins(self, plugins):
        self.session_data["activated_plugins"] = plugins

    def get_activated_plugins(self):
        return self.session_data.get("activated_plugins", [])

    def set_language(self, language):
        self.session_data["language"] = language

    def get_language(self):
        return self.session_data.get("language", "")

    def set_dark_mode(self, dark_mode):
        self.session_data["dark_mode"] = dark_mode

    def get_dark_mode(self):
        return self.session_data.get("dark_mode", bool)

    def set_os(self, os):
        self.session_data["os"] = os

    def get_os(self):
        return self.session_data.get("os", "")


# Usage:
session_manager = SessionManager()
session_manager.load_session()

# Example: Set file uploaded
file_path = fileUploader.FileUploader.get_file_path()
session_manager.set_file_uploaded(file_path)
session_manager.save_session()

# Example: Get file uploaded
file_uploaded = session_manager.get_file_uploaded()
print("File uploaded:", file_uploaded)
