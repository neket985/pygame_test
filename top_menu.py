import datetime

import pygame
from pygame import Surface
from pygame.sprite import Sprite

import env


class TopMenu(Sprite):
    timer = 30
    flowers_count = 0
    width = 500
    height = 60

    def __init__(self):
        self.start_at = int(datetime.datetime.utcnow().timestamp())
        self.finish_at = None
        self.finished = False
        Sprite.__init__(self)
        self.render()

    def update(self, *args, **kwargs) -> None:
        self.render()

    def render(self):
        self.image = Surface((self.width, self.height))
        self.image.set_colorkey(env.BLACK)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, env.WHITE, (0, 0, self.width, self.height), 2, 3)

        expire_after = self.getExpireTime()
        font = pygame.font.Font(pygame.font.get_default_font(), 30)
        text = font.render(str(self.flowers_count) + '   ' + str(expire_after), False, env.WHITE)
        text_rect = text.get_rect()
        text_rect.midleft = self.rect.midleft
        text_rect.left += 10
        self.image.blit(text, text_rect)

    def getExpireTime(self) -> int:
        if self.finished:
            expire_after = self.timer - (self.finish_at - self.start_at)
        else:
            now = int(datetime.datetime.utcnow().timestamp())
            expire_after = self.timer - (now - self.start_at)

        if expire_after < 0:
            expire_after = 0

        return expire_after

    def finish(self):
        self.finish_at = int(datetime.datetime.utcnow().timestamp())
        self.finished = True
