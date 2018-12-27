import pygame as pg
from libs import scene

def main():
    pg.init()
    scene.startWithScene(scene.TitleScene())

if __name__ == '__main__':
    main()
