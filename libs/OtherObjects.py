'''
    After modifying this module, please run generate_background_image.py to
    generate new background images.
'''
import pygame as pg
from pygame.math import Vector2 as vec2

__all__ = [
    'PureText',
    'Timer',
    'FlashingText',
    'FlashingImage',
    'Score',
    'CountDown',
    'Metal',
    'MetalStatusBar',
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
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.font = pg.font.Font(default_font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)








class Timer():
    def __init__(self):
        self.prev_time = pg.time.get_ticks()

    def dt(self):
        current_time = pg.time.get_ticks()
        dt = current_time - self.prev_time
        self.prev_time = current_time
        return dt / 1000









class FlashingText(PureText):
    def __init__(self, text, size, color, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        super().__init__(text, size, color, **pos)
        self.timer = Timer()
        self.time_sum = 0.

    def update(self):
        self.time_sum += self.timer.dt()
        if self.time_sum >= default_flashing_period: self.time_sum -= default_flashing_period

    def draw(self, screen):
        if self.time_sum < default_flashing_period / 2:
            screen.blit(self.text_surface, self.pos_rect)








class FlashingImage():
    def __init__(self, image, flashing_period=default_flashing_period, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.image = image
        self.pos_rect = self.image.get_rect(**pos)
        self.timer = Timer()
        self.flashing_period = flashing_period
        self.time_sum = 0.

    def update(self):
        self.time_sum += self.timer.dt()
        if self.time_sum >= self.flashing_period: self.time_sum -= self.flashing_period

    def draw(self, screen):
        if self.time_sum < self.flashing_period / 2:
            screen.blit(self.image, self.pos_rect)









class Score():
    def __init__(self, size, color, **pos):
        '''
        pos: refer to the attributes of pg.Rect
        '''
        self.color = color
        self.score_number = 0
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
        '''
        time_remain: in second
        pos: refer to the attributes of pg.Rect
        '''
        self.color = color
        self.time_remain = time_remain
        self.font = pg.font.Font(default_font, countdown_font_size)
        self.text_surface = self.font.render(f'{self.time_remain // 60}:{self.time_remain % 60:02}', True, pg.Color(self.color))
        self.pos_rect = self.text_surface.get_rect(**pos)
        self.time_end = pg.time.get_ticks() + self.time_remain * 1000

    def update(self):
        self.time_remain = int((self.time_end - pg.time.get_ticks()) / 1000)
        if self.time_remain < 0: self.time_remain = 0
        self.text_surface = self.font.render(f'{self.time_remain // 60}:{self.time_remain % 60:02}', True, pg.Color(self.color))

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class Metal():
    def __init__(self, mask_num, **pos):
        image_name = ['normal', 'activate', 'ground']
        self.images = []
        for i in range(3):
            self.images.append(
                scaled_surface(pg.image.load(os.path.join(data_path, 'Metal', f'{image_name[i]}.png')), 0.28)
            )
            self.images[i].set_masks(masks[mask_num])
        self.pos_rect = self.images[0].get_rect(**pos)
        self.centerx = self.pos_rect.centerx
        self.collision_rect = pg.Rect(self.pos_rect)
        self.collision_rect.height = 9
        self.timer = Timer()
        self.to_draw = 0
        self.connect_ground = False
        self.time_end = 0

    def set_highlight(self):
        self.time_end = pg.time.get_ticks() + metal_highlight_time

    def set_ground(self):
        self.connect_ground = True

    def update(self, direction):
        self.centerx += direction * velocity_of_metal * self.timer.dt()
        self.pos_rect.centerx = self.centerx
        if self.pos_rect.centerx < 50:  self.pos_rect.centerx = 50
        if self.pos_rect.centerx > 750: self.pos_rect.centerx = 750
        self.collision_rect.centerx = self.pos_rect.centerx

        # image to draw
        if self.connect_ground:
            self.to_draw = 2
        elif pg.time.get_ticks() + metal_highlight_time > self.time_end:
            self.to_draw = 0
        else:
            self.to_draw = 1

        self.connect_ground = False

    def draw(self, screen):
        screen.blit(self.images[self.to_draw], self.pos_rect)





class MetalStatusBar():
    color = ['green', 'yellow', 'darkorange', 'red2']

    def __init__(self, center):
        self.border = pg.Rect(0, 0, 20, 200)
        self.border.center = center
        self.charge_bar = []
        self.charge = 0 # electric charge: [0, 200]
        height = [60, 120, 160, 200]
        for i in range(4):
            rect = self.border.copy()
            rect.height = height[i]
            rect.bottom = self.border.bottom
            self.charge_bar.append(rect)
        self.text2 = PureText('Status', 25, 'gray90', midbottom=self.border.midtop)
        self.text1 = PureText('Metal', 25, 'gray90', midbottom=self.text2.pos_rect.midtop)

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

