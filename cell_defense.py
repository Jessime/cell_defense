# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 22:34:29 2016

@author: jessime
"""

import graphics as grf
import time
import random

class Virus(object):
    
    def __init__(self, win, level):
        self.loc = grf.Point(random.randint(25, win.width - 25), 
                             random.randint(25, win.height))
        self.pic = grf.Image(self.loc, 'images/virus.gif')
        self.power = random.randint(1, 5) * int(level**.5)
        self.health = random.randint(5, 10) * int(level**.5)
        self.speed = random.randint(1, 5) * int(level**.5)
        
class Level(object):
    
    def __init__(self, num):
        self.num = num
        self.viruses = self.spawn_viruses()

    def spawn_viruses(self):
        pass
    
    def interlude(self):
        pass
    
    def play(self):
        if self.num == 1:
            self.mac.draw(self.win)
        current_time = time.time()
        end_time = current_time + 45
        
        while current_time < end_time:
            last_key = self.win.checkKey()
            if last_key in self.action:
                self.action[last_key]()
                    
            #update time
            current_time = time.time()        
        
class Game(object):
    
    def __init__(self):
        self.win = grf.GraphWin('Cell Defense', 1200, 800)
        self.level_num = 1
        self.level = Level(self.level_num)
        self.mac = grf.Image(grf.Point(575, 200), 'images/macrophage2.gif')
        self.jump = 300
        self.last_jump = 0
        self.jump_refresh = 3
        self.action = {'a': self.left,
                       's': self.down,
                       'd': self.right,
                       'w': self.up,
                       'j': self.left_jump,
                       'k': self.down_jump,
                       'l': self.right_jump,
                       'i': self.up_jump}
        self.viruses = []

    ### Actions ###

    def left(self):
        if self.mac.anchor.x >= 20:
            self.mac.move(-10, 0)
        
    def down(self):
        if self.mac.anchor.y <= self.win.height - 20:
            self.mac.move(0, 10)

    def right(self):
        if self.mac.anchor.x <= self.win.width - 20:
            self.mac.move(10, 0)
        
    def up(self):
        if self.mac.anchor.y >= 20:
            self.mac.move(0, -10)
            
    def left_jump(self):
        if (self.mac.anchor.x >= 20+self.jump and 
            self.last_jump + self.jump_refresh < time.time()):
            self.mac.move(-self.jump, 0)
            self.last_jump = time.time()
            
    def down_jump(self):
        if (self.mac.anchor.y <= self.win.height-20-self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.mac.move(0, self.jump)
            self.last_jump = time.time()
            
    def right_jump(self):
        if (self.mac.anchor.x <= self.win.width - 20 - self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.mac.move(self.jump, 0)
            self.last_jump = time.time()
            
    def up_jump(self):
        if (self.mac.anchor.y >= 20 + self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.mac.move(0, -self.jump)
            self.last_jump = time.time()
            
    ### End of Actions ###
    
    def play_level(self):
        try:
            self.mac.draw(self.win)
        except grf.GraphicsError:
            pass
        current_time = time.time()
        end_time = current_time + 45
        
        while current_time < end_time:
            last_key = self.win.checkKey()
            if last_key in self.action:
                self.action[last_key]()
                    
            #update time
            current_time = time.time()

    def run(self):
        self.win.setBackground('white')
        for level in xrange(self.level_num):
            self.level = Level(level)
            self.
            self.play_level()
            print level
            
        self.win.getMouse()
        self.win.close()

        
if __name__ == '__main__':
    game = Game()
    game.run()