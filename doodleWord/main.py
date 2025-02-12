from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import DictProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.textinput import TextInput

class ColorConverter:

    def hexToRgba(hex_color, alpha=1):
        # Convert a hex color string to an RGBA tuple (0-1 range).
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return [round(r / 255.0, 4), round(g / 255.0, 4), round(b / 255.0, 4), alpha]

    hexRgbaDict = {
        '#FCFCFC': [252, 252, 252, 1],
        '#1E1E1E': [30, 30, 30, 1],
        '#EC9D75': [236, 157, 117, 1],
        '#C16565': [193, 101, 101, 1]
    }

class ThemeManager:
    light_theme = {
        'bg_color': ColorConverter.hexToRgba('#FCFCFC'),
        'text_color': ColorConverter.hexToRgba('#1E1E1E'),
        'button_bg': ColorConverter.hexToRgba('#EC9D75'),
        'input_bg': ColorConverter.hexToRgba('#FCFCFC'),
        'stroke_color': ColorConverter.hexToRgba('#1E1E1E'),
        'logo_image': 'logo_light.png'
    }
    dark_theme = {
        'bg_color': ColorConverter.hexToRgba('#1E1E1E'),
        'text_color': ColorConverter.hexToRgba('#FCFCFC'),
        'button_bg': ColorConverter.hexToRgba('#C16565'),
        'input_bg': ColorConverter.hexToRgba('#C16565'),
        'stroke_color': ColorConverter.hexToRgba('#FCFCFC'),
        'logo_image': 'logo_dark.png'
    }



class DoodleWordMenu(Screen):

    def switchTheme(self):
        if (self.app.theme == ThemeManager.light_theme):
            self.app.theme = ThemeManager.dark_theme
        elif (self.app.theme == ThemeManager.dark_theme):
            self.app.theme = ThemeManager.light_theme


    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

class DoodleWordGame(Screen):
    
    wordInput = ObjectProperty(None)
    backToMenuButton = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.bindGameActions()

    def bindGameActions(self):
        self.backToMenuButton.bind(on_press=self.backToMenu)

    def unbindGameActions(self):
        self.backToMenuButton.unbind(on_press=self.backToMenu)

    def backToMenu(self, instance):
        self.manager.current = 'menu'


class DoodleWordApp(App):
    FONT_SCALE = 0.05

    theme = DictProperty(ThemeManager.light_theme)
    fontSize = NumericProperty(0)

    def onWindowResize(self, window, size):
        self.fontSize = size[0] * self.FONT_SCALE

    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(DoodleWordMenu(name='menu'))
        sm.add_widget(DoodleWordGame(name='game'))
        
        screen_width = Window.size[0]
        self.fontSize = screen_width * self.FONT_SCALE
        Window.bind(size=self.onWindowResize)

        return sm

if __name__ == '__main__':
    DoodleWordApp().run()