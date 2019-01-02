import os.path
if 'libs' in __name__:
    data_path = 'data'
else:
    data_path = os.path.join('..', 'data')

default_font = os.path.join(data_path, 'VT323-Regular.ttf')
flashing_period = 80
game_time = 31

title_font_size = 150
options_font_size = 55
help_font_size = 35
score_font_size = 60
countdown_font_size = 60
