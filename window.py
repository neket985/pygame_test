from typing import Dict

import pygame
from pygame.sprite import Group

import common
import env
import flower
import girl
import player
from bot import Bot
from map import Map
from moved_entity import MovedEntity
from top_menu import TopMenu


class Window:
    flowers_count = 10
    bots_count = 50
    parents_count = 8
    childs_count = 5
    bot_kefs = None
    # bot_kefs = [0.2992764625884063, -0.45111985831907364, 0.034324156383470195, 0.7420118143078578, 0.20305567116814527,
    #             0.24585005882518152, 0.4715142168897148, -0.15017876205188951, -0.14998973648173874, 0.4929961834415246,
    #             -0.006712253240808777]

    def __init__(self):
        # создаем игру и окно
        pygame.init()
        pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((env.WIDTH, env.HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.finish = False
        self.gen = 0
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
            # print("Поражение")
            self.finish = True

    def check_win(self, plyr):
        if pygame.sprite.spritecollide(plyr, self.girl_sprites, False):
            if self.flower_sprites[plyr].__len__() == 0:
                if self.finish:
                    distance = ((plyr.rect.center[0] - self.girl.rect.center[0]) ** 2 + (
                            plyr.rect.center[0] - self.girl.rect.center[0]) ** 2) ** 0.5
                    plyr.score += 100 * distance
                else:
                    self.top_menu.finish()
                    print('Winner')
                    print('Gen ' + str(plyr.gen) + '(' + str(self.gen) + ')')
                    print('Time ' + str(self.top_menu.getExpireTime()))
                    print(plyr.kefs)
                    plyr.score += 1_000_000
                    self.finish = True
            girl_collided = common.collide_rec(plyr.rect, self.girl.rect, plyr.speed + 1)
            if girl_collided[0]:
                plyr.rect.top = self.girl.rect.bottom
            elif girl_collided[1]:
                plyr.rect.right = self.girl.rect.left
            elif girl_collided[2]:
                plyr.rect.bottom = self.girl.rect.top
            elif girl_collided[3]:
                plyr.rect.left = self.girl.rect.right

    def draw(self):
        self.screen.fill(env.GREEN)
        self.all_sprites.draw(self.screen)
        self.girl_sprites.draw(self.screen)
        [self.flower_sprites[i].draw(self.screen) for i in self.flower_sprites]

    def restart(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = player.Player()
        self.girl_sprites = pygame.sprite.Group()
        self.girl = girl.Girl()
        self.girl_sprites.add(self.girl)

        if self.finish:
            self.refresh_bots()
        else:
            self.bots = [Bot(pygame.sprite.Group(), self.girl, self.flowers_count, self.gen, self.bot_kefs) for i in
                         range(self.bots_count)]

        self.flower_sprites: Dict[MovedEntity, Group] = \
            dict([(self.player, pygame.sprite.Group())] + [(b, b.flowers) for b in self.bots])

        for i in range(self.flowers_count):
            self.flower_sprites[self.player].add(flower.Flower())

        for bot in self.bots:
            for i in self.flower_sprites[self.player]:
                self.flower_sprites[bot].add(flower.Flower(i.rect.center))

        self.top_menu = TopMenu(self.flower_sprites[self.player].__len__(), self.gen)
        self.all_sprites.add(Map(), *self.bots, self.player, self.top_menu)

        # удаление управляемого игрока с поля
        self.all_sprites.remove(self.player)
        self.flower_sprites.pop(self.player)
        # ------------------------------------

        self.finish = False

    def refresh_bots(self):
        self.gen += 1
        sorted_scores = self.bots.copy()
        sorted_scores.sort(key=lambda x: x.get_score(), reverse=True)

        best_bots = sorted_scores[0:self.parents_count]

        new_bots = []
        for bot in best_bots:
            new_bots.__iadd__([Bot(pygame.sprite.Group(), self.girl, self.flowers_count, bot.gen, kefs) for kefs in
                               bot.get_child_kefs(self.childs_count - 1).__add__([bot.kefs])])

        self.bots = new_bots.__iadd__([Bot(pygame.sprite.Group(), self.girl, self.flowers_count, self.gen) for i in
                                       range(self.bots_count - new_bots.__len__())])
