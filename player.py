import os
import pygame
import env


class Player(pygame.sprite.Sprite):
    speed = 5

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(env.BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (env.WIDTH / 2, env.HEIGHT / 2)

    def update(self):
        mouse_position = pygame.mouse.get_pos()
        x_dif = mouse_position[0] - self.rect.center[0]
        y_dif = mouse_position[1] - self.rect.center[1]

        x_move = 0
        if (x_dif < -self.speed):
            x_move = -self.speed / (1 + (y_dif / x_dif).__abs__())
        elif (x_dif > self.speed):
            x_move = self.speed / (1 + (y_dif / x_dif).__abs__())
        elif (x_dif.__abs__() > 1):
            x_move = x_dif / (1 + (y_dif / x_dif).__abs__())

        y_move = 0
        if (y_dif < -self.speed):
            y_move = -self.speed / (1 + (x_dif / y_dif).__abs__())
        elif (y_dif > self.speed):
            y_move = self.speed / (1 + (x_dif / y_dif).__abs__())
        elif (y_dif.__abs__() > 1):
            y_move = y_dif / (1 + (x_dif / y_dif).__abs__())

        self.rect.x += int(x_move)
        self.rect.y += int(y_move)

        if self.rect.left > env.WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = env.WIDTH

        if self.rect.bottom < 0:
            self.rect.top = env.HEIGHT
        elif self.rect.top > env.HEIGHT:
            self.rect.bottom = 0
