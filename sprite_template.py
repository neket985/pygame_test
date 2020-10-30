import pygame
import os
import env


class Player(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'assets', 'img')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(os.path.join(self.img_folder, 'p1_jump.png')).convert()
        self.image = player_img
        self.image.set_colorkey(env.BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (env.WIDTH / 2, env.HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > env.WIDTH:
            self.rect.right = 0
