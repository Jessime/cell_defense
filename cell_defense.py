# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 22:34:29 2016

@author: jessime

Description:

Notes:
Player's stuff (macrophage, towers, cells) is part of the Game
Viruses and Resources are part of the Level that spawns them
May work:
Attributes
    
win : graphics.GraphWin
    The new window in which the game will be rendered and played

level_num : int
    The total number of levels making up a game

level : Level
    The current level being played
    
mac : Macrophage
    The macrophage controlled by the player
    
cells : list of Cell objects
    The cells the player is attempting to defend from viruses
"""

import graphics as grf
import time
import random

def get_corners(pic):
    """Return the corner of an image
    
    :param pic: The image for which the corners will be found
    :type pic: graphics.Image 
    :return: Four values representing the boarders of the image
    :rtype: float
    """
    left = pic.anchor.x - (pic.getWidth()/2)
    top = pic.anchor.y - (pic.getWidth()/2)
    right = pic.anchor.x + (pic.getWidth()/2)
    bottom = pic.anchor.y + (pic.getWidth()/2)
    return left, top, right, bottom
    
def point_in_rect(x, y, pic):
    """Decide if a point is found within the corners of an image
    
    :param x: x coordinate for the point being checked
    :type x: int, float
    :param y: y coordinate for the point being checked
    :type y: int, float
    :param pic: The image in which to search for the given point
    :type pic: graphics.Image  
    :return: Whether or not the point lies within an image
    :rtype: bool            
    """
    inside = False
    left, top, right, bottom = get_corners(pic)
    if left <= x <= right and top <= y <= bottom:
        inside = True
    return inside
    
def collision_detection(pic1, pic2):
    """Decide if two images are touching on screen
    
    :param pic1: The first image for checking collision
    :type pic1: graphics.Image
    :param pic2: The second image for checking collison
    :type pic2: graphics.Image
    :return: Whether or not the two images have collided
    :rtype: bool
    """
    collision = False
    for a, b in [(pic1, pic2), (pic2, pic1)]:
        left, top, right, bottom = get_corners(a)
        if ((point_in_rect(left, top, b)) or
            (point_in_rect(left, bottom, b)) or
            (point_in_rect(right, top, b)) or
            (point_in_rect(right, bottom, b))):
            collision = True
    return collision

class Virus(object):
    
    def __init__(self, win, scale):
        self.win = win
        self.loc = grf.Point(random.randint(25, self.win.width - 225), 
                             random.randint(25, 50))
        self.pic = grf.Image(self.loc, 'images/virus.gif')
        self.power = random.randint(1, 5) * (int(scale**.5)+1)
        self.health = random.randint(5, 10) * (int(scale**.5)+1)
        self.speed = random.randint(1, 4) * (int(scale**.5)+1)
        
    def move(self):
        """Move towards cells according to speed attribute"""
        if self.pic.anchor.y <= self.win.height - 75:
            self.pic.move(0, self.speed)

class Cell(object):
    """Cells are what the player is stopping the Viruses from infecting."""
    
    def __init__(self, win, num):
        self.win = win
        self.num = num
        self.loc = grf.Point(50+(self.num*100), self.win.height-30)
        self.pic = grf.Image(self.loc, 'images/cells.gif')
        self.health = 100
        self.bar = None
        
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
    
    def __init__(self, num, win, mac, cells):
        self.num = num
        self.win = win
        self.mac = mac
        self.cells = cells
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
        return set(viruses)

    def draw_info_section(self):
        """Draws the right area of the screen where game statistcs are kept"""
        p1 = grf.Point(self.win.width-200, 0)
        p2 = grf.Point(self.win.width, self.win.height)
        background = grf.Rectangle(p1, p2)
        background.setFill('grey')
        background.draw(self.win)
        
    def initial_render(self):
        """Draw everything on screen at the beginning of a level"""
        self.draw_info_section()
        
        self.mac.pic.draw(self.win)
        [v.pic.draw(self.win) for v in self.viruses]
        [c.pic.draw(self.win) for c in self.cells]
        #draw towers
        
    def check_eaten(self):
        """Use collision detection to decide which viruses have been eaten"""
        eaten = []
        for v in self.viruses:
            if collision_detection(v.pic, self.mac.pic):
                eaten.append(v)
                v.pic.undraw()
        self.viruses.difference_update(eaten)
        
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
                
            #Move    
            if random.randint(0, 5) == 0:                
                [v.move() for v in self.viruses]
                
            if random.randint(0, 500):
                self.check_eaten()
            #update time
            current_time = time.time() 
        
        self.mac.pic.undraw()

        
class Game(object):
    """A single game of Cell Defense, primarily consisting of a series of Levels
    
    :py:attr win: The new window in which the game will be rendered and played
    :type win: graphics.GraphWin
    """
    
    def __init__(self):
        self.win = grf.GraphWin('Cell Defense', 1200, 800)
        self.level_num = 10
        self.level = None
        self.mac = Macrophage(self.win)
        self.cells = [Cell(self.win, i) for i in xrange(10)]
        
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
            self.current_level = Level(lvl, self.win, self.mac, self.cells)
            self.current_level.play()
        self.game_results()    
        self.win.getMouse()
        self.win.close()

        
if __name__ == '__main__':
    game = Game()
    game.run()