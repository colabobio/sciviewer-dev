from sciviewer.ui.widget import Widget

class GeneScroller(Widget):
    def setup(self):
        self.item_height = 30 # This variable determines how big the column will be to display Gene Name
        self.item_sep = 10 # Variable determines space between gene name columns.
        self.genesAr = []
        self.noMatchFound = False


        self.vs = VScrollBar(self, self.width, 0, 20, self.height, 16)

    def draw(self):
        p = self.intf.sketch

        genePos = self.vs.getPos()

   
        p.push_matrix()
        p.translate(0, -genePos)
        p.fill(140)

        self.intf.set_font("Helvetica", 14)
        p.text_align(p.CENTER, p.CENTER)
        y = 50
        for gene in p.data.genes:
            p.fill(200, 100, 100)
            p.rect(0, y, self.width, self.item_height)

            p.fill(100, 200, 200)
            p.text(gene.name, 0, y, self.width, self.item_height)

            y += self.item_height + self.item_sep
  
        p.pop_matrix()

        self.vs.update()
        self.vs.display()


    def press(self):
        self.vs.locked = True
        print("locked")

    def release(self):
        self.vs.locked = False

    def lost_focus(self):
        self.vs.locked = False

class VScrollBar:
    def __init__(self, wt, xp, yp, sw, sh, l):
        self.widget = wt
        self.swidth = sw
        self.sheight = sh # scrollbar height
        self.heighttowidth = sh - sw
        self.ratio = sh / self.heighttowidth; # Lets us know how much/far we can scroll
        self.xpos = xp - self.swidth / 2
        self.ypos = yp
        self.spos = 0 # Changes where the start button slider is
        self.newspos = self.spos
        self.sposMin = self.ypos
        self.sposMax = self.widget.height - self.swidth + 1 # having the plus one lets us get to the end
        self.loose = l
        self.locked = False

    def re_init(self, xp, yp, sw, sh, l):
        self.swidth = sw
        self.sheight = sh # scrollbar height
        self.heighttowidth = sh - sw
        self.ratio = sh / self.heighttowidth; # Lets us know how much/far we can scroll
        self.xpos = xp - self.swidth / 2
        self.ypos = yp
        self.spos = 0 # Changes where the start button slider is
        self.newspos = self.spos
        self.sposMin = self.ypos
        self.sposMax = self.widget.height - self.swidth + 1; # having the plus one lets us get to the end
        self.loose = l
        self.locked = False

    def update(self):
        p = self.widget.intf.sketch

        if self.locked:            
            self.newspos = p.constrain(self.widget.mouse_y - self.swidth/2, self.sposMin, self.sposMax)
            print(self.newspos)

        if abs(self.newspos - self.spos) > 1:
            self.spos = self.spos + (self.newspos-self.spos)/self.loose

    def display(self):
        p = self.widget.intf.sketch

        p.fill(200) # change color of scrollbar
        p.rect(self.xpos, self.ypos, self.swidth, self.sheight)
        if self.widget.is_focused or self.locked:
            p.fill(255, 255, 0)
        else:
            p.fill(255, 0, 0)    
        p.rect(self.xpos, self.spos, self.swidth, self.swidth) # change size of square in scroll bar

    # Get the Position of scrollbar and show genes at that scrolling position
    def getPos(self):
        # Convert spos to be values between

        sizeWindowGenes = 50
    
        # THIS CODE SCALES TO THE VARIABLES IN GENESAR THAT ARE ADDED
        if len(self.widget.genesAr) > 0 and (len(self.widget.genesAr) * (self.widget.item_height + self.widget.item_sep) > (self.widget.height - self.widget.item_height - self.widget.item_sep)): # CHANGE 11 TO MAKE IT SCALABLE TO THE WINDOW GENES SIZE.
            for i in range(0, len(self.widget.genesAr)):
                sizeWindowGenes += 40
      
            newArrayScroll = sizeWindowGenes - (self.sposMax - 1) - self.widget.item_height; # 30 for swidth of bar + item_sep being excluded
            newScrollPos = self.spos * (newArrayScroll / (self.sposMax -1 ))
        
            if self.spos < 1: # Resets scrollbar back to the top when you scroll all the way back up
                self.spos = 0
                self.re_init(self.widget.width, 0, 20, self.widget.height, 16)
                self.widget.genesAr = [] # this lets the array list clear so that it can scrollbar can go back to normal scroll scale
                return newScrollPos
            elif newScrollPos < newArrayScroll:
                self.widget.genesAr = []
                return newScrollPos
            else:
                self.widget.genesAr = []
                return newArrayScroll

    
        elif len(self.widget.genesAr) > 0 and (len(self.widget.genesAr) * (self.widget.item_height + self.widget.item_sep) < (self.widget.height - self.widget.item_height - self.widget.item_sep)):
            self.re_init(0, 0, 0, 0, 0)
            self.widget.genesAr = [] # this lets the array list clear so that it can scrollbar can go back to normal scroll scale
            return 0
    
        elif len(self.widget.genesAr) == 0 and self.widget.noMatchFound:
            self.re_init(0, 0, 0, 0, 0)
            self.widget.genesAr = [] # this lets the array list clear so that it can scrollbar can go back to normal scroll scale
            return 0
    
        # This else statement occurs when genesAr == 0 so the Vertical Scroll Scale is adjusted back to the initial Genes list
        else:
            sizeWindowGenes += 40 * len(self.widget.genesAr)
            
            newScaleScroll = sizeWindowGenes - (self.sposMax - 1) - self.widget.item_height # works good for 500

            newScrollPos = self.spos * (newScaleScroll/ (self.sposMax -1))
    
            if self.spos < 1: # Resets scrollbar back to the top when you scroll all the way back up
                self.spos = 0
                self.re_init(self.widget.width, 0, 20, self.widget.height, 16)
                return newScrollPos
            
            elif newScrollPos < newScaleScroll:
                return newScrollPos
            else:
                return newScaleScroll