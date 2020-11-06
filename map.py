import os

import pygame

import env
from spritesheet import SpriteSheet


class Map(pygame.sprite.Sprite):
    bit_size = (50, 50)
    map_size = (env.WIDTH // bit_size[0] + 1, env.HEIGHT // bit_size[1] + 1)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.Surface((env.WIDTH, env.HEIGHT)).convert_alpha()
        self.image = img
        self.rect = self.image.get_rect(left=0, top=0)

        sheet = SpriteSheet(os.path.join(env.img_folder, 'basictiles.png'))
        bit = pygame.transform.scale(
            sheet.image_at((1 * 16, 8 * 16, 16, 16)),
            self.bit_size
        )
        for x in range(self.map_size[0]):
            for y in range(self.map_size[1]):
                img.blit(
                    bit,
                    bit.get_rect(left=x * self.bit_size[0], top=y * self.bit_size[1])
                )
