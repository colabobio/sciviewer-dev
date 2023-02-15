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
    def __init__(self, intf, x=0, y=0, w=0, h=0, name=None, callback=None, yp=0, sw=20, l=16):
        super().__init__(intf, x, y, w, h, name, callback)

        self.swidth = sw
        self.ypos = yp
        self.spos = 0 # Changes where the start button slider is
        self.newspos = self.spos
        self.sposMin = self.ypos

        self.loose = l
        self.locked = False

    def setup(self):
        self.item_height = 30 # This variable determines how big the column will be to display Gene Name
        self.item_sep = 10 # Variable determines space between gene name columns.
        
        self.xpos = self.width - self.swidth
        self.sheight = self.height # scrollbar height
        self.heighttowidth = self.height - self.swidth
        self.ratio = self.height / self.heighttowidth # Lets us know how much/far we can scroll        
        self.sposMax = self.height - self.swidth + 1 # having the plus one lets us get to the end

    def draw(self):
        p = self.intf.sketch

        genePos = self.getPos(p.data.genes)
   
        p.push_matrix()
        p.translate(0, -genePos)
        p.fill(140)

        self.intf.set_font("Helvetica", 14)
        p.text_align(p.CENTER, p.CENTER)
        y = 0
        p.no_stroke()
        for gene in p.data.genes:
            if (y - genePos >= -self.item_height) and (y - genePos < self.height):                
                p.fill(210)
                p.rect(0, y, self.width - self.swidth, self.item_height, 5)

                p.fill(0)
                p.text(gene.name, 0, y, self.width - self.swidth, self.item_height)

            y += self.item_height + self.item_sep

        p.pop_matrix()

        self.update()
                
        p.fill("#B7B7B7")
        p.rect(self.xpos + 5, self.ypos, self.swidth - 5, self.sheight, 5)

        # change color of scrollbar
        if self.locked:
            p.fill(255, 255, 0)
        else:
            p.fill(255, 0, 0)
        p.rect(self.xpos + 5, self.spos, self.swidth - 5, self.swidth, 5) # change size of square in scroll bar

    def reset(self, yp, sw, l):
        self.swidth = sw
        self.sheight = self.height # scrollbar height
        self.heighttowidth = self.height - sw
        self.ratio = self.height / self.heighttowidth; # Lets us know how much/far we can scroll
        self.xpos = self.width - self.swidth
        self.ypos = yp
        self.spos = 0 # Changes where the start button slider is
        self.newspos = self.spos
        self.sposMin = self.ypos
        self.sposMax = self.height - self.swidth + 1; # having the plus one lets us get to the end
        self.loose = l        

    def press(self):
        if self.inside_scroll():
            self.locked = True

    def release(self):
        self.locked = False

    def lost_focus(self):
        self.locked = False

    def inside_scroll(self):
        return self.is_focused and self.mouse_x > self.xpos and self.mouse_x < self.xpos+self.swidth and self.mouse_y > self.ypos and self.mouse_y < self.ypos+self.sheight 

    def update(self):
        p = self.intf.sketch

        if self.locked:            
            self.newspos = p.constrain(self.mouse_y - self.swidth/2, self.sposMin, self.sposMax)

        if abs(self.newspos - self.spos) > 1:
            self.spos = self.spos + (self.newspos-self.spos)/self.loose

    # Get the Position of scrollbar and show genes at that scrolling position
    def getPos(self, genes):
        # Convert spos to be values between

        sizeWindowGenes = 40 * len(genes)

        newScaleScroll = sizeWindowGenes - (self.sposMax - 1) - self.item_height # works good for 500
        newScrollPos = self.spos * (newScaleScroll / (self.sposMax - 1))
    
        if self.spos < 1: # Resets scrollbar back to the top when you scroll all the way back up
            self.spos = 0
            self.reset(0, 20, 16)
            return newScrollPos            
        elif newScrollPos < newScaleScroll:
            return newScrollPos
        else:
            return newScaleScroll