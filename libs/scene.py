import pygame as pg
import element


def startWithScene(s):
    pg.init()
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
    base_focus_position = pg.Rect(260, 335, 20, 20)
    enter_pressed = False
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN: self.user_focus += 1
                if event.key == pg.K_UP:   self.user_focus -= 1
                if self.user_focus < 0: self.user_focus = 0
                if self.user_focus > 2: self.user_focus = 2

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
        title_font = pg.font.SysFont(None, 150)
        title_text = title_font.render('Title Here', True, pg.Color('white'))

        # options
        options_font = pg.font.SysFont(None, 50)
        start_text = options_font.render('Start', True, pg.Color('white'))
        help_text = options_font.render('Help (Rules)', True, pg.Color('white'))
        exit_text = options_font.render('Exit', True, pg.Color('white'))

        # draw
        screen.blit(title_text, (400 - title_text.get_width() // 2, 130))
        screen.blit(start_text, (300, 330))
        screen.blit(help_text, (300, 380))
        screen.blit(exit_text, (300, 430))
        pg.draw.rect(
            screen,
            pg.Color('white'),
            self.base_focus_position.move(0, 50*self.user_focus)
        )









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
        screen.fill(pg.Color('white'))

        # title
        title_font = pg.font.SysFont(None, 150)
        title_text_level = title_font.render('Level', True, pg.Color('black'))
        title_text_mode = title_font.render('Mode', True, pg.Color('black'))
        screen.blit(title_text_level, (200 - title_text_level.get_width() // 2, 80))
        screen.blit(title_text_mode, (600 - title_text_mode.get_width() // 2, 80))

        # level selection
        level_selection_rect = pg.Rect(0, 0, 80, 100)
        level_selection_rect.center = (200, 380)
        pg.draw.rect(screen, pg.Color('black'), level_selection_rect) # backgroound
        level_font = pg.font.SysFont(None, 50)
        level_text = level_font.render(f'{self.level}', True, pg.Color('yellow'))
        screen.blit(level_text, (200 - level_text.get_width() // 2, 360))
        # TODO: add little triangle above and below the rect

        # mode selection
        mode_font = pg.font.SysFont(None, 50)
        modes = ['Classic', 'Classic (advanced)', 'Circle']
        pos_base, delta = 310, 50
        for i in range(self.number_of_mode):
            modes_text = mode_font.render(modes[i], True, pg.Color('black'))
            screen.blit(modes_text, (600 - modes_text.get_width() // 2, pos_base + delta * i))

        # focus
        if self.user_focus[0] == 0:
            pg.draw.rect(screen, pg.Color('red'), level_selection_rect, 5)
        if self.user_focus[0] == 1:
            mode_focus_rect = pg.Rect(0, 0, 300, 50)
            mode_focus_rect.center = (600, pos_base + delta * self.user_focus[1] + 17)
            pg.draw.rect(screen, pg.Color('red'), mode_focus_rect, 5)

        # TODO:
        # image to give hint of press enter
        # highlight when focus is on modes, and vice versa









class HelpScene(SceneBase):
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill(pg.Color('white'))

        # title
        title_font = pg.font.SysFont(None, 150)
        title_text = title_font.render('Help Title', True, pg.Color('black'))

        # draw
        screen.blit(title_text, (400 - title_text.get_width() // 2, 130))










class ClassicGameScene(SceneBase):
    photons = []
    photons_per_line = 7 # should be odd number
    electrons = []
    photon_distance = 80
    line_of_horizon = 600 - 40
    velocity_of_photon = (0, 2)
    horizon_rect = pg.Rect(0, line_of_horizon, 800, 600 - line_of_horizon)
    medal_pos = [400, 600 - 60]
    medal_rect = pg.Rect(0, 0, 70, 10)
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

    def generate_electron(self, pos, vel):
        # pos -> pg.Rect()
        self.electrons.append(element.Electron(pos, vel))

    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        # update photon position
        self.medal_rect.center = self.medal_pos
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
                if photon.color_n >= self.level:
                    self.generate_electron(photon.pos.center, (0, -photon.color_n))
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
            pg.draw.rect(screen, pg.Color('olivedrab'), electron.pos)

        # horizon
        pg.draw.rect(screen, pg.Color('chocolate4'), self.horizon_rect)
        pg.draw.rect(screen, pg.Color('gray77'), self.medal_rect)









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
    #startWithScene(LevelSelectScene())
    startWithScene(ClassicGameScene(1, True))
