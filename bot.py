import os
import random
from typing import List

import pygame

import common
import env
from moved_entity import MovedEntity

kef_min = -1
kef_max = 1


def random_kefs(count):
    return [random.uniform(kef_min, kef_max) for i in range(count)]


class Bot(MovedEntity):
    moves_dict = dict([
        (0, env.BOT_KEY_LEFT[0]),
        (1, env.BOT_KEY_RIGHT[0]),
        (2, env.BOT_KEY_UP[0]),
        (3, env.BOT_KEY_DOWN[0])
    ])
    score = 0
    max_coord = (0, 0)
    min_coord = (env.WIDTH, env.HEIGHT)

    def __init__(self, flowers, girl, flowers_count, kefs=None):
        self.load_images(os.path.join(env.img_folder, 'characters.png'), (3 * 16, 0, 3 * 16, 4 * 16), (16, 16))
        self.images = [self.inverted(i) for i in self.images]
        MovedEntity.__init__(self, env.BOT_KEY_LEFT, env.BOT_KEY_RIGHT, env.BOT_KEY_UP, env.BOT_KEY_DOWN)

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(center=(env.WIDTH / 2, env.HEIGHT / 2))
        self.last_pos = self.rect.center

        self.flowers = flowers
        self.flowers_count = flowers_count
        self.girl = girl

        if kefs is None:
            self.kefs = random_kefs(flowers_count * 2 + 6)
        else:
            self.kefs = kefs

    @staticmethod
    def inverted(img):
        inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
        inv.fill((255, 255, 255, 255))
        inv.blit(img, (0, 0), None, pygame.BLEND_RGB_SUB)
        return inv

    def auto_step(self):
        self.collect_meta()
        step = (self.calc_next_step() % 100) // 10
        if step < 4:
            self.move_start(self.moves_dict[step])
        elif step < 8:
            self.move_end(self.moves_dict[step - 4])

    def collect_meta(self):
        new_pos = self.rect.center
        dist = (self.last_pos[0] - new_pos[0]).__abs__() + (self.last_pos[1] - new_pos[1]).__abs__()
        if dist <= 2:
            self.score -= 10
        if new_pos[0] > self.max_coord[0]:
            self.max_coord = (new_pos[0], self.max_coord[1])
        if new_pos[1] > self.max_coord[1]:
            self.max_coord = (self.max_coord[0], new_pos[1])
        if new_pos[0] < self.min_coord[0]:
            self.min_coord = (new_pos[0], self.min_coord[1])
        if new_pos[1] < self.min_coord[1]:
            self.min_coord = (self.min_coord[0], new_pos[1])

    def calc_next_step(self):
        flower_kef = (0, 0)
        i = 0
        for flower in self.flowers:
            flower_dist = (self.kefs[i] * (flower.rect.center[0] - self.rect.center[0]),
                           self.kefs[i + 1] * (flower.rect.center[1] - self.rect.center[1]))
            i += 2
            flower_kef = common.tuples_plus(flower_kef, flower_dist)

        girl_dist = (self.girl.rect.center[0] - self.rect.center[0], self.girl.rect.center[1] - self.rect.center[1])

        return (
                flower_kef[0] +
                flower_kef[1] +
                # self.kefs[i] * girl_dist[0] +
                # self.kefs[i+1] * girl_dist[1] +
                self.kefs[i + 2] * self.rect.top +
                self.kefs[i + 3] * self.rect.left +
                self.kefs[i + 4] * (env.HEIGHT - self.rect.bottom) +
                self.kefs[i + 5] * (env.WIDTH - self.rect.right)
        ).__abs__()

    def get_score(self):
        move_rect = (self.max_coord[0] - self.min_coord[0]) + (self.max_coord[1] - self.min_coord[1])
        return 100 * (-self.flowers.__len__()) + self.score + move_rect

    def get_child_kefs(self, count) -> List:
        return [self.get_child_kef() for i in range(count)]

    def get_child_kef(self):
        rnd_kef_num = random.randint(0, 100) % self.kefs.__len__()
        copy = self.kefs.copy()
        copy[rnd_kef_num] = random.uniform(kef_min, kef_max)
        return copy
