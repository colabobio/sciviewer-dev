import py5
import py5_tools
import numpy as np
import pandas as pd

#setup the sketch portal
def setup():
    py5.size(x_axis, y_axis, py5.P3D)                  #setup the size and rendering of Sketch Portal
    py5.stroke_weight(point_thick)                         #setup the appearance of things in the portal  
    
def draw():
    py5.background(192)

    for (x, y) in zip(df.x_values, df.y_values):       # Plot the scatterplot
        py5.ellipse(x, y, 5, 5)
    
def mouse_clicked(e):

    py5.println(e.get_x(), e.get_y())
    
    msgs = []
    
    for (x, y) in zip(df.x_values, df.y_values):
        
        range_1 = range(x-10, x+10, 1)
        range_2 = range(y-10, y+10, 1)
        
        if e.get_x() in range_1 and e.get_y() in range_2:
            py5.println(e.get_x(), e.get_y())
            msgs.append('Target acquired')
            py5.println(msgs)