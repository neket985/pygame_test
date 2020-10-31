import pygame

import common
import env
import flower
import girl
import player
from top_menu import TopMenu


class Window:
    flowers_count = 10

    def __init__(self):
        # создаем игру и окно
        pygame.init()
        pygame.mixer.init()  # для звука
        self.screen = pygame.display.set_mode((env.WIDTH, env.HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.restart()

    def onEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.restart()
            else:
                self.player.move_start(event.key)
        elif event.type == pygame.KEYUP:
            self.player.move_end(event.key)

    def update(self):
        if self.finish:
            return

        self.all_sprites.update()

        collided = pygame.sprite.spritecollide(self.player, self.flower_sprites, False,
                                               pygame.sprite.collide_rect_ratio(0.7))
        for i in collided:
            self.flower_sprites.remove(i)
            self.top_menu.flowers_count = self.flower_sprites.__len__()

        if pygame.sprite.spritecollide(self.player, self.girl_sprites, False):
            if self.flower_sprites.__len__() == 0:
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

        if self.top_menu.getExpireTime() == 0:
            print("Поражение")
            self.finish = True

    def draw(self):
        self.screen.fill(env.GREEN)
        self.girl_sprites.draw(self.screen)
        self.flower_sprites.draw(self.screen)
        self.all_sprites.draw(self.screen)

    def restart(self):
        self.finish = False
        self.all_sprites = pygame.sprite.Group()
        self.player = player.Player(self.clock)
        self.girl_sprites = pygame.sprite.Group()
        self.girl = girl.Girl()
        self.girl_sprites.add(self.girl)

        self.flower_sprites = pygame.sprite.Group()
        for i in range(self.flowers_count):
            self.flower_sprites.add(flower.Flower())

        self.top_menu = TopMenu(self.flower_sprites.__len__())
        self.all_sprites.add(self.player, self.top_menu)
