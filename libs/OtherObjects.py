import pygame as pg
from pygame.math import Vector2 as vec2

__all__ = ['PureText', 'Score', 'CountDown', 'Medal', 'MedalStatusBar', 'Ground']


class PureText():
    def __init__(self, text, size, color, font=None, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.font = pg.font.SysFont(font, size)
        self.text_surface = self.font.render(text, True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)







class Score():
    score_number = 0

    def __init__(self, size, color, font=None, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.font = pg.font.SysFont(font, size)
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))
        self.pos_rect = self.text_surface.get_rect(**pos)

    def update(self, increment):
        self.score_number += increment
        self.text_surface = self.font.render(f'Score  {self.score_number:{0}{4}}', True, pg.Color(self.color))

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class CountDown():
    def __init__(self, time_remain, size, color, font=None, **pos):
        """
        time_remain: in second
        pos: refer to the attributes of pg.Rect
        """
        self.color = color
        self.time_remain = time_remain
        self.font = pg.font.SysFont(font, size)
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
    color = 'gray77'
    velocity = vec2(2, 0)

    def __init__(self):
        self.pos_rect = pg.Rect(0, 0, 70, 10)
        self.pos_rect.center = (400, 600 - 60)

    count_down = 0
    def set_highlight(self):
        self.count_down = 5

    def update(self, deltax):
        self.pos_rect.center += deltax * self.velocity
        if self.pos_rect.centerx < 50:  self.pos_rect.centerx = 50
        if self.pos_rect.centerx > 750: self.pos_rect.centerx = 750

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color(self.color), self.pos_rect)
        if self.count_down > 0:
            pg.draw.rect(screen, pg.Color('yellow'), self.pos_rect, 5)
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

    def __init__(self, centerx):
        self.pos_rect = pg.Rect(0, 0, 50, 40)
        self.pos_rect.midbottom = (centerx, 600 - 30)

    def draw(self, screen):
        pg.draw.rect(screen, pg.Color(self.color), self.pos_rect)



