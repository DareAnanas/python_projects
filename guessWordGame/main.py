from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.clock import Clock
import random

ATTEMPTS = 10

class GuessWordMenu(Screen):
    pass

class GuessWordGame(Screen):
    words = ['chinza', 'pizza', 'pablo']
    randomWord = None
    inputWord = None
    input = ObjectProperty(None)
    hintLabel = ObjectProperty(None)
    attemptsLabel = ObjectProperty(None)
    guessButton = ObjectProperty(None)
    attempts = NumericProperty(ATTEMPTS)
    game_over = False

    def on_kv_post(self, base_widget):
        self.randomWord = random.choice(self.words)
        print(self.randomWord)

    def countCorrectPositions(self):
        correct_positions = 0

        for i in range(len(self.randomWord)):
            if i < len(self.inputWord) and self.randomWord[i] == self.inputWord[i]:
                correct_positions += 1
        
        return correct_positions

    def getInputWord(self):
        return self.input.text.strip().lower()

    def setHintLabelColorForTime(self, color, time):
        self.hintLabel.color = color
        Clock.schedule_once(self.revertHintLabelColor, time)

    def revertHintLabelColor(self, dt):
        self.hintLabel.color = 'white'

    def gameOver(self):
        self.game_over = True
        print(self.guessButton.text)
        self.guessButton.unbind(on_press=self.guessButtonAction)

    def guessButtonAction(self):
        self.attempts -= 1
        
        if (self.attempts <= 0):
            self.gameOver()

        self.inputWord = self.getInputWord()

        if (len(self.inputWord) != len(self.randomWord)):
            self.hintLabel.text = 'Your word must be ' + \
            str(len(self.randomWord)) + \
            ' letters'
            self.setHintLabelColorForTime('red', 0.5)
            return
        
        if (self.inputWord == self.randomWord):
            self.hintLabel.text = 'You guessed!'
            self.setHintLabelColorForTime('green', 0.5)
            return

        correctPositions = self.countCorrectPositions()

        if (correctPositions != 0):
            self.hintLabel.text = str(correctPositions) + \
                ' letter is on position'
            self.setHintLabelColorForTime('yellow', 0.5)
            return

        self.hintLabel.text = 'Wrong word'
        self.setHintLabelColorForTime('red', 0.5)

class GuessWordApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(GuessWordMenu(name='menu'))
        sm.add_widget(GuessWordGame(name='game'))

        return sm

if __name__ == '__main__':
    GuessWordApp().run()