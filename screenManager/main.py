from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, \
FadeTransition, SwapTransition

class ScreenManagerApp(App):
    def change_screen(self):
        pass
    
    def build(self):
        sm = ScreenManager(transition = FadeTransition())

        sm.add_widget(MenuScreen(name = 'menu'))
        sm.add_widget(SettingsScreen(name = 'settings'))

        return sm

class MenuScreen(Screen):
    def change_screen(self):
        self.manager.transition = SwapTransition()
        self.manager.current = 'settings'

class SettingsScreen(Screen):
    def change_screen(self):
        self.manager.transition = FadeTransition()
        self.manager.current = 'menu'

if __name__ == '__main__':
    ScreenManagerApp().run()