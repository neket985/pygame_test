import pygame
import datetime

WIDTH = 360  # ширина игрового окна
HEIGHT = 480 # высота игрового окна
FPS = 3 # частота кадров в секунду

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

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

        # Рендеринг
        screen.fill(BLACK)
        # держим цикл на правильной скорости
        clock.tick(FPS)
        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()

pygame.quit()
