'''
    After modifying this module, please run generate_background_image.py to
    generate new background images.
'''
import pygame as pg

def scaled_surface(surface, scale):
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))
