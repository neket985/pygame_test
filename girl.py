import pygame
import env


class Girl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(env.RED)
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.right = env.WIDTH
