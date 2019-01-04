import pygame as pg
from pygame.math import Vector2 as vec2
import random
random.seed()

import os.path
if __name__ == '__main__':
    import element
    from OtherObjects import *
    from GlobalParameters import *
    from utility import *
else:
    import libs.element as element
    from libs.OtherObjects import *
    from libs.GlobalParameters import *
    from libs.utility import *


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
                alt_pressed = pressed_keys[pg.K_LALT] or pressed_keys[pg.K_RALT]
                ctrl_pressed = pressed_keys[pg.K_LCTRL] or pressed_keys[pg.K_RCTRL]
                if (event.key == pg.K_F4 and alt_pressed) or\
                   (event.key == pg.K_w and ctrl_pressed):
                    quit_attempt = True

            if quit_attempt: current_scene.Terminate()
            else:            filtered_events.append(event)

        current_scene.ProcessInput(filtered_events, pressed_keys)
        current_scene.Update()
        current_scene.Render(screen)

        current_scene = current_scene.next

        #print(clock.get_fps())

        pg.display.flip()
        clock.tick(60)









class SceneBase:
    def __init__(self):
        self.next = self

    def ProcessInput(self, events, pressed_keys):
        print('uh-oh, you didn\'t override this in the child class')

    def Update(self):
        print('uh-oh, you didn\'t override this in the child class')

    def Render(self, screen):
        print('uh-oh, you didn\'t override this in the child class')

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)








class TitleScene(SceneBase):
    # TODO: generate some photons on background
    # TODO: highscore (create a file to store the information)
    user_focus = 0 # 0: start, 1: help, 2: exit
    background_image = pg.image.load(os.path.join(data_path, 'backgrounds', 'title_scene.png'))

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
        screen.blit(self.background_image, self.background_image.get_rect())

        # focus buttom
        base_pos_y, delta_y = 330, 55
        focus_rect = pg.Rect(0, 0, 15, 15)
        focus_rect.center = (330, base_pos_y + self.user_focus * delta_y)
        pg.draw.rect(screen, pg.Color('red'), focus_rect)










class HelpScene(SceneBase):
    background_image1 = pg.image.load(os.path.join(data_path, 'backgrounds', 'help_scene1.png'))
    background_image2 = pg.image.load(os.path.join(data_path, 'backgrounds', 'help_scene2.png'))
    enter_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'enter.png')), 0.3)
    space_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'space.png')), 0.3)

    def __init__(self):
        self.next = self
        self.current_image = 1

        # image1
        self.flashing_enter_buttom = FlashingImage(self.enter_buttom, center=(700, 500))
        self.flashing_items = [self.flashing_enter_buttom]

    enter_pressed = False
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                    self.enter_pressed = True

    def Update(self):
        if self.enter_pressed:
            if self.current_image == 1:
                # image2
                # press enter space to continue
                self.flashing_text = FlashingText('Press     or     to Continue ...', 40, 'gray90', center=(400, 515))

                # enter, space
                self.flashing_enter_buttom = FlashingImage(self.enter_buttom, center=(265, 515))
                self.flashing_space_buttom = FlashingImage(self.space_buttom, center=(375, 515))
                self.current_image = 2
                self.flashing_items = [self.flashing_text, self.flashing_enter_buttom, self.flashing_space_buttom]
                self.enter_pressed = False
            else:
                self.SwitchToScene(TitleScene())

        for item in self.flashing_items:
            item.update()

    def Render(self, screen):
        if self.current_image == 1:
            screen.blit(self.background_image1, self.background_image1.get_rect())
        else:
            screen.blit(self.background_image2, self.background_image2.get_rect())

        for item in self.flashing_items:
            item.draw(screen)










class LevelSelectScene(SceneBase):
    # TODO: generate some photons on background
    background_image = pg.image.load(os.path.join(data_path, 'backgrounds', 'level_scene.png'))

    def __init__(self):
        self.next = self
        self.level = 1
        # [0]: 0->level, 1->mode
        # [1]: 0->classic, 1->advanced, 2->cla(2P), 3->adv(2P)
        self.user_focus = [0, 0]

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
            if self.user_focus[1] > 3: self.user_focus[1] = 3
            self.up_down_pressed = 0
            if self.enter_pressed:
                if self.user_focus[1] == 0:
                    self.SwitchToScene(GameBridgeScene(self.level, 1, False))
                if self.user_focus[1] == 1:
                    self.SwitchToScene(GameBridgeScene(self.level, 1, True))
                if self.user_focus[1] == 2:
                    self.SwitchToScene(GameBridgeScene(self.level, 2, False))
                if self.user_focus[1] == 3:
                    self.SwitchToScene(GameBridgeScene(self.level, 2, True))
        if self.esc_pressed:
            self.SwitchToScene(TitleScene())

    def Render(self, screen):
        screen.blit(self.background_image, self.background_image.get_rect())

        # level selection
        level_selection_text = PureText(f'{self.level}', 80, 'white', center=(230 - 15, 380))
        level_selection_text.draw(screen)

        # focus
        base_pos_y, delta_y = 320, 40
        if self.user_focus[0] == 0:
            pg.draw.rect(screen, pg.Color('red'), pg.Rect(level_selection_text.pos_rect).inflate(35, 10), 5)
        if self.user_focus[0] == 1:
            mode_focus_rect = pg.Rect(0, 0, 350, 45)
            mode_focus_rect.center = (583, base_pos_y + delta_y * self.user_focus[1])
            pg.draw.rect(screen, pg.Color('red'), mode_focus_rect, 4)

        # TODO:
        # image to give hint of press enter
        # highlight when focus is on modes, and vice versa










class GameBridgeScene(SceneBase):
    background_image1 = pg.image.load(os.path.join(data_path, 'backgrounds', 'game_scene(classic).png'))
    background_image2 = pg.image.load(os.path.join(data_path, 'backgrounds', 'game_scene(advanced).png'))
    l_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'left.png')), 0.35)
    r_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'right.png')), 0.35)
    A_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'A.png')), 0.35)
    D_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'D.png')), 0.35)

    def __init__(self, level, num_of_player, charge_enabled):
        self.next = self
        self.level = level
        self.num_of_player = num_of_player
        self.charge_enabled = charge_enabled
        if self.charge_enabled: self.background_image = self.background_image2
        else:                   self.background_image = self.background_image1

        # depend on num_of_player
        if num_of_player == 1:
            self.scores = [ Score(score_font_size, 'pink', topright=(800 - 15, 15)) ]
            self.medals = [ Medal(0, center=(400, 600 - 60)) ]
            self.medal_statuss = [ MedalStatusBar((800 - 35, 300)) ]
            self.countdown = CountDown(game_time, 'pink', topleft=(15, 15))
            self.lr_buttoms = [
                FlashingImage(self.l_buttom, flashing_period=0.5, midright=self.medals[0].pos_rect.midleft),
                FlashingImage(self.r_buttom, flashing_period=0.5, midleft=self.medals[0].pos_rect.midright),
            ]
        else:
            self.scores = [ Score(score_font_size, 'deepskyblue1', topright=(800 - 15, 15)),
                            Score(score_font_size, 'gold1', topleft=(15, 15)) ]
            self.medals = [ Medal(1, center=(400 - 120, 600 - 60)),
                            Medal(2, center=(400 + 120, 600 - 60)) ]
            self.medal_statuss = [ MedalStatusBar(topright=(800 - 15, 15)),
                                   MedalStatusBar(topleft=(15, 15)) ]
            self.countdown = CountDown(game_time, 'pink', midtop=(400, 25))
            self.lr_buttoms = [
                FlashingImage(self.l_buttom, flashing_period=0.5, midright=self.medals[1].pos_rect.midleft),
                FlashingImage(self.r_buttom, flashing_period=0.5, midleft=self.medals[1].pos_rect.midright),
                FlashingImage(self.A_buttom, flashing_period=0.5, midright=self.medals[0].pos_rect.midleft),
                FlashingImage(self.D_buttom, flashing_period=0.5, midleft=self.medals[0].pos_rect.midright),
            ]

        self.time_end = pg.time.get_ticks() + game_bridge_time
        self.ready_text = PureText('READY?', title_font_size, 'lightblue', center=(400, 270))
        self.go_text = PureText('GO!', title_font_size, 'lightblue', center=(400, 270))

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        if pg.time.get_ticks() > self.time_end: self.SwitchToScene(GameScene(self.level, self.num_of_player, self.charge_enabled))

        # keyboard hint
        for image in self.lr_buttoms:
            image.update()

    def Render(self, screen):
        screen.blit(self.background_image, self.background_image.get_rect())

        for i in range(self.num_of_player):
            # medal status
            if self.charge_enabled:
                self.medal_statuss[i].draw(screen)

            # medal
            self.medals[i].draw(screen)

            # score
            self.scores[i].draw(screen)

        if pg.time.get_ticks() + (game_bridge_time / 2) < self.time_end:
            self.ready_text.draw(screen)
        else:
            self.go_text.draw(screen)

        # keyboard hint
        for image in self.lr_buttoms:
            image.draw(screen)













class GameScene(SceneBase):
    # TODO: press <esc> to stop the game
    electron_valid_rect = pg.Rect(0, 400, 800, 200)
    background_image1 = pg.image.load(os.path.join(data_path, 'backgrounds', 'game_scene(classic).png'))
    background_image2 = pg.image.load(os.path.join(data_path, 'backgrounds', 'game_scene(advanced).png'))


    def new_photons(self):
        # parameters: center_pos, vel
        return [ element.Photon((400 + photon_distance * i, 0), velocity_of_photon)\
            for i in range(-photons_per_line//2+1, photons_per_line//2+1) ]

    def __init__(self, level, num_of_player, charge_enabled):
        self.next = self
        self.level = level # 1:easy, 7:hard
        self.charge_enabled = charge_enabled
        self.photons = []
        self.electrons = []
        self.photons.append(self.new_photons())
        self.num_of_player = num_of_player
        self.ground = Ground()
        self.horizon_rect2 = pg.Rect(0, line_of_horizon2, 800, 600 - line_of_horizon2)
        if self.charge_enabled: self.background_image = self.background_image2
        else:                   self.background_image = self.background_image1

        # depend on num_of_player
        if num_of_player == 1:
            self.scores = [ Score(score_font_size, 'pink', topright=(800 - 15, 15)) ]
            self.medals = [ Medal(0, center=(400, 600 - 60)) ]
            self.medal_statuss = [ MedalStatusBar((800 - 35, 300)) ]
            self.countdown = CountDown(game_time, 'pink', topleft=(15, 15))
        else:
            self.scores = [ Score(score_font_size, 'gold1', topleft=(15, 15)),
                            Score(score_font_size, 'deepskyblue1', topright=(800 - 15, 15)) ]
            self.medals = [ Medal(2, center=(400 + 120, 600 - 60)),
                            Medal(1, center=(400 - 120, 600 - 60)) ]
            self.medal_statuss = [ MedalStatusBar((800 - 35, 300)),
                                   MedalStatusBar((35, 300)) ]
            self.countdown = CountDown(game_time, 'burlywood1', midtop=(400, 25))


        self.left_right_pressed = 0 # {-1, 0, 1}
        self.a_d_pressed        = 0 # {-1, 0, 1}

    def generate_electron(self, pos, vel):
        # pos -> pg.Rect()
        self.electrons.append(element.Electron(pos, vel))

    def ProcessInput(self, events, pressed_keys):
        if pressed_keys[pg.K_LEFT]:  self.left_right_pressed -= 1
        if pressed_keys[pg.K_RIGHT]: self.left_right_pressed += 1
        if pressed_keys[pg.K_a]: self.a_d_pressed -= 1
        if pressed_keys[pg.K_d]: self.a_d_pressed += 1

    def Update(self):
        # update medal position
        self.medals[0].update(self.left_right_pressed)
        self.left_right_pressed = 0
        if self.num_of_player == 2:
            self.medals[1].update(self.a_d_pressed)
            self.a_d_pressed = 0

        # update photon position
        for sub_photons in self.photons:
            for photon in sub_photons:
                photon.update_pos()

        # generate next_photons
        if self.photons[-1][0].pos.centery >= photon_distance:
            self.photons.append(self.new_photons())

        # update electron position
        for electron in self.electrons:
            electron.update_pos()
            if not electron.inside(self.electron_valid_rect):
                self.electrons.remove(electron)

        # photon collision handle
        for photon in self.photons[0]:
            remove_this = False
            if photon.inside(self.horizon_rect2): remove_this = True
            for i in range(self.num_of_player):
                if photon.collide_with(self.medals[i].collision_rect):
                    remove_this = True
                    increment = 0
                    if (not self.charge_enabled) and photon.color_n >= self.level:
                        increment = photon.color_n
                    elif self.charge_enabled and photon.color_n >= self.level:
                        increment = photon.color_n * (1 - self.medal_statuss[i].charge / 200)

                    if increment != 0:
                        self.medals[i].set_highlight()
                        self.scores[i].update(int(6 * 5 * increment))
                        self.medal_statuss[i].update(3 * photon.color_n)
                        self.generate_electron(photon.pos.center, vec2(0, -increment))

            if remove_this: self.photons[0].remove(photon)
        if not self.photons[0]:
            del self.photons[0]

        # ground (recharge)
        for i in range(self.num_of_player):
            if self.medals[i].pos_rect.collidelist([ self.ground.pos_rect_l, self.ground.pos_rect_r ]) != -1:
                self.medal_statuss[i].update(-5)
                self.medals[i].set_ground()

        # update timer
        self.countdown.update()

    def Render(self, screen):
        screen.blit(self.background_image, self.background_image.get_rect())

        # photons & electrons
        for sub_photons in self.photons:
            for photon in sub_photons:
                photon.draw(screen)
        for electron in self.electrons:
            electron.draw(screen)

        # horizon 2
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect2)

        for i in range(self.num_of_player):
            # medal status
            if self.charge_enabled:
                self.medal_statuss[i].draw(screen)

            # medal
            self.medals[i].draw(screen)

            # score
            self.scores[i].draw(screen)

        # time remain
        self.countdown.draw(screen)

        # time's up!
        if self.countdown.time_remain == 0:
            self.SwitchToScene(EndBridgeScene((self.num_of_player, self.scores), screen))









class EndBridgeScene(SceneBase):
    def __init__(self, information, screen):
        '''
        information = (
            num_of_player -> int,
            score -> list,
        )
        '''
        self.next = self
        self.information = information
        self.freezed_screen = screen.copy()
        # parameters excluding time_remain is arbitrary
        self.time_end = pg.time.get_ticks() + end_bridge_time
        self.times_up_text = FlashingText('TIME\'S UP!!!', 120, 'violetred', center=(400, 280))

    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        self.times_up_text.update()
        if pg.time.get_ticks() > self.time_end: self.SwitchToScene(EndScene(self.information))

    def Render(self, screen):
        screen.blit(self.freezed_screen, self.freezed_screen.get_rect())

        # time's up
        self.times_up_text.draw(screen)









class EndScene(SceneBase):
    background_image = pg.image.load(os.path.join(data_path, 'backgrounds', 'end_scene.png'))
    crown_image = scaled_surface(pg.image.load(os.path.join(data_path, 'crown.png')), 0.3)

    def __init__(self, information):
        '''
        information = (
            num_of_player -> int,
            winner -> int,
            scores -> list,
        )
        '''
        self.next = self
        self.num_of_player = information[0]
        self.scores = information[1]
        self.user_focus = 0
        self.animation = EndAnimation(center=(230, 380))
        self.motto_image = scaled_surface(
            pg.image.load(os.path.join(data_path, 'backgrounds', f'motto{random.randint(0, len(mottos)-1)}.png')),
            1.0
        )
        self.enter_pressed = False

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

        self.animation.update()


    def Render(self, screen):
        screen.blit(self.background_image, self.background_image.get_rect())

        # score
        if self.num_of_player == 1:
            score_text = PureText('Score:', 80, 'pink', topright=(250+60, 60+20))
            score_text.draw(screen)
            score_number = PureText(f'{self.scores[0].score_number:05}', 70, 'pink', topright=(240+80, 130+20))
            score_number.draw(screen)
        else:
            base_pos_y, delta_y = 50, 110
            for i in range(2):
                score_text = PureText(f'P{i+1}\'s Score:', 60, self.scores[i].color, topright=(370, base_pos_y + i * delta_y))
                score_text.draw(screen)
                score_number = PureText(f'{self.scores[i].score_number:05}', 55, self.scores[i].color, topright=(370, base_pos_y + 50 + i * delta_y))
                score_number.draw(screen)

            # winner
            if self.scores[0].score_number > self.scores[1].score_number:
                screen.blit(self.crown_image, self.crown_image.get_rect(midleft=(370, 50 + base_pos_y)))
            elif self.scores[0].score_number < self.scores[1].score_number:
                screen.blit(self.crown_image, self.crown_image.get_rect(midleft=(370, 50 + base_pos_y + delta_y)))

        # animation
        self.animation.draw(screen)

        # motto
        screen.blit(self.motto_image, self.motto_image.get_rect(center=(300, 510)))

        # focus buttom
        base_pos_y, delta_y = 260, 55
        focus_rect = pg.Rect(0, 0, 15, 15)
        focus_rect.center = (530, base_pos_y + self.user_focus * delta_y)
        pg.draw.rect(screen, pg.Color('red'), focus_rect)








if __name__ == '__main__':
    pg.init()
    startWithScene(TitleScene())
    #startWithScene(HelpScene())
    #startWithScene(LevelSelectScene())
    #startWithScene(GameScene(2, 1, True))
    #startWithScene(GameScene(2, 2, True))
    #startWithScene(EndScene((1, [Score(score_font_size, 'pink')])))
