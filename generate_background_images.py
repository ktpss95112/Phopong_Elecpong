import pygame as pg
import os.path
import libs.element as element
from libs.OtherObjects import *
from libs.GlobalParameters import *
from libs.utility import *
data_path = 'data'


pg.init()



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
    base_pos_y, delta_y = 330, options_font_size
    start_text = PureText('Start', options_font_size, 'white', center=(400, base_pos_y))
    help_text = PureText('Help', options_font_size, 'white', center=(400, base_pos_y + delta_y))
    exit_text = PureText('Exit', options_font_size, 'white', center=(400, base_pos_y + 2 * delta_y))
    start_text.draw(screen)
    help_text.draw(screen)
    exit_text.draw(screen)

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'title_scene.png'))

    return screen




def help_scene(save=False):
    """
    screen1: TODO: magnify down_buttom to give hint
    screen2: TODO: add flashing text
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
        line_text = PureText(lines1[i], help_font_size, 'gray90', topleft=(40, base_pos_y + i * delta_y))
        line_text.draw(screen1)

    # left, right
    left_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'left.png')), 0.35)
    screen1.blit(left_buttom, left_buttom.get_rect(center=(559, 184)))
    right_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'right.png')), 0.35)
    screen1.blit(right_buttom, right_buttom.get_rect(center=(658, 184)))

    if save:
        pg.image.save(screen1, os.path.join(data_path, 'backgrounds', 'help_scene1.png'))


    screen2 = scene_base()
    for i in range(len(lines2)):
        line_text = PureText(lines2[i], help_font_size, 'gray90', topleft=(40, base_pos_y + i * delta_y))
        line_text.draw(screen2)

    # 'press enter space to continue'
    #flashing_text = PureText('Press     or     to Continue ...', 40, 'gray90', center=(400, 515))
    #flashing_text.draw(screen2)

    # enter, space
    #enter_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'enter.png')), 0.3)
    #screen2.blit(enter_buttom, enter_buttom.get_rect(center=(265, 515)))
    #space_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'space.png')), 0.3)
    #screen2.blit(space_buttom, space_buttom.get_rect(center=(375, 515)))

    if save:
        pg.image.save(screen2, os.path.join(data_path, 'backgrounds', 'help_scene2.png'))

    return screen2



def level_scene(save=False):
    screen = scene_base()

    # title
    title_level_text = PureText('Level', title_font_size, 'white', center=(230 - 15, 150))
    title_mode_text = PureText('Mode', title_font_size, 'white', center=(600 - 15, 150))
    title_level_text.draw(screen)
    title_mode_text.draw(screen)

    # up, down, right
    # TODO: magnify buttom when pressed
    up_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'up.png')), 0.35)
    screen.blit(up_buttom, up_buttom.get_rect(center=(230 - 15, 300)))
    down_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'down.png')), 0.35)
    screen.blit(down_buttom, down_buttom.get_rect(center=(230 - 15, 460)))
    right_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'right.png')), 0.35)
    screen.blit(right_buttom, right_buttom.get_rect(center=(330 - 15, 380)))

    # mode selection
    modes = ['Classic', 'Advanced']
    base_pos_y, delta_y = 330, 70
    for i in range(len(modes)):
        mode_text = PureText(modes[i], options_font_size, 'white', center=(600 - 15, base_pos_y + i * delta_y))
        mode_text.draw(screen)

    # enter
    enter_buttom = scaled_surface(pg.image.load(os.path.join(data_path, 'keys', 'enter.png')), 0.25)
    screen.blit(enter_buttom, enter_buttom.get_rect(center=(730 - 15, 370)))

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'level_scene.png'))

    return screen




def game_bridge_scene(save=False):
    screen = scene_base()

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'game_scene(classic).png'))

    medal_status = MedalStatusBar((800 - 35, 300))
    medal_status.draw(screen)

    ground = Ground()
    ground.draw(screen)

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'game_scene(advanced).png'))

    return screen




def end_scene(save=False):
    screen = scene_base()

    options = ['Again', 'Homepage', 'Exit']
    base_pos_y, delta_y = 300, 55
    for i in range(len(options)):
        option_text = PureText(options[i], options_font_size, 'white', midleft=(550, base_pos_y + i * delta_y))
        option_text.draw(screen)

    if save:
        pg.image.save(screen, os.path.join(data_path, 'backgrounds', 'end_scene.png'))

    return screen



title_scene(save=True)
help_scene(save=True)
level_scene(save=True)
game_bridge_scene(save=True)
end_scene(save=True)
