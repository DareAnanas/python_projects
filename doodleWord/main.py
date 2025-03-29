from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import DictProperty, NumericProperty, \
ObjectProperty, ListProperty, StringProperty, ColorProperty, BooleanProperty
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.clock import Clock
import random
import configparser
import os
from words import fourLetterWords, fiveLetterWords, sixLetterWords, sevenLetterWords


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
        'logo_image': 'logo_light.png',
        'correct_color': ColorConverter.hexToRgba('#00C300'),
        'partly_correct_color': ColorConverter.hexToRgba('#D4EF07'),
        'incorrect_color': ColorConverter.hexToRgba('#B1B1B1'),
        'victory_color': ColorConverter.hexToRgba('#00C300'),
        'defeat_color': ColorConverter.hexToRgba('#FF0000'),
        'left_arrow_image': 'left_arrow_light.png',
        'right_arrow_image': 'right_arrow_light.png',
        'changed_color': ColorConverter.hexToRgba('#C16565')
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
        'defeat_color': ColorConverter.hexToRgba('#FF0000'),
        'left_arrow_image': 'left_arrow_dark.png',
        'right_arrow_image': 'right_arrow_dark.png',
        'changed_color': ColorConverter.hexToRgba('#EC9D75')
    }

class ThemedLabel(Label):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = App.get_running_app().theme['button_bg']
        

class DoodleWordMenu(Screen):

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

    def goToSettings(self):
        self.manager.current = 'settings'
    
class WordLengthSpinBox(BoxLayout):
    app = None
    index = NumericProperty(1)
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.items = self.app.editionsNames

    def nextElement(self):
        if (self.index + 1 >= len(self.items)):
            return
        self.index += 1
        self.app.setEdition(self.items[self.index][0])
        self.app.root.get_screen('settings').changedSessionSettings = True
        self.app.clearUserWord()

    def prevElement(self):
        if (self.index <= 0):
            return
        self.index -= 1
        self.app.setEdition(self.items[self.index][0])
        self.app.root.get_screen('settings').changedSessionSettings = True
        self.app.clearUserWord()

class AttemptsSpinBox(BoxLayout):
    app = None
    index = NumericProperty(5)
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.items = self.app.attemptsNames

    def nextElement(self):
        if (self.index + 1 >= len(self.items)):
            return
        self.index += 1
        self.app.attempts = self.items[self.index][0]
        self.app.root.get_screen('settings').changedSessionSettings = True
        self.app.clearUserWord()

    def prevElement(self):
        if (self.index <= 0):
            return
        self.index -= 1
        self.app.attempts = self.items[self.index][0]
        self.app.root.get_screen('settings').changedSessionSettings = True
        self.app.clearUserWord()

class UserWordModal(ModalView):
    title = StringProperty('Загадай слово')
    wordInput = ObjectProperty(None)
    infoLabel = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

    def setInfoLabelColorForTime(self, color, time):
        self.infoLabel.color = color
        Clock.schedule_once(self.revertHintLabelColor, time)

    def revertHintLabelColor(self, dt):
        self.infoLabel.color = self.app.theme['text_color']

    def isUkrainianWord(self, word):
        ukrainianLetters = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")
        apostropheCount = 0

        for char in word:
            if (char not in ukrainianLetters):
                return False

        return True

    def hasTooManyApostrophes(self, word):
        apostropheCount = 0

        for char in word:
            if (char == "'"):
                apostropheCount += 1
                if (apostropheCount > 1):
                    return True
        
        return False

    def writeUserWord(self):
        if (len(self.wordInput.text) != self.app.edition['length']):
            if (self.app.edition['length'] == 4):
                self.title = "Слово має мати 4 букви"
            else:
                self.title = f"Слово має мати {self.app.edition['length']} букв"
            self.setInfoLabelColorForTime(self.app.theme['defeat_color'], 0.5)
            return

        inputWord = self.wordInput.text.lower()

        if (self.hasTooManyApostrophes(inputWord)):
            self.title = "Слово містить забагато апострофів"
            self.setInfoLabelColorForTime(self.app.theme['defeat_color'], 0.5)
            return

        if (not self.isUkrainianWord(inputWord)):
            self.title = "Слово містить не українські символи"
            self.setInfoLabelColorForTime(self.app.theme['defeat_color'], 0.5)
            return

        self.app.setUserWord(inputWord)
        self.app.root.get_screen('settings').changedSessionSettings = True

        self.dismiss()

class DoodleWordSettings(Screen):
    changedSettings = False
    changedSessionSettings = False

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()

    def changeSetting(self, key, value):
        self.app.settings[key] = value
        self.changedSettings = True

    def switchTheme(self):
        if (self.app.theme == ThemeManager.light_theme):
            self.app.theme = ThemeManager.dark_theme
            self.changeSetting('theme', 'dark')
        elif (self.app.theme == ThemeManager.dark_theme):
            self.app.theme = ThemeManager.light_theme
            self.changeSetting('theme', 'light')

    def writeConfig(self):
        config = configparser.ConfigParser()
        config['Settings'] = self.app.settings
        thisFileDir = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(thisFileDir, 'config.ini')
        with open(configPath, 'w') as file:
            config.write(file)

    def openUserWordModal(self):
        userWordModal = UserWordModal()
        userWordModal.open()

    def restartGameButtonAction(self):
        self.changedSessionSettings = False
        self.app.clearUserWord()
        self.restartGame()

    def restartGame(self):
        self.app.root.get_screen('game').gameRestart()

    def backToMenu(self):
        if (self.changedSessionSettings):
            self.changedSessionSettings = False
            self.restartGame()
        if (self.changedSettings):
            self.writeConfig()
        self.manager.current = 'menu'

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
        self.wordGrid.cols = self.app.edition['length']
        self.wordGrid.rows = self.app.attempts
        for i in range(self.app.edition['length']*self.app.attempts):
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

        self.gameStart()

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

    def getRowColors(self):
        rowColors = []

        for i in range(self.app.edition['length']):
            rowColors.append(self.app.theme['incorrect_color'])

        for i in range(self.app.edition['length']):
            if (self.inputWord[i] == self.randomWord[i]):
                rowColors[i] = self.app.theme['correct_color']

        partlyCorrectMemory = []

        for i in range(self.app.edition['length']):
            if (rowColors[i] == self.app.theme['incorrect_color']):
                isPartlyCorrectColor = False
                for j in range(self.app.edition['length']):
                    if (isPartlyCorrectColor):
                        continue
                    if (rowColors[j] == self.app.theme['correct_color']):
                        continue
                    if (j in partlyCorrectMemory):
                        continue
                    if (self.inputWord[i] == self.randomWord[j]):
                        partlyCorrectMemory.append(j)
                        isPartlyCorrectColor = True
                if (isPartlyCorrectColor):
                    rowColors[i] = self.app.theme['partly_correct_color']

        return rowColors

    def guessWord(self, instance):
        self.inputWord = self.getInputWord()
        if (len(self.inputWord) != self.app.edition['length']):
            return
        if (self.inputWord != self.randomWord and 
            self.inputWord not in self.app.edition['words']):
            return

        self.wordHistory.append(self.inputWord)

        for i, letter in enumerate(self.inputWord):
            self.gridLabels[self.rowIndex * self.app.edition['length'] + i].text = letter.upper()

        for i, color in enumerate(self.getRowColors()):
            self.gridLabels[self.rowIndex * self.app.edition['length'] + i].bg_color = color
        
        self.rowIndex += 1

        self.wordInput.text = ''

        if (self.inputWord == self.randomWord):
            self.gameEnd(state='victory')
        elif (self.rowIndex >= self.app.attempts):
            self.gameEnd(state='defeat')

        print(self.wordHistory)
        print('Pierd')


    def getInputWord(self):
        return self.wordInput.text.strip().lower()

    def backToMenu(self, instance):
        self.manager.current = 'menu'


class DoodleWordApp(App):
    FONT_SCALE = 0.05

    settings = {}

    theme = DictProperty({})
    fontSize = NumericProperty(0)

    editions = {
        'fourLetter': {
            'length': 4,
            'words': fourLetterWords
        },
        'fiveLetter': {
            'length': 5,
            'words': fiveLetterWords
        },
        'sixLetter': {
            'length': 6,
            'words': sixLetterWords
        },
        'sevenLetter': {
            'length': 7,
            'words': sevenLetterWords
        }
    }

    defaultAttempts = 6
    attempts = defaultAttempts

    attemptsNames = [
        [1, '1 спроба'],
        [2, '2 спроби'],
        [3, '3 спроби'],
        [4, '4 спроби'],
        [5, '5 спроб'],
        [6, '6 спроб'],
        [7, '7 спроб'],
        [8, '8 спроб']
    ]

    defaultEdition = 'fiveLetter'
    edition = editions[defaultEdition]

    editionsNames = [
        ['fourLetter','4 букви'],
        ['fiveLetter','5 букв'], 
        ['sixLetter','6 букв'], 
        ['sevenLetter','7 букв']
    ]

    userWord = ''
    userWordSetted = BooleanProperty(False)

    def setEdition(self, mode):
        self.edition = self.editions[mode]

    def setTheme(self, themeName):
        if (themeName == 'light'):
            self.theme = ThemeManager.light_theme
        elif (themeName == 'dark'):
            self.theme = ThemeManager.dark_theme

    def setUserWord(self, word):
        self.userWord = word
        self.userWordSetted = True

    def clearUserWord(self):
        self.userWord = ''
        self.userWordSetted = False

    def readSettings(self):
        config = configparser.ConfigParser()
        thisFileDir = os.path.dirname(os.path.abspath(__file__))
        configPath = os.path.join(thisFileDir, 'config.ini')
        config.read(configPath)

        themeName = config.get("Settings", "theme", fallback="light")
        self.setTheme(themeName)

    def getRandomWord(self):
        if (self.userWord != ''):
            userWord = self.userWord
            self.clearUserWord()
            return userWord
        return random.choice(self.edition['words'])

    def onWindowResize(self, window, size):
        self.fontSize = size[0] * self.FONT_SCALE
        print(self.fontSize)

    def build(self):
        Window.softinput_mode = 'below_target'

        self.readSettings()

        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(DoodleWordMenu(name='menu'))
        sm.add_widget(DoodleWordSettings(name='settings'))
        sm.add_widget(DoodleWordGame(name='game'))

        screen_width = Window.size[0]
        self.fontSize = screen_width * self.FONT_SCALE
        Window.bind(size=self.onWindowResize)

        return sm

if __name__ == '__main__':
    DoodleWordApp().run()