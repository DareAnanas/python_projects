from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem
from kivy.properties import ObjectProperty, DictProperty, StringProperty
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

    def on_kv_post(self, base_widget):
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

class NameModal(ModalView):
    nameInput = ObjectProperty(None)
    actionButton = ObjectProperty(None)

    def __init__(self, action, fileView, **kwargs):
        super().__init__(**kwargs)
        self.fileView = fileView
        if (action == 'rename'):
            self.filepath = self.fileView.selection[0]
            self.actionButton.bind(on_release=self.renameFile)
            self.actionButton.text = 'Rename'
            self.nameInput.text = os.path.basename(self.filepath)
        if (action == 'create'):
            self.actionButton.bind(on_release=self.createFile)
            self.actionButton.text = 'Create'

    def renameFile(self, *args):
        fileDir = os.path.dirname(self.filepath)
        newFileName = self.nameInput.text.strip()
        os.rename(self.filepath, os.path.join(fileDir, newFileName))
        self.fileView._trigger_update()
        self.dismiss()

    def createFile(self, *args):
        fileName = self.nameInput.text.strip()
        filePath = os.path.join(self.fileView.path, fileName)
        if not os.path.exists(filePath):
            with open(filePath, 'w') as file:
                pass
        else:
            print('File already exists')
        self.fileView._trigger_update()
        self.dismiss()

class DeleteFileModal(ModalView):
    
    def __init__(self, fileView, **kwargs):
        super().__init__(**kwargs)
        self.fileView = fileView
        self.filepath = self.fileView.selection[0]

    def deleteFile(self):
        os.remove(self.filepath)
        self.fileView._trigger_update()
        self.dismiss()


class FileManager(RelativeLayout):
    fileView = ObjectProperty(None)
    appMenu = ObjectProperty(None)
    contextMenu = ObjectProperty(None)

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

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and touch.button == 'right':
            self.contextMenu.show(*touch.pos)

    def closeHandler(self, menuType, func):
        if (menuType == 'app'):
            self.appMenu.close_all()
        if (menuType == 'context'):
            self.contextMenu.hide()
        func()

    def viewTextFile(self):
        if (len(self.fileView.selection) == 0):
            return
        if (os.path.isdir(self.fileView.selection[0])):
            return
        viewTextFileModal = ViewTextFileModal(self.fileView.selection[0])
        viewTextFileModal.open()

    def renameFile(self):
        if (len(self.fileView.selection) == 0):
            return
        if (os.path.isdir(self.fileView.selection[0])):
            return
        renameModal = NameModal('rename', self.fileView)
        renameModal.open()

    def deleteFile(self):
        if (len(self.fileView.selection) == 0):
            return
        if (os.path.isdir(self.fileView.selection[0])):
            return
        deleteFileModal = DeleteFileModal(self.fileView)
        deleteFileModal.open()

    def createFile(self):
        createFileModal = NameModal('create', self.fileView)
        createFileModal.open()

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