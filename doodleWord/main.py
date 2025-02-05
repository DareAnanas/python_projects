from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import DictProperty


class ThemeManager:
    light_theme = {
        'bg_color': '#FCFCFC',
        'text_color': '#1E1E1E',
        'button_bg': '#EC9D75',
        'input_bg': '#FCFCFC',
        'stroke_color': '#1E1E1E'
    }
    dark_theme = {
        'bg_color': '#1E1E1E',
        'text_color': '#FCFCFC',
        'button_bg': '#C16565',
        'input_bg': '#C16565',
        'stroke_color': '#8F8F8F'
    }



class DoodleWordMenu(Screen):

    def switchTheme(self):
        if (app.theme == ThemeManager.light_theme):
            app.theme = ThemeManager.dark_theme
        elif (app.theme == ThemeManager.dark_theme):
            app.theme = ThemeManager.light_theme


    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

class DoodleWordApp(App):
    theme = DictProperty(ThemeManager.light_theme)




    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(DoodleWordMenu(name='menu'))

        return sm

if __name__ == '__main__':
    DoodleWordApp().run()