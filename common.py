import pygame


def aabb(mob: pygame.sprite.Sprite, player: pygame.sprite.Sprite) -> bool:
    return mob.rect.right > player.rect.left and \
           mob.rect.left < player.rect.right and \
           mob.rect.bottom > player.rect.top and \
           mob.rect.top < player.rect.bottom


def tuples_plus(i: tuple[int, ...], j: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(i, j))
