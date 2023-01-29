import py5
import py5_tools
from py5 import Sketch
import numpy as np
import pandas as pd

class SCIViewer(Sketch):
    
    def __init__(self, w, h, wt, df):
        super().__init__()
        self.w = w
        self.h = h
        self.wt = wt
        self.df = df
    
    def settings(self):
        self.size(self.w, self.h, py5.P2D)
        
    def setup(self):
        self.stroke_weight(self.wt)
        
    def draw(self):
        self.background(192)
        for (x, y) in zip(self.df.x_values, self.df.y_values):       # Plot the scatterplot
            self.ellipse(x, y, 5, 5)
        
    def mouse_clicked(self, e):
        self.println(e.get_x(), e.get_y())
        self.background(255, 0, 0)
    
        msgs = []
    
        for (x, y) in zip(self.df.x_values, self.df.y_values):
        
            range_1 = range(x-10, x+10, 1)
            range_2 = range(y-10, y+10, 1)
        
            if e.get_x() in range_1 and e.get_y() in range_2:
                self.println(e.get_x(), e.get_y())
                msgs.append('Target acquired')
                self.println(msgs)  
