import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import subprocess


class SelectFileScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectFileScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.file_label = Label(text="No memory dump selected", color=(1, 1, 1, 1), size_hint=(1, None), height=40)
        layout.add_widget(self.file_label)

        self.select_button = Button(text="Select Memory Dump", background_color=(1, 0.5, 0, 1), size_hint=(1, None),
                                    height=50)
        self.select_button.bind(on_press=self.select_file)
        layout.add_widget(self.select_button)

        self.add_widget(layout)

    def select_file(self, instance):
        content = FileChooserListView(on_submit=self.on_file_select)
        self.popup = Popup(title="Select Memory Dump", content=content, size_hint=(0.9, 0.9))
        self.popup.open()

    def on_file_select(self, chooser, selection, touch):
        if selection:
            self.file_path = selection[0]
            self.file_label.text = f"Selected file: {self.file_path}"
            self.popup.dismiss()
            self.manager.get_screen('plugin_screen').file_path = self.file_path
            self.manager.get_screen('plugin_screen').file_label.text = f"Selected file: {self.file_path}"


class PluginScreen(Screen):
    def __init__(self, **kwargs):
        super(PluginScreen, self).__init__(**kwargs)
        self.file_path = ""
        self.selected_plugins = []

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.file_label = Label(text="No memory dump selected", color=(1, 1, 1, 1), size_hint=(1, None), height=40)
        layout.add_widget(self.file_label)

        plugin_layout = BoxLayout(size_hint_y=None, height=50)
        self.plugins = ["windows.pslist", "windows.cmdline", "windows.dlllist", "windows.info"]

        for plugin in self.plugins:
            btn = Button(text=plugin, size_hint_y=None, height=50)
            btn.bind(on_press=self.toggle_plugin)
            plugin_layout.add_widget(btn)

        layout.add_widget(plugin_layout)

        self.run_button = Button(text="Run Analysis", background_color=(0, 1, 0, 1), size_hint=(1, None), height=50)
        self.run_button.bind(on_press=self.run_analysis)
        layout.add_widget(self.run_button)

        self.add_widget(layout)

    def toggle_plugin(self, instance):
        if instance.text in self.selected_plugins:
            self.selected_plugins.remove(instance.text)
            instance.background_color = (1, 1, 1, 1)
        else:
            self.selected_plugins.append(instance.text)
            instance.background_color = (0, 1, 0, 1)

    def run_analysis(self, instance):
        if self.file_path:
            self.manager.get_screen('analyzed_data_screen').output_text.text = ""
            for plugin in self.selected_plugins:
                cmd = f"python vol.py -f {self.file_path} {plugin}"
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                self.manager.get_screen(
                    'analyzed_data_screen').output_text.text += f"Output for {plugin}:\n{result.stdout}\n{'=' * 40}\n"
            self.manager.current = 'analyzed_data_screen'
        else:
            self.manager.get_screen('analyzed_data_screen').output_text.text = "No memory dump selected"


class AnalyzedDataScreen(Screen):
    def __init__(self, **kwargs):
        super(AnalyzedDataScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.output_text = TextInput(multiline=True, readonly=True, background_color=(0.2, 0.2, 0.2, 1),
                                     foreground_color=(1, 1, 1, 1))
        layout.add_widget(self.output_text)
        self.add_widget(layout)


class VolatilityApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        self.sm = ScreenManager()
        self.sm.add_widget(SelectFileScreen(name='select_file_screen'))
        self.sm.add_widget(PluginScreen(name='plugin_screen'))
        self.sm.add_widget(AnalyzedDataScreen(name='analyzed_data_screen'))

        main_layout = BoxLayout(orientation='vertical')

        button_layout = BoxLayout(size_hint_y=None, height=50)
        select_file_button = Button(text="Select File")
        select_file_button.bind(on_press=self.show_select_file_screen)
        button_layout.add_widget(select_file_button)

        plugins_button = Button(text="Plugins")
        plugins_button.bind(on_press=self.show_plugin_screen)
        button_layout.add_widget(plugins_button)

        analyzed_data_button = Button(text="Analyzed Data")
        analyzed_data_button.bind(on_press=self.show_analyzed_data_screen)
        button_layout.add_widget(analyzed_data_button)

        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.sm)

        return main_layout

    def show_select_file_screen(self, instance):
        self.sm.current = 'select_file_screen'

    def show_plugin_screen(self, instance):
        self.sm.current = 'plugin_screen'

    def show_analyzed_data_screen(self, instance):
        self.sm.current = 'analyzed_data_screen'


if __name__ == '__main__':
    VolatilityApp().run()
