from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty

class GuessWordMenu(Screen):
    pass

class GuessWordGame(Screen):
    words = ['chinza', 'pizza', 'pablo']
    input = ObjectProperty(None)

    def checkWord(self):
        pass

class GuessWordApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(GuessWordMenu(name='menu'))
        sm.add_widget(GuessWordGame(name='game'))

        return sm

if __name__ == '__main__':
    GuessWordApp().run()