from datetime import datetime
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty, ObjectProperty, StringProperty, \
    DictProperty, ColorProperty
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.uix.spinner import SpinnerOption
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

LabelBase.register(
    name="seguiemj",
    fn_regular="/home/danylo/Documents/python_projects/chatbot/seguiemj.ttf"
)

class ColorConverter:
    def hexToRgba(hex_color, alpha=1):
        # Convert a hex color string to an RGBA tuple (0-1 range).
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return [round(r / 255.0, 4), round(g / 255.0, 4), round(b / 255.0, 4), alpha]

class ThemeManager:
    light_theme = {
        'bot_message_color': ColorConverter.hexToRgba('#aad5e3'),
        'user_message_color': ColorConverter.hexToRgba('#8fee8f'),
        'hex_text_color': '000000',
        'bg_color': ColorConverter.hexToRgba('#ffffff'),
        'text_color': ColorConverter.hexToRgba('#000000'),
        'button_color': [0.7, 0.7, 0.7, 1],
        'button_normal': ''
    }
    dark_theme = {
        'bot_message_color': ColorConverter.hexToRgba('#3b4a4f'),
        'user_message_color': ColorConverter.hexToRgba('#2a462a'),
        'hex_text_color': 'ffffff',
        'bg_color': ColorConverter.hexToRgba('#000000'),
        'text_color': ColorConverter.hexToRgba('#ffffff'),
        'button_color': [1, 1, 1, 1],
        'button_normal': 'atlas://data/images/defaulttheme/button'
    }

class EmojiOption(SpinnerOption):
    font_name = StringProperty('seguiemj')
    color = ColorProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.color = self.app.theme['text_color']
        self.app.bind(theme=self.updateTheme)

    def updateTheme(self, instance, value):
        self.color = value['text_color']

        

class EmojiSpinner(Spinner):
    option_cls = ObjectProperty(EmojiOption)
    textInput = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(on_release=self.on_spinner_open)

    def on_spinner_open(self, spinner):
        dropdown = spinner._dropdown
        for btn in dropdown.container.children:
            btn.bind(on_release=self.on_spinner_select)

    def on_spinner_select(self, button):
        text = button.text
        self.text = text
        if (self.textInput):
            self.textInput.text = self.textInput.text + self.text

class HighlightLabel(Label):
    text_to_display = StringProperty("")
    highlight_range = ListProperty([0, 0])  # (start_idx, end_idx)
    background_color = ListProperty([0, 0, 0, 1])
    highlight_text_color = ListProperty([1, 1, 0, 1])
    highlight_background_color = ListProperty([0, 0, 0, 1])
    colorName = ''
    text_color = StringProperty('')

    def __init__(self, text, colorName, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.text_color = self.app.theme['hex_text_color']
        self.text_to_display = text
        self.colorName = colorName
        self.background_color = self.app.theme[self.colorName]
        self.app.bind(theme=self.updateTheme)

    def updateTheme(self, instance, value):
        self.text_color = value['hex_text_color']
        self.background_color = value[self.colorName]

    def on_text_color(self, *args):
        self.update_markup()

    def on_text_to_display(self, *args):
        self.update_markup()

    def on_highlight_range(self, *args):
        self.update_markup()

    def update_markup(self):
        text = self.text_to_display
        start, end = self.highlight_range
        start = max(0, min(len(text), start))
        end = max(start, min(len(text), end))

        before = text[:start]
        highlight = text[start:end]
        after = text[end:]

        self.markup = True
        self.text = (
            f"[color={self.text_color}]{before}[/color]"
            f"[color=ffff00]{highlight}[/color]"
            f"[color={self.text_color}]{after}[/color]"
        )

class ListItem(HighlightLabel):
    pass

class ListBox(ScrollView):
    layout = ObjectProperty(None)
    items = ListProperty([])

    def on_kv_post(self, base_widget):
        self.layout.bind(minimum_height=self.layout.setter('height'))

    def addMessage(self, text, bg_color):
        label = ListItem(text, bg_color)
        self.layout.add_widget(label)

class ChatBot(RelativeLayout):
    message_id = 0
    messages = [
        "Як проходить твій день?",
        "Чи маєш якісь звички або ритуали, які допомагають тобі бути продуктивним(-ою)?",
        "Чи є щось нове, що ти нещодавно спробував(-ла) і тобі сподобалося?",
        "Яку нову навичку ти хотів(-ла) б опанувати найближчим часом?",
        "Що тебе найбільше мотивує розвиватися?",
        "Яку останню книгу або статтю ти прочитав(-ла) для саморозвитку?",
        "Як ти зазвичай вчишся — через книги, відео, практику чи інше?",
        "Чи користуєшся ти якимись додатками або інструментами для організації навчання?",
        "Як ти борешся з прокрастинацією?",
        "Що для тебе означає 'ефективне навчання'?",
        "Який був твій найскладніший досвід навчання, і як ти його подолав(-ла)?",
        "Чи маєш менторів або людей, які тебе надихають у розвитку?",
        "Як ти оцінюєш свій прогрес у саморозвитку?",
        "Чи ведеш ти щоденник або записи своїх думок і цілей?",
        "Які онлайн-курси або ресурси ти б порадив(-ла) іншим?",
        "Чи плануєш свій час для навчання? Якщо так, то як?",
        "Як змінилися твої підходи до самонавчання за останній рік?",
        "Чи маєш довгострокову мету в навчанні? Яку?",
        "Як ти відновлюєш сили після інтенсивного навчання?",
        "Чи був у тебе момент, коли ти хотів(-ла) здатися, але не зробив(-ла) цього? Що допомогло продовжити?",
    ]

    answers = [
        'Все чудово!', 
        'Зайнятися йогою.', 
        'Ні, немає. Думаю, це треба виправити.',
        'Хочу пограти ДнД на природі!',
        'Можливість допомогти іншим людям.',
        '"Чому ми ускладнюємо життя?"',
        'Я зазвичай вчуся через практику.',
        'Ні, не користуюсь.',
        'Ставлю собі дедлайни.',
        'Це коли мені подобається те, що я вчу.',
        'Мій найскладніший досвід навчання був коли я вчив схемотехніку. І я подолав його тим, що отримав підтримку від друзів😀',
        'Менторів не маю, але маю друзів і знайомих, які надихають у розвитку.',
        'Я забагато часу витрачаю на планування там де не треба, а там де треба, то замало😢',
        'Веду. Там я записую свої ідеї та цілі.',
        'Курси Prometheus.',
        'Ні, не планую☹. Можливо це помилка.️',
        'Краще зробити гірше, ніж взагалі не зробити.',
        "Ні, мети на 5 років немає через навчання в університеті. Але думаю це щось пов'язане з розробкою додатків на Android.",
        'Пробую багато різних типів відпочинку. Полежати на ліжку, побігати у лісі, пограти у відеоігри, пограти у настільні ігри з друзями та піти на прогулянку.'
        'Мені допомогло те, за для кого я це роблю.'
    ]

    items = [
        'Bebra',
        'BebraBebra',
        'BebraBebraBebra',
        'BebraBebraBebraBebra',
        'BebraBebraBebraBebraBebra',
        'BebraBebraBebraBebraBebra\nBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebraBebra'
    ]

    listBox = ObjectProperty(None)
    messageInput = ObjectProperty(None)
    findInput = ObjectProperty(None)
    matchCaseCheckBox = ObjectProperty(None)

    def addTimeStamp(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        return timestamp + ' ' + text

    def addUserMark(self, username, text):
        return username + ' ' + text

    def on_kv_post(self, base_widget):
        self.app = App.get_running_app()
        self.getReply()

    def getReply(self):
        message = self.messages[self.message_id]
        message = self.addUserMark('Bot:', message)
        message = self.addTimeStamp(message)
        self.listBox.addMessage(message, 'bot_message_color')

    def sendMessage(self):
        message = self.messageInput.text.strip()
        if (message == ''):
            return
        self.messageInput.text = ''
        message = self.addUserMark('You:', message)
        message = self.addTimeStamp(message)
        self.listBox.addMessage(message, 'user_message_color')
        if (self.message_id >= len(self.messages) - 1):
            return
        self.message_id += 1
        Clock.schedule_once(lambda dt: self.getReply(), 0.5)

    def clearHighLights(self):
        for label in self.listBox.layout.children:
            label.highlight_range = [0, 0]

    def findAll(self):
        if (self.matchCaseCheckBox.active):
            text = self.findInput.text.strip()
            for label in self.listBox.layout.children:
                index = label.text_to_display.find(text)
                if (index == -1):
                    label.highlight_range = [0, 0]
                    continue
                label.highlight_range = [index, index + len(text)]
        else:
            text = self.findInput.text.strip().lower()
            for label in self.listBox.layout.children:
                index = label.text_to_display.lower().find(text)
                if (index == -1):
                    label.highlight_range = [0, 0]
                    continue
                label.highlight_range = [index, index + len(text)]

class ChatBotApp(App):
    theme = DictProperty(ThemeManager.dark_theme)

    def changeTheme(self):
        if (self.theme == ThemeManager.light_theme):
            self.theme = ThemeManager.dark_theme
        elif (self.theme == ThemeManager.dark_theme):
            self.theme = ThemeManager.light_theme

    def build(self):
        Window.bind(on_key_down=self._on_key_down)
        self.chatbot = ChatBot()
        return self.chatbot

    def _on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 13:
            self.chatbot.sendMessage()
        if key == 27:
            self.chatbot.clearHighLights()
            return True
        return False

if __name__ == '__main__':
    ChatBotApp().run()