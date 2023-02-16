from sciviewer import utils
from sciviewer.data import Data
from sciviewer.ui.interface import Interface
from sciviewer.ui.scatter import Scatter
from sciviewer.ui.buttons import Button
from sciviewer.ui.buttons import SwitchButton
from sciviewer.ui.selectors import DifferentialSelector
from sciviewer.ui.selectors import SingleDirectionalSelector
from sciviewer.ui.scroller import GeneScroller
from sciviewer.ui.scroller import SpaceFiller

if utils.is_mac() and utils.in_notebook():
    # Exectutes the required magic for Py5 to work in notebook mode on Mac:
    # http://py5coding.org/content/osx_users.html#jupyter-notebooks
    from IPython import get_ipython
    get_ipython().run_line_magic('gui', 'osx')

import py5_tools
from py5 import Sketch

_viewer = None

class Viewer(Sketch):
    def __init__(self, data, size):
        super().__init__()
        self.out_width = size
        self.out_height = int((0.8 * size)/2)
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

    def switch_to_diff_selection(self):
        self.intf.get_widget("diff_selector").activate()
        self.intf.get_widget("dir_selector").deactivate()
        self.intf.get_widget("dir_button").switch_off()

    def switch_to_dir_selection(self):
        self.intf.get_widget("diff_selector").deactivate()
        self.intf.get_widget("dir_selector").activate()
        self.intf.get_widget("diff_button").switch_off()

    def set_differential_selection(self, sel_area):
        self.intf.get_widget("scatter").select_cells(sel_area)

    def set_directional_selection(self, sel_dir, sel_area):
        self.intf.get_widget("scatter").select_cells(sel_area)

    def clear_selected_cells(self):
        self.intf.get_widget("scatter").clear_selection()

    def init_ui(self):
        # All dimensions below are assuming a window of 1250 x 500, the interface object will scale everything appropriately 
        # based on the actual size provided by the user
        scatter_width = 500
        scroll_width = 250
        button_height = 25

        self.intf = Interface(self, self.width / 1250)
        self.intf.add_font("Helvetica", 14)

        scatter = Scatter(self.intf, 0, 0, scatter_width, scatter_width, name="scatter")
        self.intf.add_widget(scatter)

        diff_selector = DifferentialSelector(self.intf, 0, 0, scatter_width, scatter_width, name="diff_selector", callback=self.set_differential_selection)
        dir_selector = SingleDirectionalSelector(self.intf, 0, 0, scatter_width, scatter_width, name="dir_selector", callback=self.set_directional_selection)
        self.intf.add_widget(diff_selector, parent_name="scatter")
        self.intf.add_widget(dir_selector, parent_name="scatter")

        diff_button = SwitchButton(self.intf, scatter_width + 10, 10, scroll_width, button_height, name="diff_button", callback=self.switch_to_diff_selection, label="Differential selection")
        dir_button = SwitchButton(self.intf, scatter_width + 10, 40, scroll_width, button_height, name="dir_button", callback=self.switch_to_dir_selection, label="Directional selection")
        clear_button = Button(self.intf, scatter_width + 10, 70, scroll_width, button_height, name="clear_button", callback=self.clear_selected_cells, label="Clear selection")
        self.intf.add_widget(diff_button)
        self.intf.add_widget(dir_button)
        self.intf.add_widget(clear_button)

        scroller = GeneScroller(self.intf, scatter_width + 10, 130, scroll_width, 370, name="scroller", iheght=30, isep=10, sw=20, l=16)
        self.intf.add_widget(scroller)
        self.intf.add_widget(SpaceFiller(self.intf, scatter_width + 10, 100, scroll_width, 30))


def open_viewer(adata, size):
    global _viewer

    data = Data(adata)

    _viewer = Viewer(data, size)
    _viewer.run_sketch()

def embed_viewer():
    global _viewer
    portal = py5_tools.sketch_portal(sketch=_viewer, quality=85, scale=1.0)
    return portal
