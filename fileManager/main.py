from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem
from kivy.properties import ObjectProperty

class FileManager(RelativeLayout):
    fileView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fileView.bind(path=self.on_path_change)

    def on_path_change(self, fileView, path):
        print(path)

class FileManagerApp(App):
    def build(self):
        return FileManager()

if __name__ == '__main__':
    FileManagerApp().run()