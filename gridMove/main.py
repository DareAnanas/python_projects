from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line

class MouseCoordLabel(Label):
    def on_kv_post(self, base_widget):
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        x, y = pos
        self.text = f"x: {x} y: {y}"

class DragLabel(DragBehavior, Label):
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            grid = App.get_running_app().gridSpacing
            snap_x = round(self.x / grid) * grid
            snap_y = round(self.y / grid) * grid

            max_x = self.parent.width - self.width
            max_y = self.parent.height - self.height

            if snap_x > max_x:
                snap_x = max_x // grid * grid
            if snap_y > max_y:
                snap_y = max_y // grid * grid

            snap_x = max(0, snap_x)
            snap_y = max(0, snap_y)

            self.pos = (snap_x, snap_y)
        return super().on_touch_up(touch)

class Grid(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_grid, pos=self.update_grid)
        self.update_grid()

    def update_grid(self, *args):
        self.canvas.before.clear()

        grid_spacing = App.get_running_app().gridSpacing

        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)

            x = 0
            while x <= self.width:
                Line(points=[x, 0, x, self.height], width=1)
                x += grid_spacing

            y = 0
            while y <= self.height:
                Line(points=[0, y, self.width, y], width=1)
                y += grid_spacing

class GridMove(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        Window.bind(size=self.update_size)
        
    def update_size(self, window, size):
        self.size = size

class GridMoveApp(App):
    gridSpacing = 50
    dragLabelOffset = 10

    def build(self):
        return GridMove()

if __name__ == '__main__':
    GridMoveApp().run()