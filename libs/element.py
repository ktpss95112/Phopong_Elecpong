import pygame as pg
import random

random.seed()

class Particle():
    """
    Particles.pos -> pg.Rect
    Particles.vel -> pygame.math.Vector2
    """
    radius = 10
    def __init__(self, center_position, velocity, spe_args=None):
        self.pos = pg.Rect(0, 0, self.radius, self.radius)
        self.pos.center = center_position
        self.vel = velocity
        self.specific_init(spe_args)

    def specific_init(self, args):
        pass

    def update_pos(self):
        self.pos.center += self.vel

    def collide_with(self, rect):
        return self.pos.colliderect(rect)

    def inside(self, rect):
        return rect.contains(self.pos)




class Photon(Particle):
    color_table = {1:'red2', 2:'darkorange', 3:'yellow', 4:'green', 5:'cyan2', 6:'blue', 7:'purple'}
    def specific_init(self, args):
        self.color_n = random.randint(1, 7)
        self.color = self.color_table[self.color_n]







class Electron(Particle):
    def specific_init(self, args):
        pass

