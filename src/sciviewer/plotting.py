from sciviewer import utils

if utils.is_mac() and utils.in_notebook():
    # Exectutes the required magic for Py5 to work in notebook mode on Mac:
    # http://py5coding.org/content/osx_users.html#jupyter-notebooks
    get_ipython().run_line_magic('gui', 'osx')

import py5
import py5_tools
from py5 import Sketch

_viewer = None

def test():
    print(utils.get_message())

class TestSketch(Sketch):

    def settings(self):
        self.size(400, 400, py5.P2D)

    def setup(self):
        self.background(180)

    def draw(self):
        self.ellipse(self.mouse_x, self.mouse_y, 5, 5)

def open_viewer():
    global _viewer
    viewer = TestSketch()
    _viewer = viewer
    viewer.run_sketch()

def embed_viewer():
    global _viewer
    viewer = _viewer
    portal = py5_tools.sketch_portal(sketch=viewer, quality=85, scale=1.0)
    return portal
