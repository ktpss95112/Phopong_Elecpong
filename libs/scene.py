import pygame

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
    base_focus_position = pygame.Rect(260, 335, 20, 20)
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.user_focus += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.user_focus -= 1
            if self.user_focus < 0: self.user_focus = 0
            if self.user_focus > 2: self.user_focus = 2

            if event.type == pygame.KEYDOWN and\
                    (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                if self.user_focus == 0: self.SwitchToScene(LevelSelectScene())
                if self.user_focus == 1: self.SwitchToScene(HelpScene())
                if self.user_focus == 2: self.Terminate()


    def Update(self):
        pass

    def Render(self, screen):
        screen.fill((0, 0, 0))
        # TODO: background

        # title
        title_font = pygame.font.SysFont(None, 150)
        title_text = title_font.render('Title Here', True, (255, 255, 255))

        # options
        options_font = pygame.font.SysFont(None, 50)
        start_text = options_font.render('Start', True, (255, 255, 255))
        help_text = options_font.render('Help (Rules)', True, (255, 255, 255))
        exit_text = options_font.render('Exit', True, (255, 255, 255))

        # draw
        screen.blit(title_text, (400 - title_text.get_width() // 2, 130))
        screen.blit(start_text, (300, 330))
        screen.blit(help_text, (300, 380))
        screen.blit(exit_text, (300, 430))
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            self.base_focus_position.move(0, 50*self.user_focus)
        )

class LevelSelectScene(SceneBase):
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((255, 255, 255))

class HelpScene(SceneBase):
    def ProcessInput(self, events, pressed_keys):
        pass
        
    def Update(self):
        pass
    
    def Render(self, screen):
        screen.fill((255, 255, 255))




