import os
from datetime import datetime

import pygame
from pygame.time import Clock

import common
import env
from spritesheet import SpriteSheet


class Player(pygame.sprite.Sprite):
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'assets', 'img')
    speed = 6
    move_state = (0, 0)
    img_row_k = 0

    tik_moves_buffer = set([])
    perm_move_state = (0, 0)

    @staticmethod
    def transform_sprite(s: pygame.Surface) -> pygame.Surface:
        surf = pygame.Surface((30, 50))
        surf.blit(pygame.transform.scale(s, (50, 50)), pygame.Rect(-10, 0, 50, 50))
        return surf.convert_alpha()

    def __init__(self, clock: Clock):
        pygame.sprite.Sprite.__init__(self)
        self.clock = clock
        img = SpriteSheet(os.path.join(self.img_folder, 'characters.png'))
        self.images = [self.transform_sprite(i) for i in
                       img.images_with_fixed_size((3 * 16, 0, 3 * 16, 4 * 16), (16, 16))]

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(center=(env.WIDTH / 2, env.HEIGHT / 2))

    def getSpriteByTik(self) -> pygame.Surface:
        tick = datetime.utcnow().microsecond
        tick_k = 0
        if tick // (1000_000 / 6) % 2 == 0:
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

    def move_start(self, key):
        if env.KEY_LEFT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif env.KEY_RIGHT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif env.KEY_DOWN.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, 1), self.move_state)
        elif env.KEY_UP.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, -1), self.move_state)

    def move_end(self, key):
        if self.tik_moves_buffer.__contains__(key):
            if env.KEY_LEFT.__contains__(key):
                self.perm_move_state = common.tuples_plus((-1, 0), self.perm_move_state)
            elif env.KEY_RIGHT.__contains__(key):
                self.perm_move_state = common.tuples_plus((1, 0), self.perm_move_state)
            elif env.KEY_DOWN.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, 1), self.perm_move_state)
            elif env.KEY_UP.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, -1), self.perm_move_state)

        if env.KEY_LEFT.__contains__(key):
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif env.KEY_RIGHT.__contains__(key):
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif env.KEY_DOWN.__contains__(key):
            self.move_state = common.tuples_plus((0, -1), self.move_state)
        elif env.KEY_UP.__contains__(key):
            self.move_state = common.tuples_plus((0, 1), self.move_state)
