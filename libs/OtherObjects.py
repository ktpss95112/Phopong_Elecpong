import pygame as pg

__all__ = ['PureText', 'ScoreNumber', 'MedalStatusBar']


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





class ScoreNumber():
    score_number = 0

    def __init__(self, size, color, font=None, **pos):
        """
        pos: refer to the attributes of pg.Rect
        """
        self.font = pg.font.SysFont(font, size)
        self.text_surface = font.render(f'{self.score_number:{0}{4}}', True, pg.Color(color))
        self.pos_rect = self.text_surface.get_rect(pos)

    def update(self, increment):
        self.score_number += increment

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos_rect)





class MedalStatusBar():
    # electric charge: [0, 50]
    charge = 0
    valid_charge = range(0, 51)
    # TODO: right now the status bar is only single-colored, make it like
    # spectrum in the future


    def __init__(self, **pos):
        #self.pos_rect = pg.Rect(0, 0, )
        #for key in pos:
        #    eval(f'self.pos_rect.{key} = {pos[key]}')
        pass

    def update(self):
        pass

    def draw(self):
        pass


