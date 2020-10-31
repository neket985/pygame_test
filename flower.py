import random
import pygame
import env


class Flower(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill(env.GREEN)
        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(0, env.WIDTH),
            random.randint(0, env.HEIGHT)
        )
