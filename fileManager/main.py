from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from contextmenu import AppMenu, AppMenuTextItem, \
ContextMenu, ContextMenuTextItem

class FileManager(RelativeLayout):
    pass

class FileManagerApp(App):
    def build(self):
        return FileManager()

if __name__ == '__main__':
    FileManagerApp().run()