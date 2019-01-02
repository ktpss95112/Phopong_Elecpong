import pygame as pg

__all__ = ['scaled_surface']

def scaled_surface(surface, scale):
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
