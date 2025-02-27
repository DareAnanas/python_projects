from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import DictProperty, NumericProperty, ObjectProperty
from kivy.core.window import Window
import random


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
    confirmWordButton = ObjectProperty(None)
    backToMenuButton = ObjectProperty(None)
    randomWord = None
    inputWord = None
    app = None
    wordHistory = []

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        self.bindGameActions()
        self.gameStart()

    def gameStart(self):
        self.randomWord = self.app.getRandomWord()
        print(self.randomWord)

    def bindGameActions(self):
        self.confirmWordButton.bind(on_press=self.guessWord)
        self.backToMenuButton.bind(on_press=self.backToMenu)

    def unbindGameActions(self):
        self.confirmWordButton.unbind(on_press=self.guessWord)
        self.backToMenuButton.unbind(on_press=self.backToMenu)

    def guessWord(self, instance):
        self.inputWord = self.getInputWord()
        if (len(self.inputWord) != self.app.edition['length']):
            return
        if (self.inputWord not in self.app.edition['words']):
            return

        self.wordHistory.append(self.inputWord)

        if (len(self.wordHistory) >= 6):
            print('You lose')
            return

        print(self.wordHistory)
        print('Pierd')


    def getInputWord(self):
        return self.wordInput.text.strip().lower()

    def backToMenu(self, instance):
        self.manager.current = 'menu'


class DoodleWordApp(App):
    FONT_SCALE = 0.05

    theme = DictProperty(ThemeManager.light_theme)
    fontSize = NumericProperty(0)

    editions = {
        'fourLetter': {
            'length': 4,
            'words': ['піна', 'роса', 'баня', 'гора', 'лихо']
        },
        'fiveLetter': {
            'length': 5,
            'words': ['дошка', 'вудка', 'шапка', 'бочка', 'гірка']
        },
        'sixLetter': {
            'length': 6,
            'words': ['ролики', 'ананас', 'дракон', 'поезія', 'латунь']
        },
        'sevenLetter': {
            'length': 7,
            'words': ['барабан', 'ракетка', 'локшина', 'будинок', 'вершина']
        }
    }

    edition = editions['fiveLetter']

    def setEdition(self, mode):
        self.edition = self.editions[mode]

    def getRandomWord(self):
        return random.choice(self.edition['words'])

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