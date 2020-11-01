import os
import pygame
import env
from moved_entity import MovedEntity


class Girl(MovedEntity):
    speed = 4

    @staticmethod
    def transform_sprite(s: pygame.Surface) -> pygame.Surface:
        surf = pygame.Surface((34, 50))
        surf.blit(pygame.transform.scale(s, (50, 50)), pygame.Rect(-8, 0, 50, 50))
        return surf.convert_alpha()

    def __init__(self):
        self.load_images(os.path.join(env.img_folder, 'characters.png'), (6*16, 0, 3*16, 4*16), (16, 16))
        MovedEntity.__init__(self, env.GIRL_KEY_LEFT, env.GIRL_KEY_RIGHT, env.GIRL_KEY_UP, env.GIRL_KEY_DOWN)

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(top=0, right=env.WIDTH-10)
