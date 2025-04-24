from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
import configparser
import os

class ViewTextFileModal(ModalView):
    textInput = ObjectProperty(None)
    
    def __init__(self, filepath, **kwargs):
        super().__init__(**kwargs)
        self.filepath = filepath
        self.load_file()

    def on_kv_post(self, bimba):
        Clock.schedule_once(self.setCursorToStart, 0)

    def load_file(self):
        with open(self.filepath, 'r') as stream:
            self.textInput.text = stream.read()

    def save_file(self):
        with open(self.filepath, 'w') as stream:
            stream.write(self.textInput.text)
        self.dismiss()

    def setCursorToStart(self, delta):
        self.textInput.cursor = (0, 0)
        self.textInput.focus = True

class FileManager(RelativeLayout):
    fileView = ObjectProperty(None)
    appMenu = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.fileView.bind(path=self.on_path_change)

    def changeSetting(self, key, value):
        self.app.settings[key] = value

    def writeConfig(self):
        config = configparser.ConfigParser()
        config['Settings'] = self.app.settings
        thisFileDir = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(thisFileDir, 'config.ini')
        with open(configPath, 'w') as file:
            config.write(file)

    def on_path_change(self, fileView, path):
        self.changeSetting('last_path', path)
        self.writeConfig()

    def viewTextFile(self):
        self.appMenu.close_all()
        if (len(self.fileView.selection) == 0):
            return
        if (os.path.isdir(self.fileView.selection[0])):
            return
        print(self.fileView.path, self.fileView.selection[0])
        viewTextFileModal = ViewTextFileModal(self.fileView.selection[0])
        viewTextFileModal.open()


class FileManagerApp(App):
    settings = {}

    def changeSetting(self, key, value):
        self.settings[key] = value

    def readSettings(self):
        config = configparser.ConfigParser()
        thisFileDir = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(thisFileDir, 'config.ini')
        config.read(configPath)

        last_path = config.get("Settings", "last_path", fallback="/home/danylo")
        self.changeSetting('last_path', last_path)

    def build(self):
        self.readSettings()
        return FileManager()

if __name__ == '__main__':
    FileManagerApp().run()