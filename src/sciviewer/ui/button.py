from sciviewer.ui.widget import Widget

class Button(Widget):
    def draw(self):
        p = self.intf.sketch
        p.fill(255, 0, 0)
        p.rect(0, 0, self.width, self.height)
