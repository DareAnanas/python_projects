from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):
    pass

class SecondScreen(Screen):
    pass

class BoxLayoutApp(App):
    def build(self):
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SecondScreen(name='second'))

        return sm


if __name__ == '__main__':
    BoxLayoutApp().run()