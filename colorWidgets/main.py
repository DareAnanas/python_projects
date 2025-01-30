from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.button import Button

class ColorMenu(Screen):
    pass

class ColorApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(ColorMenu(name='menu'))
        return sm

if __name__ == '__main__':
    ColorApp().run()