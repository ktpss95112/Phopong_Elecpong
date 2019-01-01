import pygame as pg
from pygame.math import Vector2 as vec2

import os.path
if __name__ == '__main__':
    import element
    from OtherObjects import *
    data_path = os.path.join('..', 'data')
else:
    import libs.element as element
    from libs.OtherObjects import *
    data_path = 'data'


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
        for i in (1, 2):
            image = pg.image.load(os.path.join(data_path, 'Title', f'title_{i}.png'))
            scale = 0.8
            image = pg.transform.smoothscale(image, (int(scale * image.get_width()), int(scale * image.get_height())))
            screen.blit(image, image.get_rect(center=(400, i * 100)))


        # options
        base_pos_y, delta_y = 330, 55
        start_text = PureText('Start', 55, 'white', center=(400, base_pos_y))
        help_text = PureText('Help', 55, 'white', center=(400, base_pos_y + delta_y))
        exit_text = PureText('Exit', 55, 'white', center=(400, base_pos_y + 2 * delta_y))
        start_text.draw(screen)
        help_text.draw(screen)
        exit_text.draw(screen)

        # focus buttom
        focus_rect = pg.Rect(0, 0, 15, 15)
        focus_rect.center = (330, base_pos_y + self.user_focus * delta_y)
        pg.draw.rect(screen, pg.Color('red'), focus_rect)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)











class HelpScene(SceneBase):
    def __init__(self):
        self.next = self
        self.flashing_text = FlashingText('Press "Enter" or "Space" To Go Back ...', 40, 'gray77', center=(400, 480))

    enter_pressed = False
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.enter_pressed = True

    def Update(self):
        if self.enter_pressed: self.SwitchToScene(TitleScene())
        self.flashing_text.update()

    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # title
        title_text = PureText('Help Title', 150, 'white', center=(400, 150))
        title_text.draw(screen)

        # content
        base_pos_y, delta_y = 260, 30
        for i in range(5):
            content_text = PureText('contents here contents here', 35, 'gray77', center=(250, base_pos_y + i * delta_y))
            content_text.draw(screen)

        # keyboard image
        image = PureText('image', 80, 'gray77', center=(600, 330))
        image.draw(screen)

        # 'press enter space to continue'
        # TODO: replace text 'enter' with image, same as 'space'
        self.flashing_text.draw(screen)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)










class LevelSelectScene(SceneBase):
    # [0]: 0->level, 1->mode
    # [1]: 0->classic, 1->advanced
    user_focus = [0, 0]
    level = 1
    enter_pressed = False
    esc_pressed = False
    up_down_pressed = 0 # -1: down, 0: not, 1: up

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
                if event.key == pg.K_ESCAPE:
                    self.esc_pressed = True

    def Update(self):
        if self.user_focus[0] == 0:
            self.level = (self.level - 1 + self.up_down_pressed + 7) % 7 + 1
            self.up_down_pressed = 0
            self.enter_pressed = False
        if self.user_focus[0] == 1:
            self.user_focus[1] -= self.up_down_pressed
            if self.user_focus[1] < 0: self.user_focus[1] = 0
            if self.user_focus[1] > 1: self.user_focus[1] = 1
            self.up_down_pressed = 0
            if self.enter_pressed:
                if self.user_focus[1] == 0:
                    self.SwitchToScene(ClassicGameScene(self.level, False))
                if self.user_focus[1] == 1:
                    self.SwitchToScene(ClassicGameScene(self.level, True))
        if self.esc_pressed:
            self.SwitchToScene(TitleScene())

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
        up_buttom = PureText('up buttom here', 30, 'gray40', center=(200, 300))
        up_buttom.draw(screen)
        down_buttom = PureText('down buttom here', 30, 'gray40', center=(200, 460))
        down_buttom.draw(screen)

        # mode selection
        modes = ['Classic', 'Advanced']
        base_pos_y, delta_y = 330, 65
        for i in range(len(modes)):
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










class GameBridgeScene(SceneBase):
    pass











class ClassicGameScene(SceneBase):
    photons_per_line = 7 # should be odd number
    photon_distance = 80
    velocity_of_photon = vec2(0, 2)
    electron_valid_rect = pg.Rect(0, 400, 800, 200)

    def new_photons(self):
        # parameters: center_pos, vel
        return [ element.Photon((400 + self.photon_distance * i, 0), self.velocity_of_photon)\
            for i in range(-self.photons_per_line//2+1, self.photons_per_line//2+1) ]

    def __init__(self, level, charge_enabled):
        self.next = self
        self.level = level # 1:easy, 7:hard
        self.charge_enabled = charge_enabled
        self.photons = []
        self.electrons = []
        self.time_remain = 31
        self.photons.append(self.new_photons())
        self.score = Score(60, 'pink', topright=(800 - 15, 15))
        self.medal = Medal()
        self.medal_status = MedalStatusBar((800 - 15, 280))
        self.ground = Ground()
        self.countdown = CountDown(self.time_remain, 60, 'pink', topleft=(15, 15))
        self.countdown.start_tick()
        line_of_horizon2 = 600 - 30
        self.horizon_rect2 = pg.Rect(0, line_of_horizon2, 800, 600 - line_of_horizon2)


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
        self.medal.update(self.left_right_pressed)
        self.left_right_pressed = 0

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
            if photon.inside(self.horizon_rect2):
                self.photons[0].remove(photon)
            elif photon.collide_with(self.medal.collision_rect):
                increment = 0
                if (not self.charge_enabled) and photon.color_n >= self.level:
                    increment = photon.color_n
                elif self.charge_enabled and photon.color_n >= self.level:
                    increment = photon.color_n * (1 - self.medal_status.charge / 100)

                if increment != 0:
                    self.medal.set_highlight()
                    self.score.update(int(5 * increment))
                    self.medal_status.update(photon.color_n)
                    self.generate_electron(photon.pos.center, vec2(0, -increment))

                self.photons[0].remove(photon)
        if not self.photons[0]:
            del self.photons[0]

        # ground (recharge)
        # TODO: change color when charging
        if self.medal.pos_rect.collidelist([ self.ground.pos_rect_l, self.ground.pos_rect_r ]) != -1:
            self.medal_status.update(-5)

        # update timer
        self.countdown.update()

    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)

        # photons & electrons
        for sub_photons in self.photons:
            for photon in sub_photons:
                photon.draw(screen)
        for electron in self.electrons:
            electron.draw(screen)

        # horizon 2
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect2)

        # ground
        self.ground.draw(screen)

        # medal
        self.medal.draw(screen)

        # time remain
        self.countdown.draw(screen)

        # score
        self.score.draw(screen)

        # medal status
        if self.charge_enabled:
            self.medal_status.draw(screen)

        # time's up!
        if self.countdown.time_remain == 0: self.SwitchToScene(EndBridgeScene(self.score.score_number, screen))








class EndBridgeScene(SceneBase):
    time_duration = 4.7

    def __init__(self, score, screen):
        """
        score: int
        """
        self.next = self
        self.score = score
        self.freezed_screen = screen.copy()
        # parameters excluding time_remain is arbitrary
        self.countdown = CountDown(self.time_duration, 0, 'black', center=(0, 0))
        self.countdown.start_tick()
        self.times_up_text = FlashingText('TIME\'S UP!!!', 120, 'violetred', center=(400, 280))

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        self.times_up_text.update()
        self.countdown.update()
        if self.countdown.time_remain == 0: self.SwitchToScene(EndScene(self.score))

    def Render(self, screen):
        screen.blit(self.freezed_screen, self.freezed_screen.get_rect())

        # time's up
        self.times_up_text.draw(screen)









class EndScene(SceneBase):
    user_focus = 0
    enter_pressed = False

    def __init__(self, score):
        """
        score: int
        """
        self.next = self
        self.score = score

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
            if self.user_focus == 1: self.SwitchToScene(TitleScene())
            if self.user_focus == 2: self.Terminate()
            self.enter_pressed = False


    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # score
        score_text = PureText('Score:', 80, 'pink', topright=(250+40, 60+20))
        score_text.draw(screen)
        score_number = PureText(f'{self.score:05}', 70, 'pink', topright=(240+40, 130+20))
        score_number.draw(screen)

        # animation
        animation = PureText('animation here', 40, 'gray40', center=(230, 400))
        animation.draw(screen)

        # options
        options = ['Again', 'Homepage', 'Exit']
        base_pos_y, delta_y = 300, 55
        for i in range(len(options)):
            option_text = PureText(options[i], 50, 'white', midleft=(550, base_pos_y + i * delta_y))
            option_text.draw(screen)

        # focus buttom
        focus_rect = pg.Rect(0, 0, 15, 15)
        focus_rect.center = (530, base_pos_y + self.user_focus * delta_y)
        pg.draw.rect(screen, pg.Color('red'), focus_rect)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)







if __name__ == '__main__':
    pg.init()
    #startWithScene(TitleScene())
    #startWithScene(HelpScene())
    #startWithScene(LevelSelectScene())
    startWithScene(ClassicGameScene(1, True))
    #startWithScene(EndScene(150))
