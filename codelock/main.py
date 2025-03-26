from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button

class CodeLock(Screen):
    displayLabel = ObjectProperty(None)
    CORRECT_CODE = "1378"
    code = ''

    def handleDigit(self, digit):
        if (len(self.code) >= 4):
            return
        self.code += digit
        self.displayLabel.text = self.code
        self.displayLabel.color = 'white'

    def handleBack(self):
        self.code = self.code[:-1]
        self.displayLabel.text = self.code

    def handleEnter(self):
        if (self.code == self.CORRECT_CODE):
            self.displayLabel.text = 'Вірно!'
            self.displayLabel.color = 'green'
        else:
            self.displayLabel.text = 'Невірно!'
            self.displayLabel.color = 'red'
        self.code = ''
        

class CodeLockApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CodeLock(name='codelock'))
        return sm

if __name__ == '__main__':
    CodeLockApp().run()