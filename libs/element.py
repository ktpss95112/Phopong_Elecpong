import pygame as pg
import random

import os.path
if 'libs' in __name__:
    from libs.GlobalParameters import *
    from libs.utility import *
    from libs.OtherObjects import Timer
else:
    from GlobalParameters import *
    from utility import *
    from OtherObjects import Timer

random.seed()

class Particle():
    """
    Particles.pos -> pg.Rect
    Particles.vel -> pygame.math.Vector2
    """
    radius = 10
    color = None
    def __init__(self, center_position, velocity, spe_args=None):
        self.pos = pg.Rect(0, 0, self.radius, self.radius)
        self.pos.center = center_position
        self.center_position = center_position
        self.vel = velocity
        self.specific_init(spe_args)
        self.timer = Timer()

    def specific_init(self, args):
        pass

    def update_pos(self):
        self.center_position += self.vel * self.timer.dt() * 60
        self.pos.center = self.center_position

    def collide_with(self, rect):
        return self.pos.colliderect(rect)

    def inside(self, rect):
        return rect.contains(self.pos)

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color(self.color), self.pos)




class Photon(Particle):
    color_table = {1:'red2', 2:'darkorange', 3:'yellow', 4:'green', 5:'cyan2', 6:'blue', 7:'purple'}
    def specific_init(self, args):
        self.color_n = random.randint(1, 7)
        self.color = self.color_table[self.color_n]







class Electron(Particle):
    color = 'gray77'
    def specific_init(self, args):
        pass

