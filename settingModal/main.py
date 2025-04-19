from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label

class WrapLabel(Label):
    wrapOffset = NumericProperty(0)

class SettingModal(ModalView):
    textInput = ObjectProperty(None)
    sizeSlider = ObjectProperty(None)
    anchorSpinner = ObjectProperty(None)
    halignSpinner = ObjectProperty(None)
    valignSpinner = ObjectProperty(None)
    wrapOffsetSlider = ObjectProperty(None)

    mainLabel = ObjectProperty(None)
    anchorLayout = ObjectProperty(None)

    def __init__(self, mainLable, anchorLayout, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.mainLabel = mainLable
        self.anchorLayout = anchorLayout

    def setDefaultSettings(self):
        self.setSettings(self.app.defaultSettings)

    def setSettings(self, settings):
        self.textInput.text = settings['text']
        self.sizeSlider.max = settings['maxSize']
        self.sizeSlider.value = settings['size']
        self.anchorSpinner.text = settings['anchor']
        self.halignSpinner.text = settings['halign']
        self.valignSpinner.text = settings['valign']
        self.wrapOffsetSlider.max = settings['maxWrapOffset']
        self.wrapOffsetSlider.value = settings['wrapOffset']

    def applySettings(self):
        self.mainLabel.text = self.textInput.text
        self.mainLabel.size = (self.sizeSlider.value, self.sizeSlider.value)
        anchor_y, anchor_x = self.anchorSpinner.text.split(' ')
        self.anchorLayout.anchor_x = anchor_x.lower()
        self.anchorLayout.anchor_y = anchor_y.lower()
        self.mainLabel.halign = self.halignSpinner.text.lower()
        self.mainLabel.valign = self.valignSpinner.text.lower()
        self.mainLabel.wrapOffset = self.wrapOffsetSlider.value
        self.dismiss()

class SettingWidget(RelativeLayout):
    mainLabel = ObjectProperty(None)
    anchorLayout = ObjectProperty(None)

    def getLabelSettings(self):
        settings = {
            'text': self.mainLabel.text,
            'size': self.mainLabel.width,
            'maxSize': min(self.anchorLayout.width, self.anchorLayout.height),
            'anchor': str(self.anchorLayout.anchor_y).capitalize() 
            + ' ' + str(self.anchorLayout.anchor_x).capitalize(),
            'halign': str(self.mainLabel.halign).capitalize(),
            'valign': str(self.mainLabel.valign).capitalize(),
            'wrapOffset': self.mainLabel.wrapOffset,
            'maxWrapOffset': self.mainLabel.width - 10
        }
        print(settings)
        return settings

    def openSettings(self):
        settingModal = SettingModal(self.mainLabel, self.anchorLayout)
        settingModal.setSettings(self.getLabelSettings())
        settingModal.open()

class SettingModalApp(App):

    defaultSettings = {
        'text': 'Get in tune with the car in my hood',
        'size': 150,
        'maxSize': 195,
        'anchor': 'Center Center',
        'halign': 'Left',
        'valign': 'Top',
        'wrapOffset': 10,
        'maxWrapOffset': 140
    }

    def build(self):
        return SettingWidget()

if __name__ == '__main__':
    SettingModalApp().run()