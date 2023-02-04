from sciviewer.ui.widget import Widget

class Button(Widget):
    def setup(self):
        self.fill_color = "#B7B7B7"

    def draw(self):
        p = self.intf.sketch
        p.fill(self.fill_color)
        p.rect(0, 0, self.width, self.height)
    
    def hover(self):
        self.fill_color = "#D13737"

    def release(self):
        print("Clicked")