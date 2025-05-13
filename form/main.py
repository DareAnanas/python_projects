from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty, \
    NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

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

class ListBox(ScrollView):
    items = ListProperty([])
    on_item_click = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.items.append('Suka')
        self.items.append('Suka')
        self.items.append('Suka')
        self.items.append('Suka')
        self.items.append('Suka')
        self.items.append('Suka')

    def on_items(self, instance, value):
        self.layout.clear_widgets()
        for item in value:
            btn = Button(text=item, size_hint_y=None, height=40)
            btn.bind(on_release=self._on_item_click)
            self.layout.add_widget(btn)

    def _on_item_click(self, button):
        if self.on_item_click:
            self.on_item_click(button.text)

class Search(BoxLayout):
    fieldName = StringProperty('')

class Form(RelativeLayout):
    pass

class FormApp(App):
    def build(self):
        return Form()

if __name__ == '__main__':
    FormApp().run()