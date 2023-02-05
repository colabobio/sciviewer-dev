from sciviewer import utils
from sciviewer.data import Data
from sciviewer.ui.interface import Interface
from sciviewer.ui.scatter import Scatter
from sciviewer.ui.buttons import SwitchButton

if utils.is_mac() and utils.in_notebook():
    # Exectutes the required magic for Py5 to work in notebook mode on Mac:
    # http://py5coding.org/content/osx_users.html#jupyter-notebooks
    from IPython import get_ipython
    get_ipython().run_line_magic('gui', 'osx')

import py5
import py5_tools
from py5 import Sketch

_viewer = None

class Viewer(Sketch):
    def __init__(self, data, size):
        super().__init__()
        self.out_width = size
        self.out_height = size
        self.data = data        

    def settings(self):
        self.size(self.out_width, self.out_height, self.P2D)

    def setup(self):
        surface = self.get_surface()
        surface.set_resizable(False)
        surface.set_title("single-cell interactive viewer")
        self.init_ui()

    def draw(self):
        self.background(255)
        self.intf.update()

    def mouse_pressed(self):
        self.intf.mouse_pressed()

    def mouse_moved(self):
       self.intf.mouse_moved() 

    def mouse_dragged(self):
       self.intf.mouse_dragged()

    def mouse_released(self):
       self.intf.mouse_released()

    def set_differential_selection(self):
        print("setting differential selection")
        self.intf.get_widget("dir_button").switch_off()

    def set_directional_selection(self):
        print("setting directional selection")
        self.intf.get_widget("diff_button").switch_off()

    def init_ui(self):
        self.intf = Interface(self)        
        self.intf.add_font("Helvetica", 14)
        self.intf.add_widget(Scatter(self.intf, 0, 0, self.width, self.height), name="scatter")

        dif_switch_btn = SwitchButton(self.intf, self.width - 170, 20, 150, 25, callback=self.set_differential_selection, label="Differential selection")
        dir_switch_btn = SwitchButton(self.intf, self.width - 170, 50, 150, 25, callback=self.set_directional_selection, label="Directional selection")
        self.intf.add_widget(dif_switch_btn, name="diff_button", parent_name="scatter")
        self.intf.add_widget(dir_switch_btn, name="dir_button", parent_name="scatter")

def open_viewer(adata, size):
    global _viewer

    data = Data(adata)

    _viewer = Viewer(data, size)
    _viewer.run_sketch()

def embed_viewer():
    global _viewer
    portal = py5_tools.sketch_portal(sketch=_viewer, quality=85, scale=1.0)
    return portal
