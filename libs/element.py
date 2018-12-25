import pygame as pg
import random

random.seed()

class Particle():
    """
    Particles.pos -> pg.Rect
    Particles.vel -> tuple like (x, y)
    """
    radius = 10
    def __init__(self, center_position, velocity, spe_args):
        self.pos = pg.Rect(0, 0, radius, radius)
        self.pos.center = center_position
        self.vel = vel
        self.specific_init(spe_args)

    def specific_init(self, args):
        pass


class Photon(Particle):
    color_table = {1:'red2', 2:'darkorange', 3:'yellow', 4:'green', 5:'cyan2', 6:'blue', 7:'purple'}
    def specific_init(self, args):
        self.color_n = random.randint(1, 7)

    def update_pos():
        self.pos.move_ip(*self.vel)

