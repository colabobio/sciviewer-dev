from sciviewer.ui.widget import Widget

class DifferentialSelector(Widget):
    def setup(self):
        self.is_active = False
        self.selection = []
        self.tolerance = 10 * self.intf.scale_factor

    def draw(self):
        if not self.is_active: return

        p = self.intf.sketch
        p.stroke(230, 20, 20)

        if 0 < len(self.selection):
            p.fill(230, 20, 20, 100)        
            if 1 < len(self.selection):
                p.begin_shape()
                for mpos in self.selection:
                    p.vertex(mpos[0], mpos[1])
                p.vertex(self.mouse_x, self.mouse_y)
                p.end_shape()
            else:
                mpos0 = self.selection[0]
                p.line(mpos0[0], mpos0[1], self.mouse_x, self.mouse_y)

        p.no_fill()
        p.ellipse(self.mouse_x, self.mouse_y, self.tolerance, self.tolerance)

    def release(self):
        if not self.is_active: return

        p = self.intf.sketch
        if p.mouse_button == p.LEFT:
            if 0 < len(self.selection):
                mouse0 = self.selection[0]
                if p.dist(mouse0[0], mouse0[1], self.mouse_x, self.mouse_y) < self.tolerance:
                    if self.callback: self.callback(self.selection)
                    self.selection = []
                    return
                pmouse = self.selection[-1]
                if self.tolerance < p.dist(pmouse[0], pmouse[1], self.mouse_x, self.mouse_y):
                    self.selection += [(self.mouse_x, self.mouse_y)]
            else:
                self.selection = [(self.mouse_x, self.mouse_y)]
        else:     
            self.selection = []

    def lost_focus(self):
        print("Selector lost focus...")
        self.selection = []

    def activate(self):
        self.is_active = True
        self.selection = []

    def deactivate(self):
        self.is_active = False
        self.selection = []