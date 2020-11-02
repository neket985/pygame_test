from typing import Dict

import pygame
from pygame.sprite import Group

import common
import env
import flower
import girl
import player
from bot import Bot
from moved_entity import MovedEntity
from top_menu import TopMenu


class Window:
    flowers_count = 10
    bots_count = 200
    childs_count = 20

    def __init__(self):
        # создаем игру и окно
        pygame.init()
        pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((env.WIDTH, env.HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.finish = False
        self.restart()

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.finish = True
                self.restart()
            else:
                self.player.move_start(event.key)
                self.girl.move_start(event.key)
        elif event.type == pygame.KEYUP:
            self.player.move_end(event.key)
            self.girl.move_end(event.key)

    def update(self):
        if self.finish:
            self.restart()
            return

        # ход ботов
        for b in self.bots:
            b.auto_step()

        self.all_sprites.update()
        self.girl_sprites.update()

        for plyr in self.flower_sprites:
            collided = pygame.sprite.spritecollide(plyr, self.flower_sprites[plyr], False,
                                                   pygame.sprite.collide_rect_ratio(0.7))
            for i in collided:
                self.flower_sprites[plyr].remove(i)
                self.top_menu.flowers_count = self.flower_sprites.__len__()

        self.check_win(self.player)
        for b in self.bots:
            self.check_win(b)

        if self.top_menu.getExpireTime() == 0:
            print("Поражение")
            self.finish = True

    def check_win(self, plyr):
        if pygame.sprite.spritecollide(plyr, self.girl_sprites, False):
            if self.flower_sprites[plyr].__len__() == 0:
                self.top_menu.finish()
                print("Победа")
                self.finish = True
            girl_collided = common.collide_rec(self.player.rect, self.girl.rect, self.player.speed + 1)
            if girl_collided[0]:
                self.player.rect.top = self.girl.rect.bottom
            elif girl_collided[1]:
                self.player.rect.right = self.girl.rect.left
            elif girl_collided[2]:
                self.player.rect.bottom = self.girl.rect.top
            elif girl_collided[3]:
                self.player.rect.left = self.girl.rect.right

    def draw(self):
        self.screen.fill(env.GREEN)
        self.girl_sprites.draw(self.screen)
        [self.flower_sprites[i].draw(self.screen) for i in self.flower_sprites]
        self.all_sprites.draw(self.screen)

    def restart(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = player.Player()
        self.girl_sprites = pygame.sprite.Group()
        self.girl = girl.Girl()
        self.girl_sprites.add(self.girl)

        if self.finish:
            self.refresh_bots()
        else:
            self.bots = [Bot(pygame.sprite.Group(), self.girl, self.flowers_count) for i in range(self.bots_count)]

        self.flower_sprites: Dict[MovedEntity, Group] = \
            dict([(self.player, pygame.sprite.Group())] + [(b, b.flowers) for b in self.bots])

        for plyr in self.flower_sprites:
            for i in range(self.flowers_count):
                self.flower_sprites[plyr].add(flower.Flower())

        self.top_menu = TopMenu(self.flower_sprites[self.player].__len__())
        self.all_sprites.add(*self.bots, self.player, self.top_menu)
        self.finish = False

    def refresh_bots(self):  # todo брать 10% лучших и разводить от них потомство. подумать над реорганизацией кэфов
        sorted_scores = self.bots.copy()
        sorted_scores.sort(key=lambda x: x.get_score(), reverse=True)
        best_bot = sorted_scores[0]
        print('Лучший!')
        print('Цветов осталось не собрано ' + str(best_bot.flowers.__len__()))
        print('Очки ' + str(best_bot.score))
        print(best_bot.kefs)

        ten_percent_count = sorted_scores.__len__() // self.childs_count
        best_bots = sorted_scores[0:ten_percent_count]

        new_bots_scores = []
        for bot in best_bots:
            new_bots_scores.__iadd__(bot.get_child_kefs(self.childs_count - 1).__add__([bot.kefs]))
        self.bots = [Bot(pygame.sprite.Group(), self.girl, self.flowers_count, kefs) for kefs in new_bots_scores]
