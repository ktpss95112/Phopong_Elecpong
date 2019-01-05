'''
    After modifying this module, please run generate_background_image.py to
    generate new background images.
'''
from pygame.math import Vector2 as vec2
import os.path
if 'libs' in __name__:
    data_path = 'data'
else:
    data_path = os.path.join('..', 'data')

default_font = os.path.join(data_path, 'VT323-Regular.ttf')

# time
default_flashing_period = 1
game_time = 31
game_bridge_time = 1.99 * 1000
end_bridge_time = 2.9 * 1000
metal_highlight_time = 0.3

# objects
line_of_horizon2 = 600 - 30
photon_distance = 80
photons_per_line = 7 # should be odd number
velocity_of_photon = vec2(0, 2)
velocity_of_metal = 100

# font size
title_font_size = 150
options_font_size = 55
mode_font_size = 40
help_font_size = 35
score_font_size = 57
countdown_font_size = 70
motto_font_size = 20


masks = [
    (255, 65280, 16711680, 4278190080),
    (255, 65280,        0, 4278190080),
    (100, 65280, 16711680, 4278190080),
]

mottos = [
    '''\
Two things are infinite: the universe and human
stupidity; and I'm not sure about the universe.
                               -Albert Einstein''',
    '''\
Logic will get you from A to Z; imagination will
get you everywhere.
                                -Albert Einstein''',
    '''\
Life is like riding a bicycle. To keep your
balance, you must keep moving.
                           -Albert Einstein''',
    '''\
Science without religion is lame, religion without
science is blind.
                                  -Albert Einstein''',
    '''\
I have no special talents. I am only passionately curious.
                                        -Albert Einstein''',
]
