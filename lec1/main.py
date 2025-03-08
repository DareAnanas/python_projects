from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

class MainWindow(RelativeLayout):
    pass

class Lec1App(App):
    def build(self):
        mainWindow = MainWindow()
        return mainWindow

if __name__ == '__main__':
    Lec1App().run()