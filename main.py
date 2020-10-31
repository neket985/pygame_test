import pygame
import env
import window

window = window.Window()

# Цикл игры
running = True
while running:
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
            break
        else: window.onEvent(event)

    # Если при прочтени списка событий, в нем не было события закрытия окна
    else:
        # Обновление
        window.update()

        # Рендеринг
        window.draw()
        # держим цикл на правильной скорости
        window.clock.tick(env.FPS)
        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()

pygame.quit()
