from datetime import datetime
from typing import Tuple, List

import pygame
from pygame.sprite import Sprite

import common
import env
from spritesheet import SpriteSheet


class MovedEntity(Sprite):
    speed = 6
    move_state = (0, 0)
    img_row_k = 0
    images: List[pygame.Surface] = []

    tik_moves_buffer = set([])
    perm_move_state = (0, 0)

    @staticmethod
    def transform_sprite(s: pygame.Surface) -> pygame.Surface:
        surf = pygame.Surface((30, 50))
        surf.blit(pygame.transform.scale(s, (50, 50)), pygame.Rect(-10, 0, 50, 50))
        return surf.convert_alpha()

    def load_images(self, path, rect: Tuple[int, int, int, int], size: Tuple[int, int]):
        img = SpriteSheet(path)
        self.images = [self.transform_sprite(i) for i in img.images_with_fixed_size(rect, size)]

    def getSpriteByTik(self) -> pygame.Surface:
        tick = datetime.utcnow().microsecond
        tick_k = 0
        if tick // (1000_000 / self.speed) % 2 == 0:
            tick_k = 2
        move_vector = common.tuples_plus(self.move_state, self.perm_move_state)
        is_run_x = move_vector[0] != 0
        is_run_y = move_vector[1] != 0
        if is_run_x:
            if move_vector[0] > 0:
                self.img_row_k = 6
            else:
                self.img_row_k = 3
        elif is_run_y:
            if move_vector[1] > 0:
                self.img_row_k = 0
            else:
                self.img_row_k = 9
        else:
            tick_k = 1

        return self.images[self.img_row_k + tick_k]

    def move_start(self, key):
        if self.KEY_LEFT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif self.KEY_RIGHT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif self.KEY_DOWN.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, 1), self.move_state)
        elif self.KEY_UP.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, -1), self.move_state)

    def move_end(self, key):
        if self.tik_moves_buffer.__contains__(key):
            if self.KEY_LEFT.__contains__(key):
                self.perm_move_state = common.tuples_plus((-1, 0), self.perm_move_state)
            elif self.KEY_RIGHT.__contains__(key):
                self.perm_move_state = common.tuples_plus((1, 0), self.perm_move_state)
            elif self.KEY_DOWN.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, 1), self.perm_move_state)
            elif self.KEY_UP.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, -1), self.perm_move_state)

        if self.KEY_LEFT.__contains__(key):
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif self.KEY_RIGHT.__contains__(key):
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif self.KEY_DOWN.__contains__(key):
            self.move_state = common.tuples_plus((0, -1), self.move_state)
        elif self.KEY_UP.__contains__(key):
            self.move_state = common.tuples_plus((0, 1), self.move_state)

    def __init__(self, key_left, key_right, key_up, key_down):
        Sprite.__init__(self)
        self.KEY_LEFT = key_left
        self.KEY_RIGHT = key_right
        self.KEY_DOWN = key_down
        self.KEY_UP = key_up

    def update(self):
        self.image = self.getSpriteByTik()
        move_x = 0
        if self.move_state[0] != 0:
            move_x = (self.move_state[0].__abs__() / self.move_state[0]) * \
                     self.speed / (1 + (self.move_state[1] / self.move_state[0]).__abs__())

        move_y = 0
        if self.move_state[1] != 0:
            move_y = (self.move_state[1].__abs__() / self.move_state[1]) * \
                     self.speed / \
                     (1 + (self.move_state[0] / self.move_state[1]).__abs__())

        move_x += self.perm_move_state[0]
        move_y += self.perm_move_state[1]

        self.rect.x += int(move_x)
        self.rect.y += int(move_y)

        if self.rect.right > env.WIDTH:
            self.rect.right = env.WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > env.HEIGHT:
            self.rect.bottom = env.HEIGHT

        self.tik_moves_buffer.clear()
        self.perm_move_state = (0, 0)
