"""
    After modifying this module, please run generate_background_image.py to
    generate new background images.
"""
import pygame as pg
from pygame.math import Vector2 as vec2

__all__ = [
    'PureText',
    'FlashingText',
    'FlashingImage',
    'Score',
    'CountDown',
    'Medal',
    'MedalStatusBar',
    'Ground',
    'EndAnimation',
]

import os.path
if 'libs' in __name__:
    from libs.GlobalParameters import *
    from libs.utility import *
else:
    from GlobalParameters import *
    from utility import *



class PureText():
    def __init__(self, text, size, color, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.font = pg.font.Font(default_font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)








class FlashingText(PureText):
    def __init__(self, text, size, color, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        super().__init__(text, size, color, **pos)
        self.time_count = 0

    def update(self):
        self.time_count = (self.time_count + 1) % flashing_period

    def draw(self, screen):
        if self.time_count < flashing_period // 2:
            screen.blit(self.text_surface, self.pos_rect)








class FlashingImage():
    def __init__(self, image, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.image = image
        self.pos_rect = self.image.get_rect(**pos)
        self.time_count = 0

    def update(self):
        self.time_count = (self.time_count + 1) % flashing_period

    def draw(self, screen):
        if self.time_count < flashing_period // 2:
            screen.blit(self.image, self.pos_rect)









class Score():
    score_number = 0

    def __init__(self, size, color, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.font = pg.font.Font(default_font, size)
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def update(self, increment):
        self.score_number += increment
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class CountDown():
    def __init__(self, time_remain, color, **pos):
        """
        time_remain: in second
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.time_remain = time_remain
        self.font = pg.font.Font(default_font, countdown_font_size)
        self.text_surface = self.font.render(f'{self.time_remain // 60}:{self.time_remain % 60:02}', True, pg.Color(self.color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def start_tick(self):
        self.time_end = pg.time.get_ticks() + self.time_remain * 1000

    def update(self):
        self.time_remain = int((self.time_end - pg.time.get_ticks()) / 1000)
        if self.time_remain < 0: self.time_remain = 0
        self.text_surface = self.font.render(f'{self.time_remain // 60}:{self.time_remain % 60:02}', True, pg.Color(self.color))

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class Medal():
    velocity = vec2(2, 0)

    def __init__(self):
        image_name = ['normal', 'activate', 'ground']
        self.images = []
        for i in range(3):
            self.images.append(
                scaled_surface(pg.image.load(os.path.join(data_path, 'Medal', f'{image_name[i]}.png')), 0.28)
            )
        self.pos_rect = self.images[0].get_rect(center=(400, 600 - 60))
        self.collision_rect = pg.Rect(self.pos_rect)
        self.collision_rect.height = 9
        self.to_draw = 0

    count_down = 0
    def set_highlight(self):
        self.count_down = 5

    connect_ground = False
    def set_ground(self):
        self.connect_ground = True

    def update(self, deltax):
        self.pos_rect.center += deltax * self.velocity
        if self.pos_rect.centerx < 50:  self.pos_rect.centerx = 50
        if self.pos_rect.centerx > 750: self.pos_rect.centerx = 750
        self.collision_rect.centerx = self.pos_rect.centerx

        # image to draw
        if self.connect_ground:
            self.to_draw = 2
        elif self.count_down == 0:
            self.to_draw = 0
        else:
            self.to_draw = 1
            self.count_down -= 1

        self.connect_ground = False

    def draw(self, screen):
        screen.blit(self.images[self.to_draw], self.pos_rect)





class MedalStatusBar():
    # electric charge: [0, 100]
    charge = 0
    color = ['green', 'yellow', 'darkorange', 'red2']

    def __init__(self, center):
        self.border = pg.Rect(0, 0, 20, 200)
        self.border.center = center
        self.charge_bar = []
        height = [60, 120, 160, 200]
        for i in range(4):
            rect = self.border.copy()
            rect.height = height[i]
            rect.bottom = self.border.bottom
            self.charge_bar.append(rect)
        self.text2 = PureText('Status', 25, 'gray90', midbottom=self.border.midtop)
        self.text1 = PureText('Medal', 25, 'gray90', midbottom=self.text2.pos_rect.midtop)

    def update(self, increment):
        self.charge += increment
        if self.charge < 0:   self.charge = 0
        if self.charge > 200: self.charge = 200

    def draw(self, screen):
        # draw all rects
        for i in range(4)[::-1]:
            pg.draw.rect(screen, pg.Color(self.color[i]), self.charge_bar[i])

        # block
        block = self.border.copy()
        block.height = 200 - self.charge
        pg.draw.rect(screen, pg.Color('black'), block)

        # draw border and text
        pg.draw.rect(screen, pg.Color('gray20'), self.border, 2)
        self.text1.draw(screen)
        self.text2.draw(screen)








class Ground():
    def __init__(self):
        self.ground_l = scaled_surface(pg.image.load(os.path.join(data_path, 'ground.png')), 0.6)
        self.ground_r = pg.transform.flip(self.ground_l, True, False)
        self.pos_rect_l = self.ground_l.get_rect(bottomleft=(0, 600 - 30))
        self.pos_rect_r = self.ground_r.get_rect(bottomright=(800, 600 - 30))

    def draw(self, screen):
        screen.blit(self.ground_l, self.pos_rect_l)
        screen.blit(self.ground_r, self.pos_rect_r)








class EndAnimation():
    frames = [
        scaled_surface(pg.image.load(os.path.join(data_path, 'EndSceneAnimation', f'{i}.png')), 0.5)
        for i in range(4)
    ]

    def __init__(self, **pos):
        self.clock = 0
        self.current_frame = 0
        self.pos_rect = self.frames[0].get_rect(**pos)

    deltat = 10
    def update(self):
        self.clock += 1
        if self.clock % self.deltat == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], self.pos_rect)

