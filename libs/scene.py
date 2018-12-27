import pygame as pg
from pygame.math import Vector2 as vec2
import element
from OtherObjects import *


def startWithScene(s):
    screen = pg.display.set_mode((800, 600))
    clock = pg.time.Clock()

    current_scene = s

    while current_scene != None:
        pressed_keys = pg.key.get_pressed()
        filtered_events = []
        for event in pg.event.get():
            quit_attempt = False
            if event.type == pg.QUIT:
                quit_attempt = True
            elif event.type == pg.KEYDOWN:
                alt_pressed = pressed_keys[pg.K_LALT] or \
                              pressed_keys[pg.K_RALT]
                if event.key == pg.K_F4 and alt_pressed:
                    quit_attempt = True
            
            if quit_attempt: current_scene.Terminate()
            else:            filtered_events.append(event)

        current_scene.ProcessInput(filtered_events, pressed_keys)
        current_scene.Update()
        current_scene.Render(screen)

        current_scene = current_scene.next

        pg.display.flip()
        clock.tick(60)









class SceneBase:
    line_of_horizon = 600 - 40
    horizon_rect = pg.Rect(0, line_of_horizon, 800, 600 - line_of_horizon)

    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def Update(self):
        print("uh-oh, you didn't override this in the child class")

    def Render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)








class TitleScene(SceneBase):
    user_focus = 0 # 0: start, 1: help, 2: exit
    enter_pressed = False

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN: self.user_focus += 1
                if event.key == pg.K_UP:   self.user_focus -= 1
                if self.user_focus < 0: self.user_focus = 0
                if self.user_focus > 2: self.user_focus = 2

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.enter_pressed = True

    def Update(self):
        if self.enter_pressed:
            if self.user_focus == 0: self.SwitchToScene(LevelSelectScene())
            if self.user_focus == 1: self.SwitchToScene(HelpScene())
            if self.user_focus == 2: self.Terminate()
            self.enter_pressed = False

    def Render(self, screen):
        screen.fill(pg.Color('black'))
        # TODO: background

        # title
        title_text = PureText('Title Here', 150, 'white', center=(400, 180))
        title_text.draw(screen)

        # options
        base_pos_y, delta_y = 315, 60
        start_text = PureText('Start', 50, 'white', center=(400, base_pos_y))
        help_text = PureText('Help', 50, 'white', center=(400, base_pos_y + delta_y))
        exit_text = PureText('Exit', 50, 'white', center=(400, base_pos_y + 2 * delta_y))
        start_text.draw(screen)
        help_text.draw(screen)
        exit_text.draw(screen)

        # focus buttom
        focus_rect = pg.Rect(0, 0, 15, 15)
        focus_rect.center = (330, base_pos_y + self.user_focus * delta_y)
        pg.draw.rect(screen, pg.Color('pink'), focus_rect)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)








class LevelSelectScene(SceneBase):
    # [0]: 0->level, 1->mode
    # [1]: 0->classic, 1->classic(advanced), 2->circle
    user_focus = [0, 0]
    level = 1
    enter_pressed = False
    up_down_pressed = 0 # -1: down, 0: not, 1: up
    number_of_mode = 3

    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT: self.user_focus[0] += 1
                if event.key == pg.K_LEFT:  self.user_focus[0] -= 1
                if self.user_focus[0] < 0:  self.user_focus[0] = 0
                if self.user_focus[0] > 1:  self.user_focus[0] = 1

                if event.key == pg.K_UP:   self.up_down_pressed = 1
                if event.key == pg.K_DOWN: self.up_down_pressed = -1

            elif event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.enter_pressed = True
        
    def Update(self):
        if self.user_focus[0] == 0:
            self.level = (self.level - 1 + self.up_down_pressed + 7) % 7 + 1
            self.up_down_pressed = 0
            self.enter_pressed = False
        if self.user_focus[0] == 1:
            self.user_focus[1] -= self.up_down_pressed
            if self.user_focus[1] < 0: self.user_focus[1] = 0
            if self.user_focus[1] >= self.number_of_mode: self.user_focus[1] = self.number_of_mode - 1
            self.up_down_pressed = 0
            if self.enter_pressed:
                if self.user_focus[1] == 0:
                    self.SwitchToScene(ClassicGameScene(self.level, False))
                if self.user_focus[1] == 1:
                    self.SwitchToScene(ClassicGameScene(self.level, True))
                if self.user_focus[1] == 2:
                    self.SwitchToScene(CircleGameScene(self.level))
    
    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # title
        title_level_text = PureText('Level', 150, 'white', center=(200, 150))
        title_mode_text = PureText('Mode', 150, 'white', center=(570, 150))
        title_level_text.draw(screen)
        title_mode_text.draw(screen)
        
        # level selection
        level_selection_text = PureText(f'{self.level}', 80, 'white', center=(200, 380))
        level_selection_text.draw(screen)
        # TODO: add little triangle above and below the rect

        # mode selection
        modes = ['Classic', 'Classic (advanced)', 'Circle']
        base_pos_y, delta_y = 330, 65
        for i in range(self.number_of_mode):
            mode_text = PureText(modes[i], 50, 'white', center=(570, base_pos_y + i * delta_y))
            mode_text.draw(screen)

        # focus
        if self.user_focus[0] == 0:
            pg.draw.rect(screen, pg.Color('red'), pg.Rect(level_selection_text.pos_rect).inflate(35, 35).move(0, -3), 5)
        if self.user_focus[0] == 1:
            mode_focus_rect = pg.Rect(0, 0, 340, 50)
            mode_focus_rect.center = (570, base_pos_y + delta_y * self.user_focus[1])
            pg.draw.rect(screen, pg.Color('red'), mode_focus_rect, 5)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)

        # TODO:
        # image to give hint of press enter
        # highlight when focus is on modes, and vice versa









class HelpScene(SceneBase):
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # title
        title_text = PureText('Help Title', 150, 'white', center=(400, 150))
        title_text.draw(screen)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)











class ClassicGameScene(SceneBase):
    photons = []
    photons_per_line = 7 # should be odd number
    electrons = []
    photon_distance = 80
    velocity_of_photon = vec2(0, 2)
    medal_rect = pg.Rect(0, 0, 70, 10)
    medal_rect.center = (400, 600 - 60)
    velocity_of_medal = vec2(2, 0)
    electron_valid_rect = pg.Rect(0, 400, 800, 200)

    def new_photons(self):
        # parameters: center_pos, vel
        return [ element.Photon((400 + self.photon_distance * i, 0), self.velocity_of_photon)\
            for i in range(-self.photons_per_line//2+1, self.photons_per_line//2+1) ]

    def __init__(self, level, ground_enabled):
        self.next = self
        self.level = level # 1:easy, 7:hard
        self.ground_enabled = ground_enabled
        self.photons.append(self.new_photons())
        self.score = Score(70, 'pink', topright=(800 - 20, 20))

    def generate_electron(self, pos, vel):
        # pos -> pg.Rect()
        self.electrons.append(element.Electron(pos, vel))


    left_right_pressed = 0 # {-1, 0, 1}
    space_pressed = False
    def ProcessInput(self, events, pressed_keys):
        if pressed_keys[pg.K_LEFT]:  self.left_right_pressed -= 1
        if pressed_keys[pg.K_RIGHT]: self.left_right_pressed += 1

        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.space_pressed = True
        
    def Update(self):
        # update medal position
        self.medal_rect.center += self.left_right_pressed * self.velocity_of_medal
        self.left_right_pressed = 0
        if self.medal_rect.centerx < 50:  self.medal_rect.centerx = 50
        if self.medal_rect.centerx > 750: self.medal_rect.centerx = 750

        # update photon position
        for sub_photons in self.photons:
            for photon in sub_photons:
                photon.update_pos()

        # generate next_photons
        if self.photons[-1][0].pos.centery >= self.photon_distance:
            self.photons.append(self.new_photons())

        # update electron position
        for electron in self.electrons:
            electron.update_pos()
            if not electron.inside(self.electron_valid_rect):
                self.electrons.remove(electron)

        # photon collision handle
        for photon in self.photons[0]:
            if photon.inside(self.horizon_rect):
                self.photons[0].remove(photon)
            elif photon.collide_with(self.medal_rect):
                self.score.update(5 * photon.color_n)
                if photon.color_n >= self.level:
                    self.generate_electron(photon.pos.center, vec2(0, -photon.color_n))
                self.photons[0].remove(photon)
        if not self.photons[0]:
            del self.photons[0]
    
    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # photons & electrons
        for sub_photons in self.photons:
            for photon in sub_photons:
                pg.draw.rect(screen, pg.Color(photon.color), photon.pos)
        for electron in self.electrons:
            pg.draw.rect(screen, pg.Color('gray40'), electron.pos)

        # horizon & medal
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)
        pg.draw.rect(screen, pg.Color('gray77'), self.medal_rect)

        # score
        self.score.draw(screen)








class CircleGameScene(SceneBase):
    def __init__(self, level):
        self.next = self
        self.level = level

    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill(pg.Color('pink'))







if __name__ == '__main__':
    pg.init()
    #startWithScene(TitleScene())
    #startWithScene(LevelSelectScene())
    startWithScene(ClassicGameScene(4, True))
