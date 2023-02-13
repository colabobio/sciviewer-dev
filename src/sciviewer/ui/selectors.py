from sciviewer.ui.widget import Widget
from sciviewer.utils import angle_between

import numpy as np
import numpy.linalg as la

class DifferentialSelector(Widget):
    def setup(self):       
        self.is_active = False

        self.selection = []
        self.tolerance = 10 * self.intf.scale_factor

    def draw(self):
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

        if self.is_active:
            p.no_fill()
            p.ellipse(self.mouse_x, self.mouse_y, self.tolerance, self.tolerance)

    def release(self):
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
        self.selection = []

    def set_active(self):
        self.selection = []

    def set_inactive(self):
        self.selection = []
                
class MultiDirectionalSelector(Widget):
    def setup(self):
        self.is_active = False

        self.tolerance = 10 * self.intf.scale_factor
        self.spine = []
        self.selection = []
        self.spine_mode = True

    def draw(self):
        p = self.intf.sketch

        p.stroke(230, 20, 20)
        
        if 0 < len(self.spine):
            if 1 < len(self.spine):
                p.no_fill()
                p.begin_shape()
                for mpos in self.spine:
                    p.vertex(mpos[0], mpos[1])
                p.vertex(self.mouse_x, self.mouse_y)
                p.end_shape()
            else:
                mpos0 = self.spine[0]
                p.line(mpos0[0], mpos0[1], self.mouse_x, self.mouse_y)

        if not self.spine_mode and 1 < len(self.spine):
            self.update_selection(self.mouse_x, self.mouse_y)
            p.fill(230, 20, 20, 100)
            p.begin_shape()
            for mpos in self.selection:
                p.vertex(mpos[0], mpos[1])                
            p.end_shape(p.CLOSE)
            ppos = self.spine[-1]
            p.line(ppos[0], ppos[1], self.mouse_x, self.mouse_y)

        if self.is_active:
            p.no_fill()
            p.ellipse(self.mouse_x, self.mouse_y, self.tolerance, self.tolerance)

    def release(self):
        p = self.intf.sketch
        if p.mouse_button == p.LEFT:
            if self.spine_mode:
                self.update_spine()
            else:
                if self.callback: self.callback(self.selection)
                self.spine = []
                self.selection = []
                self.spine_mode = True
                return                    
        else:     
            self.spine = []
            self.selection = []

    def update_spine(self):
        p = self.intf.sketch
        if 0 < len(self.spine):
            pmouse = self.spine[-1]
            if self.tolerance < p.dist(pmouse[0], pmouse[1], self.mouse_x, self.mouse_y):
                self.spine += [(self.mouse_x, self.mouse_y)]
            else:
                self.spine_mode = False
        else:
            self.spine = [(self.mouse_x, self.mouse_y)]

    def update_selection(self, mx, my):
        ppos1 = self.spine[-1]
        ppos2 = self.spine[-2]
        
        dirpt = np.array([mx - ppos1[0], my - ppos1[1]])        
        dirsp = np.array([ppos1[1] - ppos2[1], ppos2[0] - ppos1[0]])
        
        lenpt = la.norm(dirpt)
        lensp = la.norm(dirsp)

        if 0 < lensp and 0 < lenpt: 
            self.selection = []

            a = angle_between(dirpt, dirsp)
            proj = np.cos(a) * lenpt / lensp

            poly_width = abs(proj) * self.width / 2

            n = len(self.spine)
            # Adding points backwards
            for idx in range(0, n - 1, 1):
                ib1 = n - 1 - idx
                ib2 = ib1 - 1

                ppos1 = self.spine[ib1]
                ppos2 = self.spine[ib2]

                dirsp = np.array([ppos1[1] - ppos2[1], ppos2[0] - ppos1[0]])
                dirsp = dirsp / la.norm(dirsp)

                if idx == 0:
                    new_pos0 = ppos1 - poly_width * dirsp
                    self.selection += [(new_pos0[0], new_pos0[1])]

                new_pos = ppos1 + poly_width * dirsp
                self.selection += [(new_pos[0], new_pos[1])]
                        
            # Adding points forwards
            for idx in range(0, n - 1, 1):
                if1 = idx
                if2 = idx + 1

                ppos1 = self.spine[if1]
                ppos2 = self.spine[if2]

                dirsp = np.array([ppos1[1] - ppos2[1], ppos2[0] - ppos1[0]])
                dirsp = dirsp / la.norm(dirsp)

                if idx == 0:
                    new_pos1 = ppos1 - poly_width * dirsp
                    self.selection += [(new_pos1[0], new_pos1[1])]

                new_pos = ppos1 + poly_width * dirsp
                self.selection += [(new_pos[0], new_pos[1])]

    def lost_focus(self):
        self.spine = []
        self.selection = []

    def set_active(self):
        self.spine_mode = True
        self.spine = []
        self.selection = []

    def set_inactive(self):
        self.spine = []
        self.selection = []

class SingleDirectionalSelector(MultiDirectionalSelector):
    def update_spine(self):
        p = self.intf.sketch
        if 0 < len(self.spine):
            pmouse = self.spine[-1]
            if self.tolerance < p.dist(pmouse[0], pmouse[1], self.mouse_x, self.mouse_y):
                self.spine += [(self.mouse_x, self.mouse_y)]
                if len(self.spine) == 2:
                    self.spine_mode = False
        else:
            self.spine = [(self.mouse_x, self.mouse_y)]       