import py5
import py5_tools
from py5 import Sketch

from . import utils

class Test(Sketch):

    def settings(self):
        self.size(400, 400, py5.P2D)

    def setup(self):
        self.background(180)

    def draw(self):
        self.ellipse(self.mouse_x, self.mouse_y, 5, 5)

    def say_something(self):
        print(utils.get_message())

def view():
   test = Test()
   test.run_sketch()

   # We wait until the sketch is running
   while not test.is_running: 
       print(test.is_running)
       continue

   portal = py5_tools.sketch_portal(sketch=test, quality=75, scale=1.0)
   return portal