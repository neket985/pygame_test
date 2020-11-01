import os
import random
from typing import List

import pygame

import common
import env
from moved_entity import MovedEntity

kef_min = -10
kef_max = 10


def random_kefs():
    return [
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max),
        random.uniform(kef_min, kef_max)
    ]


class Bot(MovedEntity):
    moves_dict = dict([
        (0, env.BOT_KEY_LEFT[0]),
        (1, env.BOT_KEY_RIGHT[0]),
        (2, env.BOT_KEY_UP[0]),
        (3, env.BOT_KEY_DOWN[0])
    ])
    stay_frames = 0

    def __init__(self, flowers, girl, kefs=random_kefs()):
        self.load_images(os.path.join(env.img_folder, 'characters.png'), (3 * 16, 0, 3 * 16, 4 * 16), (16, 16))
        self.images = [self.inverted(i) for i in self.images]
        MovedEntity.__init__(self, env.BOT_KEY_LEFT, env.BOT_KEY_RIGHT, env.BOT_KEY_UP, env.BOT_KEY_DOWN)

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(center=(env.WIDTH / 2, env.HEIGHT / 2))

        self.flowers = flowers
        self.girl = girl
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
        if self.rect.top <= 0 or self.rect.left <= 0 or self.rect.bottom >= env.HEIGHT or self.rect.right >= env.WIDTH:
            self.stay_frames += 1

    def calc_next_step(self):
        flower_kef = (0, 0)
        for flower in self.flowers:
            flower_dist = (flower.rect.center[0] - self.rect.center[0], flower.rect.center[1] - self.rect.center[1])
            flower_kef = common.tuples_plus(flower_kef, flower_dist)

        girl_dist = (self.girl.rect.center[0] - self.rect.center[0], self.girl.rect.center[1] - self.rect.center[1])
        return (
                self.kefs[0] * flower_kef[0] +
                self.kefs[1] * flower_kef[1] +
                # self.kefs[2] * girl_dist[0] +
                # self.kefs[3] * girl_dist[1] +
                self.kefs[4] * self.rect.top +
                self.kefs[5] * self.rect.left +
                self.kefs[6] * (env.HEIGHT - self.rect.bottom) +
                self.kefs[7] * (env.WIDTH - self.rect.right)
        ).__abs__()

    def get_score(self):
        return 100 * (-self.flowers.__len__()) - self.stay_frames

    def get_child_kefs(self, count) -> List:
        return [self.get_child_kef() for i in range(count)]

    def get_child_kef(self):
        rnd_kef_num = random.randint(0, 100) % self.kefs.__len__()
        copy = self.kefs.copy()
        copy[rnd_kef_num] = random.uniform(kef_min, kef_max)
        return copy
