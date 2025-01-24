from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty

class MainScreen(Screen):
    input = ObjectProperty(None)
    label = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.input.bind(text=self.transferText)

    def transferText(self, inputInstance, inputText):
        self.label.text = inputText
    

class TextInputApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    TextInputApp().run()