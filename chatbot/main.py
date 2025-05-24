from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import ListProperty, ObjectProperty

class ListItem(Label):
    pass

class ListBox(ScrollView):
    layout = ObjectProperty(None)
    items = ListProperty([])

    def on_kv_post(self, base_widget):
        self.layout.bind(minimum_height=self.layout.setter('height'))

    def on_items(self, instance, value):
        self.layout.clear_widgets()
        for item in value:
            label = ListItem(text=item)
            self.layout.add_widget(label)

class ChatBot(RelativeLayout):
    items = [
        'Bebra',
        'BebraBebra',
        'BebraBebraBebra',
        'BebraBebraBebraBebra',
        'BebraBebraBebraBebraBebra',
        'BebraBebraBebraBebraBebraBebra'
    ]

    listBox = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.listBox.items = self.items

class ChatBotApp(App):
    def build(self):
        return ChatBot()

if __name__ == '__main__':
    ChatBotApp().run()