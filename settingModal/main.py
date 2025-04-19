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

    def setSettings(self, settings):
        self.textInput.text = settings['text']
        self.sizeSlider.max = settings['maxSize']
        self.sizeSlider.value = settings['size']
        self.anchorSpinner.text = settings['anchor']
        self.halignSpinner.text = settings['halign']
        self.valignSpinner.text = settings['valign']
        self.wrapOffsetSlider.max = settings['maxWrapOffset']
        self.wrapOffsetSlider.value = settings['wrapOffset']

class SettingWidget(RelativeLayout):
    mainLabel = ObjectProperty(None)
    anchorLayout = ObjectProperty(None)
    anchorSpinner = ObjectProperty(None)

    def getLabelSettings(self):
        settings = {
            'text': self.mainLabel.text,
            'size': self.mainLabel.size,
            'maxSize': min(self.anchorLayout.width, self.anchorLayout.height),
            'anchor': (self.anchorLayout.anchor_x, self.anchorLayout.anchor_y),
            'halign': self.mainLabel.halign,
            'valign': self.mainLabel.valign,
            'wrapOffset': self.mainLabel.wrapOffset,
            'maxWrapOffset': self.mainLabel.width - 10
        }
        print(settings)
        return settings

    def openSettings(self):
        settingModal = SettingModal()
        settingModal.setSettings(self.getLabelSettings())
        settingModal.open()

class SettingModalApp(App):
    def build(self):
        return SettingWidget()

if __name__ == '__main__':
    SettingModalApp().run()