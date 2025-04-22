from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem
from kivy.properties import ObjectProperty, DictProperty
from kivy.uix.modalview import ModalView
import configparser
import os

class ViewTextFileModal(ModalView):
    textInput = ObjectProperty(None)
    
    def load_file(self):
        pass

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

    def sayHello(self):
        if (len(self.fileView.selection) != 0):
            print(self.fileView.path, self.fileView.selection[0])
        self.appMenu.close_all()
        viewTextFileModal = ViewTextFileModal()
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