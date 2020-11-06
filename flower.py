import os
import random

import pygame

import env
from spritesheet import SpriteSheet


class Flower(pygame.sprite.Sprite):
    width = 50
    height = 50

    def __init__(self, center=None):
        pygame.sprite.Sprite.__init__(self)
        img = SpriteSheet(os.path.join(env.img_folder, 'flower.png'))
        self.image = pygame.transform.scale(img.image_at((5 * 32, 0, 32, 32)),
                                            (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()

        if center is None:
            center = (
                random.randint(self.width // 2, env.WIDTH - self.width // 2),
                random.randint(self.height // 2, env.HEIGHT - self.height // 2)
            )
        self.rect.center = center
