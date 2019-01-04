"""
    After modifying this module, please run generate_background_image.py to
    generate new background images.
"""
from pygame.math import Vector2 as vec2
import os.path
if 'libs' in __name__:
    data_path = 'data'
else:
    data_path = os.path.join('..', 'data')

default_font = os.path.join(data_path, 'VT323-Regular.ttf')

flashing_period = 60
game_time = 31
end_bridge_time = 3.6

line_of_horizon2 = 600 - 30
photon_distance = 80
photons_per_line = 7 # should be odd number
velocity_of_photon = vec2(0, 2)

title_font_size = 150
options_font_size = 55
help_font_size = 35
score_font_size = 57
countdown_font_size = 60


