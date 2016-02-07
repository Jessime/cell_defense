# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:30:58 2016

@author: jessime
"""
import random
import time
import graphics as grf
import move

class Resource(object):
    
    def __init__(self, kind):
        self.kind = kind
        self.pic = self.make_pic()
        
    def make_pic(self):
        if self.kind == 'glucose':
            loc = grf.Point()
        elif self.kind == 'protein':
            loc = grf.Point()
        elif self.kind == 'lipid':
            loc = grf.Point()
        pic = grf.Image(loc, 'images/{}.gif'.format(self.kind))
        return pic

class Virus(object):
    
    def __init__(self, win, scale):
        self.win = win
        self.loc = grf.Point(random.randint(25, self.win.width - 225), 
                             random.randint(25, 50))
        self.pic = grf.Image(self.loc, 'images/virus.gif')
        self.power = random.randint(1, 5) * (int(scale**.5)+1)
        self.health = random.randint(5, 10) * (int(scale**.5)+1)
        self.move_prob = 2
        self.speed = random.randint(1, 4) * (int(scale**.5)+1)
        
    def move(self):
        """Move towards cells according to speed attribute"""
        y = self.pic.anchor.y
        hard_stop = self.win.height - (60+12)
        soft_stop = hard_stop - self.speed
        if random.randint(0,self.move_prob) == 0:
            if  y < soft_stop:
                self.pic.move(0, self.speed)
            elif soft_stop <= y < hard_stop:
                self.pic.move(0, hard_stop - y)
            
    def attack(self, cells):
        """Do damage to Cell if possible
        
        Parameters
        ----------
        cells : list of Cells
            The cells the player is attempting to defend from viruses       
        """
        x = self.pic.anchor.x
        y = self.pic.anchor.y
        if y == self.win.height - (60+12):
            for cell in cells:
                if move.point_in_rect(x, y+5, cell.pic):
                    cell.health -= self.power
                    break

class Cell(object):
    """Cells are what the player is stopping the Viruses from infecting.
    
    Parameters
    ----------
    win : graphics.GraphWin
        The window in which the Cell is drawn
    
    num : int
        Number designated to the Cell. Determines location on screen
        
    
    Attributes
    ----------
    win : graphics.GraphWin
        The window in which the Cell is drawn
    
    num : int
        Number designated to the Cell. Determines location on screen
        
    loc : graphics.Point
        The coordinate location for the cell
        
    pic : graphics.Image
        The picture representation of the Cell shown to player
        
    health : int
        The number of points of damage a Cell can withstand without being destroyed
        
    bar : graphics.Line
        A visual indicator of how much health a Cell has left
        """
    
    def __init__(self, win, num):
        self.win = win
        self.num = num
        self.loc = grf.Point(50+(self.num*100), self.win.height-30)
        self.pic = grf.Image(self.loc, 'images/cells.gif')
        self.health = 100
        self.bar = self.make_bar()
        
    def make_bar(self):
        """Initalizes the health bar for the cell
        
        Returns
        -------
        bar : graphics.Line
            The health bar for the cell        
        """
        p1 = grf.Point(self.num*100, self.win.height-30)
        p2 = grf.Point((self.num*100)+self.health, self.win.height-30)
        bar = grf.Line(p1, p2)
        bar.setOutline('red')
        bar.setWidth(4)
        return bar
        
    def update_bar(self):
        """Redraw the health bar to reflect current health level"""
        if self.health != 100:
            self.bar.p2.x = (self.num*100)+self.health
            self.bar.undraw()
            self.bar.draw(self.win)        
        
class Macrophage(object):
    
    def __init__(self, win):
        self.win = win
        self.pic = grf.Image(grf.Point(575, 200), 'images/macrophage2.gif')        
        self.speed = 10
        self.jump = 350
        self.jump_refresh = 3
        self.last_jump = 0

    def left(self):
        if self.pic.anchor.x >= 20:
            self.pic.move(-self.speed, 0)
        
    def down(self):
        if self.pic.anchor.y <= self.win.height - 20:
            self.pic.move(0, self.speed)

    def right(self):
        if self.pic.anchor.x <= self.win.width - 220:
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
        if (self.pic.anchor.x <= self.win.width - 220 - self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(self.jump, 0)
            self.last_jump = time.time()
            
    def up_jump(self):
        if (self.pic.anchor.y >= 20 + self.jump and
            self.last_jump + self.jump_refresh < time.time()):
            self.pic.move(0, -self.jump)
            self.last_jump = time.time()
