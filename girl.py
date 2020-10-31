import os

import pygame
import env
from spritesheet import SpriteSheet


class Girl(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'assets', 'img')

    @staticmethod
    def transform_sprite(s: pygame.Surface) -> pygame.Surface:
        surf = pygame.Surface((34, 50))
        surf.blit(pygame.transform.scale(s, (50, 50)), pygame.Rect(-8, 0, 50, 50))
        return surf.convert_alpha()

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = SpriteSheet(os.path.join(self.img_folder, 'characters.png'))
        self.image = self.transform_sprite(img.image_at((7*16, 0, 16, 16)))
        self.rect = self.image.get_rect(top=0, right=env.WIDTH-10)
