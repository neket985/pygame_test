import pygame
import env
import player
import apple

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((env.WIDTH, env.HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()


all_sprites = pygame.sprite.Group()
player = player.Player()
all_sprites.add(player)

all_sprites.add(apple.Apple(), apple.Apple(), apple.Apple(), apple.Apple(), apple.Apple(), apple.Apple())

# Цикл игры
running = True
while running:
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
            break
    # Если при прочтени списка событий, в нем не было события закрытия окна
    else:
        # Обновление
        for i in all_sprites:
            if(isinstance(i, apple.Apple)):
                if (i.rect.right > player.rect.left and \
                        i.rect.left < player.rect.right and \
                        i.rect.bottom > player.rect.top and \
                        i.rect.top < player.rect.bottom):
                    all_sprites.remove(i)

        all_sprites.update()

        # Рендеринг
        screen.fill(env.BLACK)
        all_sprites.draw(screen)
        # держим цикл на правильной скорости
        clock.tick(env.FPS)
        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()

pygame.quit()
