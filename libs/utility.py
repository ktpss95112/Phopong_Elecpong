import pygame as pg

def scaled_surface(surface, scale):
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
