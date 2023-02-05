from sciviewer.ui.widget import Widget

class Button(Widget):
    def draw(self):
        p = self.intf.sketch
        p.fill(self.color())
        p.rect(0, 0, self.width, self.height, 5)
        self.intf.set_font("Helvetica", 14)
        p.fill(0)
        p.text_align(p.CENTER, p.CENTER)
        p.text("Click me", 0, 0, self.width, self.height)
    
    def color(self):
        if self.is_focused:
            if self.intf.sketch.is_mouse_pressed:
                return "#D13737"
            else:
                return "#D89B9B"
        else:
            return "#B7B7B7"

    def release(self):
        print("Clicked", self.is_focused)