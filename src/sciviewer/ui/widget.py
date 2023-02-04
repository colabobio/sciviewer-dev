class Widget():
    def __init__(self, intf, x=0, y=0, w=0, h=0):
        self.intf = intf

        self.left = x
        self.top = y
        self.width = w
        self.height = h

        self.mouse_x = 0
        self.mouse_y = 0
        self.pmouse_x = 0
        self.pmouse_y = 0

        self.focused = False
        self.parent = None
        self.children = []

        self.setup()

    def set_parent(self, p):
        self.parent = p

    def add_children(self, c):
        self.children += [c]
        c.set_parent(self)

    def update_children(self):
        p = self.intf.sketch
        for child in self.children:
            child.set_mouse(p.mouse_x, p.mouse_y, p.pmouse_x, p.pmouse_y)
            self.focused = self == self.intf.focused
            child.update_children()

    def draw_children(self):
        p = self.intf.sketch
        for child in self.children:
            p.push_matrix()            
            child.set_origin()
            
            p.push_style()
            child.draw()
            p.pop_style()

            self.intf.add_drawn(child)

            child.draw_children()            
            p.pop_matrix()

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

    def set_origin(self):
        self.intf.sketch.translate(self.left, self.top)

    def set_mouse(self, mx, my, pmx, pmy):
        self.mouse_x = mx - self.left
        self.mouse_y = my - self.top
        self.pmouse_x = pmx - self.left
        self.pmouse_y = pmy - self.top

    def has_focus(self, mx, my):
        return self.left <= mx and mx <= self.left + self.width and\
               self.top <= my and my <= self.top + self.height