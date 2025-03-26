from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

from kivy.config import Config
Config.set('graphics', 'resizable', False)

class SpinBox(BoxLayout):
    index = NumericProperty(0)
    items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items = App.get_running_app().items

    def nextElement(self):
        if (self.index + 1 >= len(self.items)):
            return
        self.index += 1

    def prevElement(self):
        if (self.index <= 0):
            return
        self.index -= 1

class Questionary(RelativeLayout):
    app = None
    textInput = ObjectProperty(None)
    radioButtons = ListProperty([])
    checkBoxes = ListProperty([])
    spinBox = ObjectProperty(None)
    spinner = ObjectProperty(None)
    resultsLabel = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        self.radioButtons = [
            self.ids.radioButton1,
            self.ids.radioButton2,
            self.ids.radioButton3
        ]
        self.checkBoxes = [
            self.ids.checkBox1,
            self.ids.checkBox2,
            self.ids.checkBox3,
        ]

    def getValues(self):
        values = {
            self.app.items[0]: 0,
            self.app.items[1]: 0,
            self.app.items[2]: 0
        }

        inputText = ''
        if (len(self.textInput.text) == 1):
            inputText = self.textInput.text.upper()
        elif (len(self.textInput.text) > 1):
            inputText = self.textInput.text.lower()
            inputText = inputText[0].upper() + inputText[1:]
        if (inputText in values):
            values[inputText] += 1

        for i, radioButton in enumerate(self.radioButtons):
            if (radioButton.active):
                values[self.app.items[i]] += 1
        
        for i, checkBox in enumerate(self.checkBoxes):
            if (checkBox.active):
                values[self.app.items[i]] += 1

        if (self.spinBox.items[self.spinBox.index] in values):
            values[self.spinBox.items[self.spinBox.index]] += 1

        if (self.spinner.text in values):
            values[self.spinner.text] += 1

        self.resultsLabel.text = \
            f"{self.app.items[0]} = {values[self.app.items[0]]}  " + \
            f"{self.app.items[1]} = {values[self.app.items[1]]}  " + \
            f"{self.app.items[2]} = {values[self.app.items[2]]}"

class QuestionaryApp(App):
    items = ['White', 'Gray', 'Black']

    def build(self):
        self.title = 'Опитування'
        questionary = Questionary()
        return questionary

if __name__ == '__main__':
    QuestionaryApp().run()