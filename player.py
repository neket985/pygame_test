import common
import pygame
import env


class Player(pygame.sprite.Sprite):
    speed = 6
    move_state = (0, 0)

    tik_moves_buffer = set([])
    perm_move_state = (0, 0)

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(env.BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (env.WIDTH / 2, env.HEIGHT / 2)

    def update(self):
        move_x = 0
        if self.move_state[0]!=0 :
            move_x = (self.move_state[0].__abs__()/self.move_state[0])*\
                     self.speed/\
                     (1+(self.move_state[1]/self.move_state[0]).__abs__())

        move_y = 0
        if self.move_state[1]!=0 :
            move_y = (self.move_state[1].__abs__()/self.move_state[1])*\
                     self.speed/\
                     (1+(self.move_state[0]/self.move_state[1]).__abs__())

        move_x += self.perm_move_state[0]
        move_y += self.perm_move_state[1]

        self.rect.x += int(move_x)
        self.rect.y += int(move_y)

        if self.rect.right > env.WIDTH:
            self.rect.right = env.WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > env.HEIGHT:
            self.rect.bottom = env.HEIGHT

        self.tik_moves_buffer.clear()
        self.perm_move_state = (0, 0)

    def move_start(self, key):
        if env.KEY_LEFT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif env.KEY_RIGHT.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif env.KEY_DOWN.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, 1), self.move_state)
        elif env.KEY_UP.__contains__(key):
            self.tik_moves_buffer.add(key)
            self.move_state = common.tuples_plus((0, -1), self.move_state)

    def move_end(self, key):
        if self.tik_moves_buffer.__contains__(key):
            if env.KEY_LEFT.__contains__(key):
                self.perm_move_state = common.tuples_plus((-1, 0), self.perm_move_state)
            elif env.KEY_RIGHT.__contains__(key):
                self.perm_move_state = common.tuples_plus((1, 0), self.perm_move_state)
            elif env.KEY_DOWN.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, 1), self.perm_move_state)
            elif env.KEY_UP.__contains__(key):
                self.perm_move_state = common.tuples_plus((0, -1), self.perm_move_state)

        if env.KEY_LEFT.__contains__(key):
            self.move_state = common.tuples_plus((1, 0), self.move_state)
        elif env.KEY_RIGHT.__contains__(key):
            self.move_state = common.tuples_plus((-1, 0), self.move_state)
        elif env.KEY_DOWN.__contains__(key):
            self.move_state = common.tuples_plus((0, -1), self.move_state)
        elif env.KEY_UP.__contains__(key):
            self.move_state = common.tuples_plus((0, 1), self.move_state)

