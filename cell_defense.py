# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 22:34:29 2016

@author: jessime

Description:

Notes:
Player's stuff (macrophage, towers, cells) is part of the Game
Viruses and Resources are part of the Level that spawns them
"""

import graphics as grf
import time
import random

class Virus(object):
    
    def __init__(self, win, scale):
        self.win = win
        self.loc = grf.Point(random.randint(25, self.win.width - 25), 
                             random.randint(25, 50))
        self.pic = grf.Image(self.loc, 'images/virus.gif')
        self.power = random.randint(1, 5) * (int(scale**.5)+1)
        self.health = random.randint(5, 10) * (int(scale**.5)+1)
        self.speed = random.randint(1, 4) * (int(scale**.5)+1)
        
    def move(self):
        """Move towards cells according to speed attribute"""
        if self.pic.anchor.y <= self.win.height - 150:
            self.pic.move(0, self.speed)

            
class Macrophage(object):
    
    def __init__(self, win):
        self.win = win
        self.pic = grf.Image(grf.Point(575, 200), 'images/macrophage2.gif')        
        self.speed = 10
        self.jump = 300
        self.jump_refresh = 3
        self.last_jump = 0

    def left(self):
        if self.pic.anchor.x >= 20:
            self.pic.move(-self.speed, 0)
        
    def down(self):
        if self.pic.anchor.y <= self.win.height - 20:
            self.pic.move(0, self.speed)

    def right(self):
        if self.pic.anchor.x <= self.win.width - 20:
            self.pic.move(self.speed, 0)
        
    def up(self):
        if self.pic.anchor.y >= 20:
            self.pic.move(0, -self.speed)
            
    def left_jump(self):
        if (self.pic.anchor.x >= 20+self.jump and 
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(-self.jump, 0)
            self.last_jump = time.time()
            
    def down_jump(self):
        if (self.pic.anchor.y <= self.win.height-20-self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(0, self.jump)
            self.last_jump = time.time()
            
    def right_jump(self):
        if (self.pic.anchor.x <= self.win.width - 20 - self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(self.jump, 0)
            self.last_jump = time.time()
            
    def up_jump(self):
        if (self.pic.anchor.y >= 20 + self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(0, -self.jump)
            self.last_jump = time.time()

        
class Level(object):
    
    def __init__(self, num, win, mac):
        self.num = num
        self.win = win
        self.mac = mac
        self.len = 45
        self.viruses = self.spawn_viruses()        
        self.action = {'a': self.mac.left,
                       's': self.mac.down,
                       'd': self.mac.right,
                       'w': self.mac.up,
                       'j': self.mac.left_jump,
                       'k': self.mac.down_jump,
                       'l': self.mac.right_jump,
                       'i': self.mac.up_jump}
            
    def spawn_viruses(self):
        """Randomly generate a number of viruses to fight"""
        viruses = []
        for v in xrange(random.randint(10, 10 + self.num*2)):
            viruses.append(Virus(self.win, self.num))
        return viruses

    def initial_render(self):
        """Draw everything on screen at the beginning of a level"""
        self.mac.pic.draw(self.win)
        [v.pic.draw(self.win) for v in self.viruses]
        #draw cells
        #draw towers
        
    def interlude(self):
        pass
    
    def play(self):
        self.interlude()
        self.initial_render()
            
        current_time = time.time()
        end_time = current_time + self.len
        
        while current_time < end_time:
            last_key = self.win.checkKey()
            if last_key in self.action:
                self.action[last_key]()
                
            if random.randint(0, 1000) == 0:                
                [v.move() for v in self.viruses]
            #update time
            current_time = time.time() 
        
        self.mac.pic.undraw()

        
class Game(object):
    
    def __init__(self):
        """A single game of Cell Defense, primarily consisting of a series of Levels"""
        self.win = grf.GraphWin('Cell Defense', 1200, 800)
        self.level_num = 10
        self.level = None
        self.mac = Macrophage(self.win)
        
    def start_menu(self):
        """An initial start menu where player can tune settings"""
        pass
    
    def game_results(self):
        """Decides if the game was a win or loss, and displays appropriate screen"""
        pass
    
    def run(self):
        """Launches the game"""
        self.win.setBackground('white')
        self.start_menu()
        for lvl in xrange(self.level_num):
            self.current_level = Level(lvl, self.win, self.mac)
            self.current_level.play()
        self.game_results()    
        self.win.getMouse()
        self.win.close()

        
if __name__ == '__main__':
    game = Game()
    game.run()