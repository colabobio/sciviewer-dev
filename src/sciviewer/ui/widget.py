class Widget():
    def __init__(self, intf, x=0, y=0, w=0, h=0, name=None, callback=None):
        self.intf = intf

        self.rel_x = intf.scale_factor * x
        self.rel_y = intf.scale_factor * y

        self.abs_x = intf.scale_factor * x
        self.abs_y = intf.scale_factor * y

        self.width = intf.scale_factor * w
        self.height = intf.scale_factor * h

        self.mouse_x = 0
        self.mouse_y = 0
        self.pmouse_x = 0
        self.pmouse_y = 0

        self.is_focused = False
        self.parent = None
        self.children = []

        self.is_active = True
        self.is_visible = True

        self.name = name
        self.callback = callback

    def set_parent(self, p):
        self.parent = p
        self.abs_x = p.abs_x + self.rel_x
        self.abs_y = p.abs_y + self.rel_y

    def set_callback(self, callback):
        self.callback = callback    

    def add_children(self, c):
        self.children += [c]
        c.set_parent(self)

    def update_children(self):        
        for child in self.children:
            child.set_rel_mouse_pos()
            child.set_focused_state()
            child.update_children()

    def draw_children(self):
        p = self.intf.sketch
        for child in self.children:
            if not child.is_visible: continue

            p.push_matrix()
            child.set_origin()
            
            p.push_style()
            child.draw()
            p.pop_style()

            self.intf.add_drawn(child)

            child.draw_children()
            p.pop_matrix()

    def set_origin(self):
        self.intf.sketch.translate(self.rel_x, self.rel_y)

    def set_rel_mouse_pos(self):
        p = self.intf.sketch
        self.mouse_x = p.mouse_x - self.abs_x
        self.mouse_y = p.mouse_y - self.abs_y
        self.pmouse_x = p.pmouse_x - self.abs_x
        self.pmouse_y = p.pmouse_y - self.abs_y

    def set_focused_state(self):
        self.is_focused = self == self.intf.focused

    def has_focus(self, mx, my):
        return self.abs_x <= mx and mx <= self.abs_x + self.width and \
               self.abs_y <= my and my <= self.abs_y + self.height

    def show(self):
        self.is_visible = True
        self.set_visible()

    def hide(self):
        self.is_visible = False
        self.set_invisible()

    def activate(self):
        self.is_active = True
        self.set_active()

    def deactivate(self):
        self.is_active = False
        self.set_inactive()

    def setup(self):
        pass

    def draw(self):
        pass

    def press(self):
        pass

    def hover(self):
        pass

    def drag(self):
        pass

    def release(self):
        pass

    def lost_focus(self):
        pass

    def set_active(self):
        pass

    def set_inactive(self):
        pass

    def set_visible(self):
        pass
    
    def set_invisible(self):
        pass
