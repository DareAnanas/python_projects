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
    label = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.randomWord = random.choice(self.words)
        print(self.randomWord)

    def guessWordPositions(word, guess):
        if guess == word:
            return -1
        
        correct_positions = 0
        for i in range(len(word)):
            if i < len(guess) and word[i] == guess[i]:
                correct_positions += 1
        
        return correct_positions

    def guessButtonAction(self):
        self.inputWord = self.getInputWord()
        if (self.checkWordLength() == True):
            self.checkWord()
        else:
            self.label.text = 'Your word must be ' + \
            str(len(self.randomWord)) + \
            ' letters'

    def getInputWord(self):
        return self.input.text.strip().lower()

    def checkWord(self):
        if (self.inputWord == self.randomWord):
            self.label.text = 'You guessed!'
        else:
            self.label.text = 'Wrong word.'

    def checkWordLength(self):
        if (len(self.inputWord) == len(self.randomWord)):
            return True
        else:
            return False

class GuessWordApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(GuessWordMenu(name='menu'))
        sm.add_widget(GuessWordGame(name='game'))

        return sm

if __name__ == '__main__':
    GuessWordApp().run()