__all__ = ['data_path', 'default_font', 'flashing_period', 'countdown_font_size']

import os.path
if 'libs' in __name__:
    data_path = 'data'
else:
    data_path = os.path.join('..', 'data')

default_font = os.path.join(data_path, 'VT323-Regular.ttf')
flashing_period = 80
countdown_font_size = 60
