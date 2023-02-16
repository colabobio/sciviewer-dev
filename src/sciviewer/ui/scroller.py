from sciviewer.ui.widget import Widget

class SpaceFiller(Widget):
    def __init__(self, intf, x=0, y=0, w=0, h=0, name=None, callback=None, color="#FFFFFF"):
        super().__init__(intf, x, y, w, h, name, callback)
        self.color = color

    def draw(self):
        p = self.intf.sketch
        p.no_stroke()
        p.fill(self.color)
        p.rect(0, 0, self.width, self.height)

class GeneScroller(Widget):
    def __init__(self, intf, x=0, y=0, w=0, h=0, name=None, callback=None, iheght=30, isep=10, sw=20, l=16):
        super().__init__(intf, x, y, w, h, name, callback)

        self.item_height = iheght * self.intf.scale_factor # This variable determines how big the column will be to display Gene Name
        self.item_sep = isep * self.intf.scale_factor # Variable determines space between gene name columns.
        self.swidth = sw * self.intf.scale_factor
        self.loose = l * self.intf.scale_factor

    def setup(self):
        self.locked = False
        self.selected = -1
        self.reset()

    def draw(self):
        p = self.intf.sketch

        dy = self.get_translation(p.data.genes)
   
        p.push_matrix()
        p.translate(0, -dy)
        p.fill(140)
        self.intf.set_font("Helvetica", 14)
        p.text_align(p.CENTER, p.CENTER)
        y = 0
        p.no_stroke()
        for gene in p.data.genes:
            if (y - dy >= -self.item_height) and (y - dy < self.height):
                p.fill(210)
                p.rect(0, y, self.width - self.swidth, self.item_height, 5)
                p.fill(0)
                p.text(gene.name, 0, y, self.width - self.swidth, self.item_height)
            y += self.item_height + self.item_sep
        p.pop_matrix()

        self.update_position()
        self.draw_scroll()

    def press(self):
        if self.inside_scroll():
            self.locked = True

    def release(self):
        self.locked = False

    def lost_focus(self):
        self.locked = False

    def inside_scroll(self):
        return self.is_focused and self.mouse_x > self.xpos and self.mouse_x < self.xpos+self.swidth and \
                                   self.mouse_y > self.ypos and self.mouse_y < self.ypos+self.sheight 

    def draw_scroll(self):
        p = self.intf.sketch

        p.fill(210)
        p.rect(self.xpos + 5, self.ypos, self.swidth - 5, self.sheight, 5)

        # change color of scrollbar
        if self.locked:
            p.fill("#D13737")
        else:
            p.fill("#B7B7B7")
        p.rect(self.xpos + 5, self.spos, self.swidth - 5, self.swidth, 5) # change size of square in scroll bar

    def reset(self):        
        self.xpos = self.width - self.swidth
        self.ypos = 0
        self.spos = 0 # Changes where the start button slider is
        self.new_spos = 0

        self.sheight = self.height # scrollbar height
        self.spos_min = 0
        self.spos_max = self.height - self.swidth + 1; # having the plus one lets us get to the end

    def update_position(self):
        p = self.intf.sketch

        if self.locked:            
            self.new_spos = p.constrain(self.mouse_y - self.swidth / 2, self.spos_min, self.spos_max)

        if abs(self.new_spos - self.spos) > 1:
            self.spos = self.spos + (self.new_spos - self.spos) / self.loose

    # Get the trasnlation of scrollbar to show genes at that scrolling position
    def get_translation(self, genes):
        size_window_genes = (self.item_height + self.item_sep) * len(genes)

        new_scale_scroll = size_window_genes - (self.spos_max - 1) - self.item_height
        new_scroll_pos = self.spos * (new_scale_scroll / (self.spos_max - 1))
    
        if self.spos < 1: # Resets scrollbar back to the top when you scroll all the way back up
            self.reset()
            return new_scroll_pos            
        elif new_scroll_pos < new_scale_scroll:
            return new_scroll_pos
        else:
            return new_scale_scroll