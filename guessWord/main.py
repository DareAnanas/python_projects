from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class GuessWordGame(Screen):
    button = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.button.bind(texture_size=self.update_button_size)

    def update_button_size(self, instance, texture_size):
        padding = 30
        instance.size = [
            texture_size[0] + padding, 
            texture_size[1] + padding
        ]
        instance.center_x = self.width / 2

    def test(self):
        print('Clicked')

class GuessWordApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(GuessWordGame())
        
        return sm

if __name__ == '__main__':
    GuessWordApp().run()