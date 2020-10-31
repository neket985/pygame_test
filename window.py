import pygame
import player
import env
import apple


class Window:
    apples_count = 10

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
        collided = pygame.sprite.spritecollide(self.player, self.apple_sprites, False)
        for i in collided:
            self.apple_sprites.remove(i)

        self.all_sprites.update()
        self.apple_sprites.update()

    def draw(self):
        self.screen.fill(env.BLACK)
        self.all_sprites.draw(self.screen)
        self.apple_sprites.draw(self.screen)

    def restart(self):
        self.all_sprites = pygame.sprite.Group()
        self.player = player.Player()
        self.all_sprites.add(self.player)

        self.apple_sprites = pygame.sprite.Group()
        for i in range(self.apples_count):
            self.apple_sprites.add(apple.Apple())


