from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, ColorProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle, Triangle, Ellipse
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.textinput import TextInput
from kivy.core.text import Label as CoreLabel
import math

class SpinBox(BoxLayout):
    value = NumericProperty(0)
    minValue = NumericProperty(0)
    maxValue = NumericProperty(500)
    textInput = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.textInput.bind(focus=self.on_focus)
        self.bind(maxValue=self.on_maxValue)

    def on_maxValue(self, instance, value):
        if (self.value >= value):
            self.value = self.maxValue
            return

    def on_focus(self, instance, value):
        if not value:
            inputValue = int(self.textInput.text)
            if (inputValue <= self.minValue):
                self.value = self.minValue
                return
            if (inputValue >= self.maxValue):
                self.value = self.maxValue
                return
            self.value = inputValue
            

    def nextElement(self):
        if (self.value >= self.maxValue):
            return
        self.value += 1

    def prevElement(self):
        if (self.value <= self.minValue):
            return
        self.value -= 1

class ColorButton(Button):
    
    def showColorPicker(self):
        modal = ModalView(size_hint=(0.5,0.5))
        colorPicker = ColorPicker()
        colorPicker.bind(color=self.on_color)
        modal.add_widget(colorPicker)
        modal.open()

    def on_color(self, instance, value):
        self.background_color = value

class SideBar(BoxLayout):
    
    objectTypeSpinner = ObjectProperty(None)
    x1 = ObjectProperty(None)
    y1 = ObjectProperty(None)
    x2 = ObjectProperty(None)
    y2 = ObjectProperty(None)
    colorButton = ObjectProperty(None)
    arrowSpinner = ObjectProperty(None)
    arrowShapeSpinner = ObjectProperty(None)
    labelTextInput = ObjectProperty(None)

    def defocusInputs(self):
        for child in self.walk():
            if isinstance(child, TextInput):
                child.focus = False

    def readShapeSettings(self):
        self.defocusInputs()
        return {
            'shape': self.objectTypeSpinner.text,
            'point1': [self.x1.value, self.y1.value],
            'point2': [self.x2.value, self.y2.value],
            'color': self.colorButton.background_color,
            'arrow': self.arrowSpinner.text,
            'arrowshape': self.arrowShapeSpinner.text,
            'text': self.labelTextInput.text
        }



class PaintCanvas(Widget):
    sideBar = ObjectProperty(None)
    xSpinboxes = []
    ySpinboxes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_spinboxes)

    def leanWithIt(self, point):
        return [point[0] + self.pos[0], point[1] + self.pos[1]]

    def on_kv_post(self, base_widget):
        for element in reversed(self.sideBar.children):
            if ('group' in element.properties()):
                if (element.group == 'x'):
                    self.xSpinboxes.append(element)
                if (element.group == 'y'):
                    self.ySpinboxes.append(element)

    def update_spinboxes(self, *args):
        print(self.width, self.height)
        for xSpinbox in self.xSpinboxes:
            xSpinbox.maxValue = int(self.width)
        for ySpinbox in self.ySpinboxes:
            ySpinbox.maxValue = int(self.height)

    def draw(self):
        shapeSettings = self.sideBar.readShapeSettings()
        self.drawShape(**shapeSettings)

    def drawArrowHead(self, point1, point2, color, arrowshape='Forward', length=15):
        x1, y1 = point1
        x2, y2 = point2
        
        angle = math.atan2(y2 - y1, x2 - x1)
    
        if arrowshape == 'Backward':
            angle += math.pi  # розвертає стрілку

        left = (x2 - length * math.cos(angle - math.pi / 6),
                y2 - length * math.sin(angle - math.pi / 6))
        right = (x2 - length * math.cos(angle + math.pi / 6),
                y2 - length * math.sin(angle + math.pi / 6))

        with self.canvas:
            Color(*color)
            Triangle(points=[x2, y2, *left, *right])

    

    def drawShape(self, shape, point1, point2, color, arrow='None', arrowshape='Forward', text='Get In Tune With It'):
        point1 = self.leanWithIt(point1)
        point2 = self.leanWithIt(point2)
        x1, y1 = point1
        x2, y2 = point2
        w, h = abs(x2 - x1), abs(y2 - y1)
        pos = (min(x1, x2), min(y1, y2))
        size = (w, h)
        with self.canvas:
            Color(*color)
            if (shape == 'Line'):
                Line(points=[x1, y1, x2, y2], width=2)

                if (arrow in ('Start', 'Both')):
                    self.drawArrowHead(point2, point1, color, arrowshape)
                if arrow in ('End', 'Both'):
                    self.drawArrowHead(point1, point2, color, arrowshape)
            elif shape == 'Rectangle':
                Rectangle(pos=pos, size=size)

            elif shape == 'Ellipse':
                Ellipse(pos=pos, size=size)

            elif shape == 'Arc':
                Line(ellipse=(pos[0], pos[1], w, h, -90, 90), width=2)

            elif shape == 'Label' and text:
                label = CoreLabel(text=text, font_size=20)
                label.refresh()
                texture = label.texture
                Rectangle(texture=texture, pos=pos, size=texture.size)

    def clearCanvas(self):
        self.canvas.clear()

class Paint(RelativeLayout):
    paintCanvas = ObjectProperty(None)

    def draw(self):
        self.paintCanvas.draw()

    def clear(self):
        self.paintCanvas.clearCanvas()

class PaintApp(App):
    def build(self):
        return Paint()

if __name__ == '__main__':
    PaintApp().run()