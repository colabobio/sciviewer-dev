from . import utils

class Test:
    def add_one(self, number):
        return number + 1

    def add_two(self, number):
        return number + 2

    def add_three(self, number):
        return number + 3

    def say_something(self):
        print(utils.get_message())