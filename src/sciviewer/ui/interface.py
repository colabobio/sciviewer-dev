from sciviewer.ui.widget import Widget

class Interface():
    def __init__(self, sketch, scale=1):
        self.scale_factor = scale
        self.sketch = sketch
        self.root = Widget(self)        
        self.focused = None
        self.drawn = []
        self.fonts = {}

    def add_widget(self, w, parent=None):
        if parent:
            parent.add_children(w)
        else:
            self.root.add_children(w)

    def add_font(self, name, size):
        font = self.sketch.create_font(name, self.scale_factor * size)
        self.fonts[name + str(size)] = font

    def set_font(self, name, size):
        key = name + str(size)
        if key in self.fonts:
            font = self.fonts[key]
            self.sketch.text_font(font)

    def update(self):
        self.root.update_children()
        self.drawn = []
        self.root.draw_children()

    def add_drawn(self, w):
        self.drawn += [w]

    def mouse_pressed(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.press()

    def mouse_moved(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.hover()

    def mouse_dragged(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.drag()

    def mouse_released(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.release()

    def set_focused(self, mx, my):
        self.focused = None
        for child in self.drawn[::-1]:
            if child.has_focus(mx, my):
                self.focused = child
                return