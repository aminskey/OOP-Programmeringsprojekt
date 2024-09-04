import random
import pygame

from vector import Vector
from pygame.locals import *
from math import degrees
from os import listdir

FPS = 60
stdFPS = 45

dTime = stdFPS/FPS

GREEN = (0, 0, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

bubbleGrp = pygame.sprite.Group()
frontBub = pygame.sprite.Group()
backBub = pygame.sprite.Group()

def isInRange(x, offset, min, max):
    return (x - offset) > min and (x + offset) < max

def isInBounds(pos, offset, minPoint, maxPoint):
    return isInRange(pos[0], offset, minPoint[0], maxPoint[0]) and isInRange(pos[1], offset, minPoint[1], maxPoint[1])