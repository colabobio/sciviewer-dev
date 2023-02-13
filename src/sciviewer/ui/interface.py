from sciviewer.ui.widget import Widget

class Interface():
    def __init__(self, sketch, scale=1):
        self.scale_factor = scale
        self.sketch = sketch          
        self.focused = None
        self.drawn = []
        self.fonts = {}
        self.widgets = {}
        self.root = Widget(self)

    def add_widget(self, w, parent=None, parent_name=None):
        if parent:
            parent.add_children(w)
        else:
            if parent_name:
                named_parent = self.get_widget(parent_name)
                if named_parent:
                    named_parent.add_children(w)
            else:    
                self.root.add_children(w)
        if w.name:
            self.widgets[w.name] = w

    def get_widget(self, name):
        if name in self.widgets:
            return self.widgets[name]
        else:
            return None    

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
            self.focused.set_rel_mouse_pos()
            self.focused.press()

    def mouse_moved(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.set_rel_mouse_pos()
            self.focused.hover()

    def mouse_dragged(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.set_rel_mouse_pos()
            self.focused.drag()

    def mouse_released(self):
        self.set_focused(self.sketch.mouse_x, self.sketch.mouse_y)
        if self.focused:
            self.focused.set_rel_mouse_pos()
            self.focused.release()

    def set_focused(self, mx, my):
        pfocused = self.focused
        self.focused = None        
        for child in self.drawn[::-1]:
            if child.is_visible and child.is_active and child.has_focus(mx, my):
                if pfocused and pfocused != child: 
                     pfocused.lost_focus()
                self.focused = child
                return
        if pfocused:
            pfocused.lost_focus()            