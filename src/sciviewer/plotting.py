import py5
import py5_tools
from py5 import Sketch

from . import utils

class Test(Sketch):

    def settings(self):
        self.size(400, 400)

    def setup(self):
        self.background(180)

    def draw(self):
        self.ellipse(self.mouse_x, self.mouse_y, 5, 5)

    def say_something(self):
        print(utils.get_message())