from sciviewer.ui.widget import Widget

class Button(Widget):
    def __init__(self, intf, x, y, w, h, name, callback, label):
        super().__init__(intf, x, y, w, h, name, callback)
        self.label = label

    def draw(self):
        p = self.intf.sketch
        p.no_stroke()
        p.fill(self.color())
        p.rect(0, 0, self.width, self.height, 5)
        self.intf.set_font("Helvetica", 14)
        p.fill(0)
        p.text_align(p.CENTER, p.CENTER)
        p.text(self.label, 0, 0, self.width, self.height)
    
    def color(self):
        if self.is_focused:
            if self.intf.sketch.is_mouse_pressed:
                return "#D13737"
            else:
                return "#D89B9B"
        else:
            return "#B7B7B7"

    def release(self):
        if self.callback: self.callback()

class SwitchButton(Widget):
    def __init__(self, intf, x, y, w, h, name, callback, label):
        super().__init__(intf, x, y, w, h, name, callback)
        self.label = label

    def setup(self):
        self.switched_on = False

    def draw(self):
        p = self.intf.sketch
        p.no_stroke()
        p.fill(self.color())
        p.rect(0, 0, self.width, self.height, 5)
        self.intf.set_font("Helvetica", 14)
        p.fill(0)
        p.text_align(p.CENTER, p.CENTER)
        p.text(self.label, 0, 0, self.width, self.height)
    
    def color(self):
        if self.switched_on:
            return "#D13737"
        else:
            if self.is_focused:
                return "#D89B9B"
            else:
                return "#B7B7B7"

    def switch_off(self):
        self.switched_on = False

    def switch_on(self):
        self.switched_on = True

    def release(self):
        self.switch_on()
        if self.callback: self.callback()