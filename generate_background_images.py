import pygame as pg
import os.path
import libs.element as element
from libs.OtherObjects import *
data_path = 'data'


pg.init()


def scaled_surface(surface, scale):
    return pg.transform.smoothscale(surface, (int(scale * surface.get_width()), int(scale * surface.get_height())))



def show(s):
    screen = pg.display.set_mode((800, 600))
    screen.blit(s, s.get_rect())

    pg.display.flip()
    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)



def scene_base():
    screen = pg.Surface((800, 600))

    # horizon
    line_of_horizon = 600 - 40
    horizon_rect = pg.Rect(0, line_of_horizon, 800, 600 - line_of_horizon)
    pg.draw.rect(screen, pg.Color('chocolate4'), horizon_rect)

    return screen




def title_scene(save=False):
    screen = scene_base()

    # title
    for i in (1, 2):
        image = scaled_surface(pg.image.load(os.path.join(data_path, 'Title', f'title_{i}.png')), 0.8)
        screen.blit(image, image.get_rect(center=(400, i * 100)))

    # options
    base_pos_y, delta_y = 330, 55
    start_text = PureText('Start', 55, 'white', center=(400, base_pos_y))
    help_text = PureText('Help', 55, 'white', center=(400, base_pos_y + delta_y))
    exit_text = PureText('Exit', 55, 'white', center=(400, base_pos_y + 2 * delta_y))
    start_text.draw(screen)
    help_text.draw(screen)
    exit_text.draw(screen)

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'title_scene.png'))

    return screen




def help_scene(save=False):
    """
    screen1: TODO: magnify down_buttom to give hint
    screen2: TODO: use black rect to block to make flashing effect
    """
    lines1 = """
tldr: Catch as many purple photons as you can!

   It is a game simulating "photoelectric effect".

   In this game, the player can use    and    to
move his/her "Einstein". The "Einstein" is holding
a medal upward in order to catch the photons
falling from the sky.

   By "photoelectric effect", photons that has a
higher frequency can emit an electron with higher
kinetic energy. That is, the electron will move
faster, and your score is proportional to its
velocity.
""".strip('\n').split('\n')
    lines2 = """
   However, different medal has different "work
function", which is implemented as "Level" in this
game. In short, electron won't be emitted if the
frequency of the catched photon is too low.

Advanced mode:
   In reality, as the electron emitted, the medal
will be charged, and thus harder for the next
emission. In advanced mode, you will see a charge
status bar on one side of the screen. The charge
increases as the electron emitted. If charge reach
the maximum, you have to connect to "ground" on
each side of the horizon. Of course you can connect
to ground when the status hasn't reached maximum.
""".strip('\n').split('\n')

    screen1 = scene_base()

    base_pos_y, delta_y = 45, 30
    for i in range(len(lines1)):
        line_text = PureText(lines1[i], 35, 'gray90', topleft=(40, base_pos_y + i * delta_y))
        line_text.draw(screen1)

    # left, right
    left_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'left.png')), 0.35)
    screen1.blit(left_buttom, left_buttom.get_rect(center=(560, 185)))
    right_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'right.png')), 0.35)
    screen1.blit(right_buttom, right_buttom.get_rect(center=(660, 185)))

    if save:
        pg.image.save(screen1, os.path.join(data_path, 'backgrounds', 'help_scene1.png'))


    screen2 = scene_base()
    for i in range(len(lines2)):
        line_text = PureText(lines2[i], 35, 'gray90', topleft=(40, base_pos_y + i * delta_y))
        line_text.draw(screen2)
    # 'press enter space to continue'
    flashing_text = PureText('Press     or     to Continue ...', 40, 'gray90', center=(400, 515))
    flashing_text.draw(screen2)

    # enter, space
    enter_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'enter.png')), 0.3)
    screen2.blit(enter_buttom, enter_buttom.get_rect(center=(265, 515)))
    space_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'space.png')), 0.3)
    screen2.blit(space_buttom, space_buttom.get_rect(center=(375, 515)))

    if save:
        pg.image.save(screen2, os.path.join(data_path, 'backgrounds', 'help_scene2.png'))

    return screen2




def level_scene(save=False):
    screen = scene_base()

    # title
    title_level_text = PureText('Level', 150, 'white', center=(200, 150))
    title_mode_text = PureText('Mode', 150, 'white', center=(570, 150))
    title_level_text.draw(screen)
    title_mode_text.draw(screen)

    # up, down, right
    # TODO: magnify buttom when pressed
    up_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'up.png')), 0.35)
    screen.blit(up_buttom, up_buttom.get_rect(center=(200, 300)))
    down_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'down.png')), 0.35)
    screen.blit(down_buttom, down_buttom.get_rect(center=(200, 460)))
    right_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'right.png')), 0.35)
    screen.blit(right_buttom, right_buttom.get_rect(center=(300, 380)))

    # mode selection
    modes = ['Classic', 'Advanced']
    base_pos_y, delta_y = 330, 70
    for i in range(len(modes)):
        mode_text = PureText(modes[i], 50, 'white', center=(570, base_pos_y + i * delta_y))
        mode_text.draw(screen)

    # enter
    enter_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'enter.png')), 0.25)
    screen.blit(enter_buttom, enter_buttom.get_rect(center=(700, 370)))

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'level_scene.png'))

    return screen



"""
def game_bridge_scene(save=False):
    """
    #TODO: add ground or not based on mode
    """
    screen1 = scene_base()

    score = Score(60, 'pink', topright=(800 - 15, 15))
    medal = Medal()
    medal_status = MedalStatusBar((800 - 15, 280))
    countdown = CountDown(self.time_remain, 60, 'pink', topleft=(15, 15))
    countdown.start_tick()

    if save:
        pg.image.save(screen1, os.path.join(data_path, 'backgrounds', 'help_scene1.png'))

    return screen1

    screen2 = scene_base()

    if save:
        pg.image.save(screen2, os.path.join(data_path, 'backgrounds', 'help_scene2.png'))

    return screen2

"""


"""


class GameBridgeScene(SceneBase):
    pass











class ClassicGameScene(SceneBase):
    photons = []
    photons_per_line = 7 # should be odd number
    electrons = []
    photon_distance = 80
    velocity_of_photon = vec2(0, 2)
    electron_valid_rect = pg.Rect(0, 400, 800, 200)
    time_remain = 31

    def new_photons(self):
        # parameters: center_pos, vel
        return [ element.Photon((400 + self.photon_distance * i, 0), self.velocity_of_photon)\
            for i in range(-self.photons_per_line//2+1, self.photons_per_line//2+1) ]

    def __init__(self, level, charge_enabled):
        self.next = self
        self.level = level # 1:easy, 7:hard
        self.charge_enabled = charge_enabled
        self.photons.append(self.new_photons())
        self.score = Score(60, 'pink', topright=(800 - 15, 15))
        self.medal = Medal()
        self.medal_status = MedalStatusBar((800 - 15, 280))
        self.ground = [Ground(10), Ground(790)]
        self.countdown = CountDown(self.time_remain, 60, 'pink', topleft=(15, 15))
        self.countdown.start_tick()

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
            if photon.inside(self.horizon_rect):
                self.photons[0].remove(photon)
            elif photon.collide_with(self.medal.pos_rect):
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
        if self.medal.pos_rect.collidelist([ g.pos_rect for g in self.ground ]) != -1:
            self.medal_status.update(-5)

        # update timer
        self.countdown.update()

    def Render(self, screen):
        screen.fill(pg.Color('black'))

        # photons & electrons
        for sub_photons in self.photons:
            for photon in sub_photons:
                photon.draw(screen)
        for electron in self.electrons:
            electron.draw(screen)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)

        # ground
        self.ground[0].draw(screen)
        self.ground[1].draw(screen)

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








class EndBridgeScene(SceneBase):
    time_duration = 4.7

    def __init__(self, score, screen):
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



"""



title_scene(save=True)
help_scene(save=True)
level_scene(save=True)
