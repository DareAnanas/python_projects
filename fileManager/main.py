from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem
from kivy.properties import ObjectProperty, DictProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivy.clock import Clock
from kivy.uix.behaviors import ToggleButtonBehavior
import configparser
import os

from kivy.uix.togglebutton import ToggleButton
from kivy.uix.filechooser import FileChooserListView

class ViewTextFileModal(ModalView):
    textInput = ObjectProperty(None)
    
    def __init__(self, fileView, **kwargs):
        super().__init__(**kwargs)
        self.fileView = fileView
        self.filepath = self.fileView.selection[0]
        self.load_file()

    def on_kv_post(self, base_widget):
        Clock.schedule_once(self.setCursorToStart, 0)

    def load_file(self):
        with open(self.filepath, 'r') as stream:
            self.textInput.text = stream.read()

    def save_file(self):
        with open(self.filepath, 'w') as stream:
            stream.write(self.textInput.text)
        self.fileView.selection = []
        self.fileView._trigger_update()
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
        if (action == 'createDir'):
            self.actionButton.bind(on_release=self.createDir)
            self.actionButton.text = 'Create'

    def renameFile(self, *args):
        fileDir = os.path.dirname(self.filepath)
        newFileName = self.nameInput.text.strip()
        if (newFileName == ''):
            print('Empty file name')
            self.dismiss()
            return
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

    def createDir(self, *args):
        dirName = self.nameInput.text.strip()
        dirPath = os.path.join(self.fileView.path, dirName)
        if (not os.path.exists(dirPath)):
            os.mkdir(dirPath)
        else:
            print('Directory already exists')
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
        viewTextFileModal = ViewTextFileModal(self.fileView)
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

    def createSortFunc(self, criteria, order):

        reverse = False
        if (order == 'z-a'):
            reverse = True

        def sortByName(files, filesystem):
            return (sorted((f for f in files if filesystem.is_dir(f)), reverse=reverse) +
                sorted((f for f in files if not filesystem.is_dir(f)), reverse=reverse))

        def sortByDate(files, filesystem):
            return (sorted((f for f in files if filesystem.is_dir(f))) +
                sorted((f for f in files if not filesystem.is_dir(f)), 
                    key=lambda f: os.path.getmtime(f), reverse=reverse))

        def sortByType(files, filesystem):
            return (sorted((f for f in files if filesystem.is_dir(f))) +
                sorted((f for f in files if not filesystem.is_dir(f)), 
                    key=lambda f: os.path.splitext(os.path.basename(f))[1], reverse=reverse))

        def sortBySize(files, filesystem):
            return (sorted((f for f in files if filesystem.is_dir(f))) +
                sorted((f for f in files if not filesystem.is_dir(f)),
                    key=lambda f: filesystem.getsize(f), reverse=reverse))

        if (criteria == 'name'):
            return sortByName
        if (criteria == 'date'):
            return sortByDate
        if (criteria == 'type'):
            return sortByType
        if (criteria == 'size'):
            return sortBySize
        
        return sortByName

    def getSortCriteria(self):
        for toggleButton in ToggleButtonBehavior.get_widgets('criteria'):
            if toggleButton.state == 'down':
                return toggleButton.text.lower()
        return 'name'

    def getSortOrder(self):
        for toggleButton in ToggleButtonBehavior.get_widgets('order'):
            if toggleButton.state == 'down':
                return toggleButton.text.lower()
        return 'a-z'

    def sortFiles(self):
        criteria = self.getSortCriteria()
        order = self.getSortOrder()
        self.fileView.sort_func = self.createSortFunc(criteria, order)
        self.fileView.selection = []
        self.fileView._trigger_update()

    def goToParentDir(self):
        parentDir = os.path.dirname(self.fileView.path)
        self.fileView.path = parentDir

    def goToHomeDir(self):
        self.fileView.path = self.fileView.rootpath

    def createDir(self):
        createDirModal = NameModal('createDir', self.fileView)
        createDirModal.open()

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