import os

import pygame


WIDTH = 1080  # ширина игрового окна
HEIGHT = 650 # высота игрового окна
FPS = 30 # частота кадров в секунду

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (80, 155, 80)
BLUE = (0, 0, 255)

PLAYER_KEY_LEFT = (97, 1092) #pygame.K_a
PLAYER_KEY_RIGHT = (100, 1074) #pygame.K_d
PLAYER_KEY_UP = (119, 1094) #pygame.K_w
PLAYER_KEY_DOWN = (115, 1099) #pygame.K_s

BOT_KEY_LEFT = (0,)
BOT_KEY_RIGHT = (1,)
BOT_KEY_UP = (2,)
BOT_KEY_DOWN = (3,)

GIRL_KEY_LEFT = (1073741904,)
GIRL_KEY_RIGHT = (1073741903,)
GIRL_KEY_UP = (1073741906,)
GIRL_KEY_DOWN = (1073741905,)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'assets', 'img')



