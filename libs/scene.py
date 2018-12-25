import pygame as pg


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
    user_level = 1
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
            self.user_level = (self.user_level - 1 + self.up_down_pressed + 7) % 7 + 1
            self.up_down_pressed = 0
            self.enter_pressed = False
        if self.user_focus[0] == 1:
            self.user_focus[1] -= self.up_down_pressed
            if self.user_focus[1] < 0: self.user_focus[1] = 0
            if self.user_focus[1] >= self.number_of_mode: self.user_focus[1] = self.number_of_mode - 1
            self.up_down_pressed = 0
            if self.enter_pressed:
                if self.user_focus[1] == 0:
                    self.SwitchToScene(ClassicGameScene(self.user_level, False))
                if self.user_focus[1] == 1:
                    self.SwitchToScene(ClassicGameScene(self.user_level, True))
                if self.user_focus[1] == 2:
                    self.SwitchToScene(CircleGameScene(self.user_level))
    
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
        level_text = level_font.render(f'{self.user_level}', True, pg.Color('yellow'))
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
    def __init__(self, level, ground_enabled):
        self.next = self
        self.level = level
        self.ground_enabled = ground_enabled

    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill(pg.Color('black'))









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
    startWithScene(ClassicGameScene(1, True))
