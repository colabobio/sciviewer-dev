from sciviewer import utils
from sciviewer.data import Data

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
        self.size(self.out_width, self.out_height, py5.P2D)

    def setup(self):
        surface = self.get_surface()
        surface.set_resizable(True)
        surface.set_title("single-cell interactive viewer")
        self.no_stroke()
        self.fill(0, 100)

    def draw(self):
        self.background(255)
        for cell in self.data.cells:
            x = self.remap(cell.umap1, 0, 1, 0, self.width)
            y = self.remap(cell.umap2, 0, 1, 0, self.height)
            self.ellipse(x, y, 3, 3)

def open_viewer(adata, size):
    global _viewer

    data = Data(adata)

    _viewer = Viewer(data, size)
    _viewer.run_sketch()

def embed_viewer():
    global _viewer
    portal = py5_tools.sketch_portal(sketch=_viewer, quality=85, scale=1.0)
    return portal
