from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty
from math import floor

class MouseCoordLabel(Label):
    def on_kv_post(self, base_widget):
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        x, y = pos
        self.text = f"x: {x} y: {y}"

class DragLabel(DragBehavior, Label):
    app = None
    _keyboard = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        grid = self.app.gridSpacing

        max_x = self.parent.width - self.width
        max_y = self.parent.height - self.height

        if keycode[1] == 'w' and self.y + grid <= max_y:
            self.y += grid
        if keycode[1] == 'd' and self.x + grid <= max_x:
            self.x += grid
        if keycode[1] == 's' and self.y - grid >= 0:
            self.y -= grid
        if keycode[1] == 'a' and self.x - grid >= 0:
            self.x -= grid

        if keycode[1] == 'q' and self.y + grid <= max_y and self.x - grid >= 0:
            self.y += grid
            self.x -= grid
        if keycode[1] == 'e' and self.y + grid <= max_y and self.x + grid <= max_x:
            self.y += grid
            self.x += grid
        if keycode[1] == 'c' and self.x + grid <= max_x and self.y - grid >= 0:
            self.x += grid
            self.y -= grid
        if keycode[1] == 'z' and self.y - grid >= 0 and self.x - grid >= 0:
            self.y -= grid
            self.x -= grid

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            grid = self.app.gridSpacing
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
    app = None
    dragLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
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
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_double_tap:
                grid = self.app.gridSpacing
                snap_x = floor(touch.x / grid) * grid
                snap_y = floor(touch.y / grid) * grid

                max_x = self.width - self.dragLabel.width
                max_y = self.height - self.dragLabel.height

                if snap_x > max_x:
                    snap_x = max_x // grid * grid
                if snap_y > max_y:
                    snap_y = max_y // grid * grid

                snap_x = max(0, snap_x)
                snap_y = max(0, snap_y)

                self.dragLabel.pos = (snap_x, snap_y)
        return super().on_touch_down(touch)

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