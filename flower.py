import os
import random
import pygame
import env
from spritesheet import SpriteSheet


class Flower(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'assets', 'img')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = SpriteSheet(os.path.join(self.img_folder, 'basictiles.png'))
        self.image = pygame.transform.scale(img.image_at((4*16, 2*16, 16, 16)).convert_alpha(), (25, 25))
        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(0, env.WIDTH),
            random.randint(0, env.HEIGHT)
        )
