import json
from simpleAnalyze.utils.fileUploader import FileUploader


class SessionManager:
    session_data = {}
    def __init__(self):
        self.session_file = "session_data.json"
        self.session_data = self.load_session()
        self.fileUploader = FileUploader()
        print(f"Session file path: {self.session_file}")

    def load_session(self):
        try:
            with open(self.session_file, "r") as file:
                print(f"Loaded session data: {self.session_data}")
                return json.load(file)
        except FileNotFoundError:
            print("No session file found. Starting with empty session data.")
            return {}

    def save_session(self):
        with open(self.session_file, "w") as file:
            print(f"Saving session data: {self.session_data}")
            json.dump(self.session_data, file)

    def set_session_data(self, key, value):
        self.session_data[key] = value
        self.save_session()

    def set_file_uploaded(self, file_name):
        self.set_session_data("file_uploaded", file_name)

    def get_file_uploaded(self):
        print(f"File uploaded: {self.session_data.get('file_uploaded', self.fileUploader.get_file_path())}")
        return self.session_data.get("file_uploaded", self.fileUploader.get_file_path() or "")


    def set_activated_plugins(self, plugins):
        self.session_data["activated_plugins"] = plugins
        self.save_session()

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

