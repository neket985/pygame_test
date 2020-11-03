import os
import random
from typing import List

import pygame

import env
from moved_entity import MovedEntity

kef_min = -1
kef_max = 1


def random_kefs(count):
    return [random.uniform(kef_min, kef_max) for i in range(count)]


class Bot(MovedEntity):
    score = 0
    max_coord = (0, 0)
    min_coord = (env.WIDTH, env.HEIGHT)
    die_oreol = 50
    oreol_move_timer = 40
    oreol_contains = 0
    max_distance = (env.WIDTH**2+env.HEIGHT**2)**0.5

    def __init__(self, flowers, girl, flowers_count, gen, kefs=None):
        self.gen = gen
        self.load_images(os.path.join(env.img_folder, 'characters.png'), (3 * 16, 0, 3 * 16, 4 * 16), (16, 16))
        # if kefs is None:
        self.images = [self.inverted(i) for i in self.images]

        MovedEntity.__init__(self, env.BOT_KEY_LEFT, env.BOT_KEY_RIGHT, env.BOT_KEY_UP, env.BOT_KEY_DOWN)

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(center=(env.WIDTH / 2, env.HEIGHT / 2))
        self.last_pos = self.rect.center

        self.flowers = flowers
        self.flowers_count = flowers_count
        self.girl = girl

        if kefs is None:
            self.kefs = random_kefs(flowers_count + 1)
        else:
            self.kefs = kefs

    def inverted(self, img):
        inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
        inv.blit(img, (0, 0))
        text = pygame.font.Font(pygame.font.get_default_font(), 20).render(str(self.gen), False, env.WHITE)
        inv.blit(text, text.get_rect(center=inv.get_rect().center))
        return inv

    def auto_step(self):
        self.collect_meta()
        self.move_state = self.calc_next_step()

    def collect_meta(self):
        new_pos = self.rect.center
        x_pos_dist = (self.last_pos[0] - new_pos[0]).__abs__()
        y_pos_dist = (self.last_pos[1] - new_pos[1]).__abs__()

        self.oreol_contains += 1
        if x_pos_dist > self.die_oreol or y_pos_dist > self.die_oreol:
            self.last_pos = new_pos
            self.oreol_contains = 0
        elif self.oreol_move_timer - self.oreol_contains <= 0:
            self.score -= (self.oreol_contains - self.oreol_move_timer) // 10

        if new_pos[0] > self.max_coord[0]:
            self.max_coord = (new_pos[0], self.max_coord[1])
        if new_pos[1] > self.max_coord[1]:
            self.max_coord = (self.max_coord[0], new_pos[1])
        if new_pos[0] < self.min_coord[0]:
            self.min_coord = (new_pos[0], self.min_coord[1])
        if new_pos[1] < self.min_coord[1]:
            self.min_coord = (self.min_coord[0], new_pos[1])

    def calc_next_step(self):
        object_for_move = []
        i = 0
        for flower in self.flowers:
            flower_dist = (flower.rect.center[0] - self.rect.center[0],
                           flower.rect.center[1] - self.rect.center[1])
            distance = ((flower_dist[0]**2 + flower_dist[1]**2)**0.5)/self.max_distance
            object_for_move.append((self.kefs[i]/distance, flower_dist))
            i += 1

        girl_dist = (self.girl.rect.center[0] - self.rect.center[0], self.girl.rect.center[1] - self.rect.center[1])
        object_for_move.append((self.kefs[i], girl_dist))

        object_for_move.sort(key=lambda x: x[0], reverse=True)
        best_move = object_for_move[0]
        return best_move[1]

    def get_score(self):
        return 1000 * (-self.flowers.__len__()) + self.score

    def get_child_kefs(self, count) -> List:
        return [self.get_child_kef() for i in range(count)]

    def get_child_kef(self):
        rnd_kef_num = random.randint(0, 100) % self.kefs.__len__()
        copy = self.kefs.copy()
        copy[rnd_kef_num] *= random.uniform(kef_min, kef_max)
        return copy
