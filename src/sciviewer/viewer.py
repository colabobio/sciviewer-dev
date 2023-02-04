from sciviewer import utils
from sciviewer.data import Data

if utils.is_mac() and utils.in_notebook():
    # Exectutes the required magic for Py5 to work in notebook mode on Mac:
    # http://py5coding.org/content/osx_users.html#jupyter-notebooks
    get_ipython().run_line_magic('gui', 'osx')

import py5
import py5_tools
from py5 import Sketch

_viewer = None

class Viewer(Sketch):
    def __init__(self, size):
        super().__init__()
        self.out_width = size
        self.out_height = size

    def settings(self):
        self.size(self.out_width, self.out_height, py5.P2D)

    def setup(self):
        surface = self.get_surface()
        surface.set_resizable(True)
        surface.set_title("single-cell interactive viewer")

        self.background(180)

    def draw(self):
        self.ellipse(self.mouse_x, self.mouse_y, 5, 5)

def open_viewer(adata, size):
    global _viewer

    data = Data(adata)

    _viewer = Viewer(data, size)
    _viewer.run_sketch()

def embed_viewer():
    global _viewer
    portal = py5_tools.sketch_portal(sketch=_viewer, quality=85, scale=1.0)
    return portal
