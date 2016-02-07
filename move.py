# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 16:48:47 2016

@author: jessime
"""

def get_corners(pic):
    """Return the corner of an image
    
    Parameters
    ----------
    pic : graphics.Image
        The image for which the corners will be found
        
    Returns
    -------
    tuple
        Four values representing the boarders of the image
    """
    left = pic.anchor.x - (pic.getWidth()/2)
    top = pic.anchor.y - (pic.getWidth()/2)
    right = pic.anchor.x + (pic.getWidth()/2)
    bottom = pic.anchor.y + (pic.getWidth()/2)
    return (left, top, right, bottom)
    
def point_in_rect(x, y, pic):
    """Decide if a point is found within the corners of an image
    
    Parameters
    ----------
    x : int, float
        x coordinate for the point being checked
    y : int, float
        y coordinate for the point being checked
    pic : graphics.Image
        The image in which to search for the given point
    
    Returns
    -------
    inside : bool
        Whether or not the point lies within an image            
    """
    inside = False
    left, top, right, bottom = get_corners(pic)
    if left <= x <= right and top <= y <= bottom:
        inside = True
    return inside
    
def collision_detection(pic1, pic2):
    """Decide if two images are touching on screen

    Parameters
    ----------
    pic1 : graphics.Image
        The first image for checking collision
    pic2 : graphics.Image
        The second image for checking collison

    Returns
    -------
    collision : bool
        Whether or not the two images have collided
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