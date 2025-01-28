from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
from kivy.properties import ObjectProperty
import random

class GuessWordMenu(Screen):
    pass

class GuessWordGame(Screen):
    words = ['chinza', 'pizza', 'pablo']
    randomWord = None
    inputWord = None
    input = ObjectProperty(None)
    hintLabel = ObjectProperty(None)

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

    def guessButtonAction(self):
        self.inputWord = self.getInputWord()

        if (len(self.inputWord) != len(self.randomWord)):
            self.hintLabel.text = 'Your word must be ' + \
            str(len(self.randomWord)) + \
            ' letters'
            return
        
        if (self.inputWord == self.randomWord):
            self.hintLabel.text = 'You guessed!'
            return

        correctPositions = self.countCorrectPositions()

        if (correctPositions != 0):
            self.hintLabel.text = str(correctPositions) + \
                ' letter is on position'
            return

        self.hintLabel.text = 'Wrong word'

class GuessWordApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(GuessWordMenu(name='menu'))
        sm.add_widget(GuessWordGame(name='game'))

        return sm

if __name__ == '__main__':
    GuessWordApp().run()