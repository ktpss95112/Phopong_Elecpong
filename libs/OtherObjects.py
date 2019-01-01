import pygame as pg
from pygame.math import Vector2 as vec2

__all__ = ['PureText', 'FlashingText', 'Score', 'CountDown', 'Medal', 'MedalStatusBar', 'Ground']

import os.path
if 'libs' in __name__:
    data_path = 'data'
else:
    data_path = os.path.join('..', 'data')

#default_font = 'JACKEYFONT.ttf'
default_font = 'VT323-Regular.ttf'
#default_font = 'ocr-aregular.ttf'

def scaled_surface(surface, scale):
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))




class PureText():
    def __init__(self, text, size, color, font=default_font, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.font = pg.font.Font(os.path.join(data_path, font), size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)








class FlashingText(PureText):
    period = 80

    def __init__(self, text, size, color, font=default_font, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        super().__init__(text, size, color, font, **pos)
        self.time_count = 0

    def update(self):
        self.time_count = (self.time_count + 1) % self.period

    def draw(self, screen):
        if self.time_count < self.period // 2:
            screen.blit(self.text_surface, self.pos_rect)








class Score():
    score_number = 0

    def __init__(self, size, color, font=default_font, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.font = pg.font.Font(os.path.join(data_path, font), size)
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def update(self, increment):
        self.score_number += increment
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class CountDown():
    def __init__(self, time_remain, size, color, font=default_font, **pos):
        """
        time_remain: in second
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.time_remain = time_remain
        self.font = pg.font.Font(os.path.join(data_path, font), size)
        self.text_surface = self.font.render('0:00', True, pg.Color(self.color))
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
        self.normal = scaled_surface(pg.image.load(os.path.join(data_path, 'Medal', 'normal.png')), 0.3)
        self.ground = scaled_surface(pg.image.load(os.path.join(data_path, 'Medal', 'ground.png')), 0.3)
        self.activate = scaled_surface(pg.image.load(os.path.join(data_path, 'Medal', 'activate.png')), 0.3)
        self.pos_rect = self.normal.get_rect(center=(400, 600 - 60))
        self.collision_rect = pg.Rect(self.pos_rect)
        self.collision_rect.height = 9

    count_down = 0
    def set_highlight(self):
        self.count_down = 5

    def update(self, deltax):
        self.pos_rect.center += deltax * self.velocity
        if self.pos_rect.centerx < 50:  self.pos_rect.centerx = 50
        if self.pos_rect.centerx > 750: self.pos_rect.centerx = 750
        self.collision_rect.centerx = self.pos_rect.centerx

    def draw(self, screen):
        if self.count_down == 0:
            screen.blit(self.normal, self.pos_rect)
        else:
            screen.blit(self.activate, self.pos_rect)
            self.count_down -= 1





class MedalStatusBar():
    # electric charge: [0, 100]
    charge = 0
    # TODO: right now the status bar is only single-colored, make it like
    # spectrum in the future

    def __init__(self, center):
        self.border = pg.Rect(0, 0, 20, 100)
        self.border.center = center

    def update(self, increment):
        self.charge += increment
        if self.charge < 0:   self.charge = 0
        if self.charge > 100: self.charge = 100

    def draw(self, screen):
        charge_rect = pg.Rect(0, 0, 20, self.charge)
        charge_rect.bottomleft = self.border.bottomleft
        pg.draw.rect(screen, pg.Color('pink'), charge_rect)
        pg.draw.rect(screen, pg.Color('gray20'), self.border, 2)







class Ground():
    color = 'white'

    def __init__(self):
        self.ground_l = scaled_surface(pg.image.load(os.path.join(data_path, 'ground.png')), 0.5)
        self.ground_r = pg.transform.flip(self.ground_l, True, False)
        self.pos_rect_l = self.ground_l.get_rect(bottomleft=(0, 600 - 38))
        self.pos_rect_r = self.ground_r.get_rect(bottomright=(800, 600 - 38))
        #self.pos_rect = pg.Rect(0, 0, 50, 40)
        #self.pos_rect.midbottom = (centerx, 600 - 30)

    def draw(self, screen):
        screen.blit(self.ground_l, self.pos_rect_l)
        screen.blit(self.ground_r, self.pos_rect_r)
        #pg.draw.rect(screen, pg.Color(self.color), self.pos_rect)



