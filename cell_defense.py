# -*- coding: utf-8 -*-
"""
Welcome to Cell Defense!

Description
-----------

This is a tower defense style game with a biological theme.
The player controls a macrophage cell, in an attempt to defend healthy cells from viruses. 

Notes
-----

Player's stuff (macrophage, towers, cells) is part of the Game
Viruses and Resources are part of the Level that spawns them

Controls
--------

Definitely should include description of controls somewhere here.
"""

import time
import random
import sys

import graphics as grf
import pieces
import move

class Panel(object):
    """Section on the right of the screen used for displaying Game information"""
    
    def __init__(self, win):
        self.win = win
        self.background = self.make_background()
    
    def make_background(self):
        """Draws the right area of the screen where game statistcs are kept"""
        p1 = grf.Point(self.win.width-200, 0)
        p2 = grf.Point(self.win.width, self.win.height)
        background = grf.Rectangle(p1, p2)
        background.setFill('grey')
        return background
        
class Level(object):
    
    def __init__(self, num, win, mac, cells):
        self.num = num
        self.win = win
        self.mac = mac
        self.cells = cells
        self.panel = Panel(self.win)
        self.len = 15
        self.framerate = 1/20.
        self.current_time = None
        self.end_time = None
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
            viruses.append(pieces.Virus(self.win, self.num))
        return set(viruses)
        
    def initial_render(self):
        """Draw everything on screen at the beginning of a level"""
        self.panel.background.draw(self.win)
        self.mac.pic.draw(self.win)
        [v.pic.draw(self.win) for v in self.viruses]
        [c.pic.draw(self.win) for c in self.cells]
        [c.bar.draw(self.win) for c in self.cells]
        #draw towers
        
    def cleanup(self):
        self.panel.background.undraw()
        self.mac.pic.undraw()
        [v.pic.undraw() for v in self.viruses]
        [c.pic.undraw() for c in self.cells]
        [c.bar.undraw() for c in self.cells]        
        
    def check_eaten(self):
        """Use collision detection to decide which viruses have been eaten"""
        eaten = []
        for v in self.viruses:
            if move.collision_detection(v.pic, self.mac.pic):
                eaten.append(v)
                v.pic.undraw()
        self.viruses.difference_update(eaten)
        
    def check_infected(self):
        """Use cell health to check if any cells have been infected"""
        healthy = []
        for c in self.cells:
            if c.health <= 0:
                c.pic.undraw()
                c.bar.undraw()
            else:
                healthy.append(c)
        self.cells = healthy
        
    def interlude(self):
        pass
    
    def level_over(self):
        """Check if the level is over.
        
        The level can end in several different ways:
        
        1. The time for the level runs out
        2. The player kills all of the viruses
        3. The player loses more than half of the cells and loses the game.
  
        Returns
        -------
        over : bool
            Whether or not the level is over
        """
        over = False
        if (self.current_time >= self.end_time or
            len(self.viruses) == 0 or
            len(self.cells) < 5):
            over = True
        return over

    def update_player(self):
        last_key = self.win.checkKey()
        if last_key in self.action:
            self.action[last_key]()
    
    def update_viruses(self):
        self.check_eaten()
        [v.move() for v in self.viruses]
        [v.attack(self.cells) for v in self.viruses]
        
    def update_cells(self):
        self.check_infected()
        [c.update_bar() for c in self.cells]
        
    def update_time(self, loop_start):
        """Limit loop to framerate, sleeping if necessary. Update current time."""
        loop_end = time.time()
        execute_time = loop_end - loop_start
        if execute_time < self.framerate:
            time.sleep(self.framerate - execute_time)
        self.current_time = time.time()         
        
    def update(self):
        """The main loop of a level. Responsible for checking changes each frame."""
        loop_start = time.time()
        self.update_player()
        self.update_viruses()
        self.update_cells()
        self.update_time(loop_start)
       
    def play(self):
        """Wrapper function for everything that happens during a level."""
        self.interlude()
        self.initial_render()
        self.current_time = time.time()
        self.end_time = self.current_time + self.len
        while not self.level_over():
            self.update()
        self.cleanup()
        

        
class Game(object):
    """A single game of Cell Defense, primarily consisting of a series of Levels.
    
    Attributes
    ----------    
    win : graphics.GraphWin
        The new window in which the game will be rendered and played
    
    level_num : int
        The total number of levels making up a game
    
    level : Level
        The current level being played
        
    mac : Macrophage
        The macrophage controlled by the player
        
    cells : list of Cells
        The cells the player is attempting to defend from viruses
    """
    
    def __init__(self):
        self.win = grf.GraphWin('Cell Defense', 1200, 800)
        self.level_num = 10
        self.level = None
        self.mac = pieces.Macrophage(self.win)
        self.cells = [pieces.Cell(self.win, i) for i in xrange(10)]
        
    def start_menu(self):
        """An initial start menu where player can tune settings."""
        pass

    def game_results(self):
        """Decides if the game was a win or loss, and displays appropriate screen."""
        pass
    
    def run(self):
        """Launches the game."""
        self.win.setBackground('white')
        self.start_menu()
        for lvl in xrange(self.level_num):
            self.current_level = Level(lvl, self.win, self.mac, self.cells)
            self.current_level.play()
        self.game_results()    
        self.win.getMouse()
        self.win.close()

        
if __name__ == '__main__':
    game = Game()
    game.run()