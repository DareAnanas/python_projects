from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty, \
    NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

class SpinBox(BoxLayout):
    app = None
    index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()

    def nextElement(self):
        if (self.index >= 10):
            return
        self.index += 1

    def prevElement(self):
        if (self.index <= 0):
            return
        self.index -= 1

class ListItem(Button):
    pass

class ListBox(ScrollView):
    layout = ObjectProperty(None)
    items = ListProperty([])
    on_item_click = ObjectProperty(None)
        
    def on_kv_post(self, base_widget):
        self.layout.bind(minimum_height=self.layout.setter('height'))

    def on_items(self, instance, value):
        self.layout.clear_widgets()
        for item in value:
            btn = ListItem(text=item)
            btn.bind(on_release=self._on_item_click)
            self.layout.add_widget(btn)

    def _on_item_click(self, button):
        if self.on_item_click:
            self.on_item_click(button.text)

class Search(BoxLayout):
    textInput = ObjectProperty(None)
    listBox = ObjectProperty(None)
    fieldName = StringProperty('')
    items = ListProperty([])
    focusNextInput = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.textInput.bind(text=self.on_text_change)
        self.textInput.bind(on_text_validate=self.selectFirstHint)
        self.listBox.on_item_click = self.onListItemClick

    def onListItemClick(self, text):
        self.textInput.text = text
        self.listBox.items = []

    def deferFocusInput(self, delta):
        self.textInput.focus = True

    def selectFirstHint(self, instance):
        if (len(self.listBox.items) == 0):
            Clock.schedule_once(self.deferFocusInput, 0)
            return
        self.textInput.text = self.listBox.items[0]
        self.listBox.items = []
        if (self.focusNextInput):
            self.focusNextInput()

    def on_text_change(self, instance, text):
        if (text == ''):
            self.listBox.items = []
            return
        text = text.lower()
        self.listBox.items = list(filter(lambda s: s.lower().startswith(text), self.items))


class Form(RelativeLayout):
    routeSearch = ObjectProperty(None)
    surnameSearch = ObjectProperty(None)
    spinBox = ObjectProperty(None)
    statusLabel = ObjectProperty(None)

    def clearEntries(self):
        self.routeSearch.textInput.text = ''
        self.surnameSearch.textInput.text = ''
        self.spinBox.index = 0
        self.statusLabel.text = ''

    def on_kv_post(self, base_widget):
        self.routeSearch.focusNextInput = self.focusInput

    def deferFocusInput(self, delta):
        self.surnameSearch.textInput.focus = True

    def focusInput(self):
        Clock.schedule_once(self.deferFocusInput, 0)

    def setStatusLabelColorForTime(self, color, time):
        self.statusLabel.color = color
        Clock.schedule_once(self.revertStatusLabelColor, time)

    def revertStatusLabelColor(self, dt):
        self.statusLabel.color = 'white'

    def validate(self):
        route = self.routeSearch.textInput.text.strip().lower()
        surname = self.surnameSearch.textInput.text.strip().lower()
        numberOfPassengers = self.spinBox.index
        if (route == ''):
            self.statusLabel.text = 'Напрям не може бути пустим'
            self.setStatusLabelColorForTime('red', 0.5)
            return
        if (not self.isCorrectRoute(route)):
            self.statusLabel.text = 'Напрям може містити тільки українські символи, пробіл та тире'
            self.setStatusLabelColorForTime('red', 0.5)
            return
        if (not self.isCorrectSurname(surname)):
            self.statusLabel.text = 'Прізвище може містити тільки українські символи'
            self.setStatusLabelColorForTime('red', 0.5)
            return
        if (not self.isCorrectLength(surname)):
            self.statusLabel.text = 'Прізвище не може бути довшим за 20 символів'
            self.setStatusLabelColorForTime('red', 0.5)
            return

        self.statusLabel.text = 'Форма надіслана'
        self.setStatusLabelColorForTime('green', 0.5)
        
    def isCorrectRoute(self, route):
        correctSymbols = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя- ")

        for char in route:
            if (char not in correctSymbols):
                return False

        return True

    def isCorrectSurname(self, surname):
        if (surname == ''):
            return True

        correctSymbols = set("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")

        for char in surname:
            if (char not in correctSymbols):
                return False

        return True

    def isCorrectLength(self, surname):
        if (surname == ''):
            return True
        
        if len(surname) > 20:
            return False

        return True

class FormApp(App):
    form = ObjectProperty(None)

    routes = [
        'Вінниця - Умань',
        'Умань - Вінниця',
        'Вінниця - Полтава',
        'Полтава - Вінниця',
        'Вінниця - Тернопіль',
        'Тернопіль - Вінниця',
        'Вінниця - Львів',
        'Львів - Вінниця',
        'Вінниця - Київ',
        'Київ - Вінниця',
        'Умань - Полтава',
        'Полтава - Умань',
        'Умань - Тернопіль',
        'Тернопіль - Умань',
        'Умань - Львів',
        'Львів - Умань',
        'Умань - Київ',
        'Київ - Умань',
        'Полтава - Тернопіль',
        'Тернопіль - Полтава',
        'Полтава - Львів',
        'Львів - Полтава',
        'Полтава - Київ',
        'Київ - Полтава',
        'Тернопіль - Львів',
        'Львів - Тернопіль',
        'Тернопіль - Київ',
        'Київ - Тернопіль',
        'Львів - Київ',
        'Київ - Львів'
    ]

    surnames = [
        'Дворницький',
        'Підлісний',
        'Фещак',
        'Качин',
        'Ярко',
        'Тиндик',
        'Огородник',
        'Шевченко',
        'Бондаренко',
        'Ковальчук',
        'Мельник',
        'Ткаченко',
        'Романюк',
        'Олійник',
        'Павленко',
        'Сорока',
        'Довженко'
    ]

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 27:
            self.form.clearEntries()
            return True
        return False

    def build(self):
        Window.bind(on_key_down=self.on_key_down)
        self.form = Form()
        return self.form

if __name__ == '__main__':
    FormApp().run()