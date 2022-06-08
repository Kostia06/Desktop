import pyautogui as p
from pynput.mouse import Listener
import clipboard as cb
import time as t
class Mouse():
    def __init__(self):
        self.work = False
        self.list = []
        self.change_back = False
        self.x = 0
        self.y= 0
    def update(self):
        one = t.time_ns()
        p.PAUSE = 0.00001
        r,g,b = p.pixel(self.x*2, self.y*2)
        self.list = [r,g,b]
        return self.list
        two = t.time_ns()
    def pos(self, x, y):
        self.x = x 
        self.y = y
    def change(self, x, y, button, pressed):
        if self.work and pressed:
            self.work = False
            self.change_back = True
            cb.copy(str(self.list))
    def input(self):
        with Listener(on_click=self.change, on_move=self.pos) as  m:
            m.join()