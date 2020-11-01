import os
import env
from moved_entity import MovedEntity


class Player(MovedEntity):

    def __init__(self):
        self.load_images(os.path.join(env.img_folder, 'characters.png'), (3 * 16, 0, 3 * 16, 4 * 16), (16, 16))
        MovedEntity.__init__(self, env.PLAYER_KEY_LEFT, env.PLAYER_KEY_RIGHT, env.PLAYER_KEY_UP, env.PLAYER_KEY_DOWN)

        self.image = self.getSpriteByTik()
        self.rect = self.image.get_rect(center=(env.WIDTH / 2, env.HEIGHT / 2))
