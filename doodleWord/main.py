from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.properties import DictProperty, NumericProperty, \
ObjectProperty, ListProperty, StringProperty, ColorProperty
from kivy.core.window import Window
from kivy.factory import Factory
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

    cssColorsRgbaDict = {

    }

class ThemeManager:
    light_theme = {
        'bg_color': ColorConverter.hexToRgba('#FCFCFC'),
        'text_color': ColorConverter.hexToRgba('#1E1E1E'),
        'button_bg': ColorConverter.hexToRgba('#EC9D75'),
        'input_bg': ColorConverter.hexToRgba('#FCFCFC'),
        'stroke_color': ColorConverter.hexToRgba('#1E1E1E'),
        'logo_image': 'logo_light.png',
        'correct_color': ColorConverter.hexToRgba('#00C300'),
        'partly_correct_color': ColorConverter.hexToRgba('#D4EF07'),
        'incorrect_color': ColorConverter.hexToRgba('#B1B1B1'),
        'victory_color': ColorConverter.hexToRgba('#00C300'),
        'defeat_color': ColorConverter.hexToRgba('#FF0000')
    }
    dark_theme = {
        'bg_color': ColorConverter.hexToRgba('#1E1E1E'),
        'text_color': ColorConverter.hexToRgba('#FCFCFC'),
        'button_bg': ColorConverter.hexToRgba('#C16565'),
        'input_bg': ColorConverter.hexToRgba('#C16565'),
        'stroke_color': ColorConverter.hexToRgba('#FCFCFC'),
        'logo_image': 'logo_dark.png',
        'correct_color': ColorConverter.hexToRgba('#008000'),
        'partly_correct_color': ColorConverter.hexToRgba('#A1B907'),
        'incorrect_color': ColorConverter.hexToRgba('#808080'),
        'victory_color': ColorConverter.hexToRgba('#008000'),
        'defeat_color': ColorConverter.hexToRgba('#FF0000')
    }

class ThemedLabel(Label):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = App.get_running_app().theme['button_bg']
        

class DoodleWordMenu(Screen):

    def switchTheme(self):
        if (self.app.theme == ThemeManager.light_theme):
            self.app.theme = ThemeManager.dark_theme
        elif (self.app.theme == ThemeManager.dark_theme):
            self.app.theme = ThemeManager.light_theme


    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

class GameEndModal(ModalView):
    title = StringProperty('')
    color = ColorProperty([1, 1, 1, 1])
    restartButton = ObjectProperty(None)

    def __init__(self, title='', color=[1, 1, 1, 1], **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.color = color
        self.restartButton.bind(on_press=self.restartGame)

    def restartGame(self, instance):
        self.dismiss()
        App.get_running_app().root.get_screen('game').gameRestart()
        App.get_running_app().root.get_screen('game').gameStart()

class DoodleWordGame(Screen):
    
    wordGrid = ObjectProperty(None)
    wordInput = ObjectProperty(None)
    confirmWordButton = ObjectProperty(None)
    backToMenuButton = ObjectProperty(None)
    randomWord = None
    inputWord = None
    app = None
    wordHistory = []
    gridLabels = []
    rowIndex = 0

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        self.bindGameActions()
        self.gameStart()

    def gameStart(self):
        self.randomWord = self.app.getRandomWord()
        for i in range(5*6):
            themedLabel = ThemedLabel()
            self.gridLabels.append(themedLabel)
            self.wordGrid.add_widget(themedLabel)
        
        print(self.randomWord)

    def gameRestart(self):
        self.gridLabels.clear()
        self.wordGrid.clear_widgets()
        self.rowIndex = 0
        self.wordHistory.clear()

        self.bindGameActions()

    def gameEnd(self, state):
        self.unbindGameActions()

        if (state == 'victory'):
            gameEndModal = GameEndModal(
                title='Ти переміг!', 
                color=self.app.theme['victory_color']
            )
            gameEndModal.open()
        elif (state == 'defeat'):
            gameEndModal = GameEndModal(
                title='Ти програв!',
                color=self.app.theme['defeat_color']
            )
            gameEndModal.open()
        else:
            print('Розробник лох')

    def bindGameActions(self):
        self.confirmWordButton.bind(on_press=self.guessWord)
        self.backToMenuButton.bind(on_press=self.backToMenu)

    def unbindGameActions(self):
        self.confirmWordButton.unbind(on_press=self.guessWord)
        self.backToMenuButton.unbind(on_press=self.backToMenu)

    def checkLetterAndGetColor(self):
        for i in range(self.app.edition['length']):
            if (self.inputWord[i] == self.randomWord[i]):
                yield self.app.theme['correct_color'] # green
            elif (self.inputWord[i] in self.randomWord):
                yield self.app.theme['partly_correct_color'] # dark yellow
            else:
                yield self.app.theme['incorrect_color'] # gray


    def guessWord(self, instance):
        self.inputWord = self.getInputWord()
        if (len(self.inputWord) != self.app.edition['length']):
            return
        if (self.inputWord not in self.app.edition['words']):
            return

        self.wordHistory.append(self.inputWord)

        for i, letter in enumerate(self.inputWord):
            self.gridLabels[self.rowIndex * 5 + i].text = letter.upper()

        for i, color in enumerate(self.checkLetterAndGetColor()):
            self.gridLabels[self.rowIndex * 5 + i].bg_color = color
        
        self.rowIndex += 1

        self.wordInput.text = ''

        if (self.inputWord == self.randomWord):
            self.gameEnd(state='victory')
        elif (self.rowIndex >= 6):
            self.gameEnd(state='defeat')

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