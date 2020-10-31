from typing import Tuple
import pygame


def collide_rec(rect1: pygame.Rect, rect2: pygame.Rect, offset: int) -> Tuple[bool, bool, bool, bool]:
    # top
    if rect1.collidepoint(rect2.left + offset, rect2.bottom) != 0 or \
            rect1.collidepoint(rect2.right - offset, rect2.bottom) != 0:
        return (True, False, False, False)
    # right
    elif rect1.collidepoint(rect2.left, rect2.bottom - offset) != 0 or \
            rect1.collidepoint(rect2.left, rect2.top + offset) != 0:
        return (False, True, False, False)
    # bottom
    elif rect1.collidepoint(rect2.left + offset, rect2.top) != 0 or \
            rect1.collidepoint(rect2.right - offset, rect2.top) != 0:
        return (False, False, True, False)
    # left
    elif rect1.collidepoint(rect2.right, rect2.bottom - offset) != 0 or \
            rect1.collidepoint(rect2.right, rect2.top + offset) != 0:
        return (False, False, False, True)
    else:
        return (False, False, False, False)


def tuples_plus(i: Tuple[int, ...], j: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(x + y for x, y in zip(i, j))
