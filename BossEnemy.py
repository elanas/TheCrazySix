from Enemy import Enemy
from ChaseEnemy import ChaseEnemy
import os
from asset_loader import AssetLoader
from FileManager import FileManager
from Player import Player
from Globals import Globals


class BossEnemy(ChaseEnemy):
    COLLISION_OFFSET = -20
    MIN_DIRECTION_CHANGE_TIME = .5
    MIN_DISTANCE_CHECK = .4
    HIT_BONUS = 10
    KILL_BONUS = 100
    FINAL_TILE_RADIUS = 15
    WALKING_PATH = os.path.join('images', 'scientist')
    PREFIX_PATH = os.path.join('scientist')
    WALKING_DOWN_PATH = 'walking_down'
    WALKING_UP_PATH = 'walking_up'
    WALKING_LEFT_PATH = 'walking_left'
    WALKING_RIGHT_PATH = 'walking_right'
    walking_images = [None, None, None, None]
    INIT_HEALTH = 100
    JUMP_DIST = 5

    def __init__(self, camera, x=None, y=None):
        super(BossEnemy, self).__init__(
            camera, x=x, y=y, min_dist_check=0,
            kill_bonus=BossEnemy.KILL_BONUS)
        self.first_find = False
        self.health = BossEnemy.INIT_HEALTH

    def loadResources(self):
        loader = AssetLoader('images')
        if BossEnemy.walking_images[Enemy.INDEX_DOWN] is None:
            path = os.path.join(BossEnemy.WALKING_PATH, BossEnemy.WALKING_DOWN_PATH)
            prefix_path = os.path.join(BossEnemy.PREFIX_PATH, BossEnemy.WALKING_DOWN_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            BossEnemy.walking_images[Enemy.INDEX_DOWN] = \
                loader.load_images(fM.get_files(prefix_path=prefix_path))
        if BossEnemy.walking_images[Enemy.INDEX_UP] is None:
            path = os.path.join(BossEnemy.WALKING_PATH, BossEnemy.WALKING_UP_PATH)
            prefix_path = os.path.join(BossEnemy.PREFIX_PATH, BossEnemy.WALKING_UP_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            BossEnemy.walking_images[Enemy.INDEX_UP] = \
                loader.load_images(fM.get_files(prefix_path=prefix_path))
        if BossEnemy.walking_images[Enemy.INDEX_LEFT] is None:
            path = os.path.join(BossEnemy.WALKING_PATH, BossEnemy.WALKING_LEFT_PATH)
            prefix_path = os.path.join(BossEnemy.PREFIX_PATH, BossEnemy.WALKING_LEFT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            BossEnemy.walking_images[Enemy.INDEX_LEFT] = \
                loader.load_images(fM.get_files(prefix_path=prefix_path))
        if BossEnemy.walking_images[Enemy.INDEX_RIGHT] is None:
            path = os.path.join(BossEnemy.WALKING_PATH, BossEnemy.WALKING_RIGHT_PATH)
            prefix_path = os.path.join(BossEnemy.PREFIX_PATH, BossEnemy.WALKING_RIGHT_PATH)
            fM = FileManager(path, file_ext='.png', create_dir=False)
            BossEnemy.walking_images[Enemy.INDEX_RIGHT] = \
                loader.load_images(fM.get_files(prefix_path=prefix_path))

    def get_images(self):
        return BossEnemy.walking_images[self.direction]

    def update(self, time, camera, player):
        result = super(BossEnemy, self).update(time, camera, player, False)

    def player_in_radius(self, time):
        result = super(BossEnemy, self).player_in_radius(time)
        if result and self.first_find:
            self.first_find = False
            self.chase_radius = self.tile_size * BossEnemy.FINAL_TILE_RADIUS
        return result

    def handle_hit(self, camera, player):
        self.health -= 1
        Globals.PLAYER_SCORE += BossEnemy.HIT_BONUS
        if self.health == 0:
            self.is_alive = False
            Globals.PLAYER_SCORE += self.kill_bonus
        self.jump_back(camera, player)

    def jump_back(self, camera, player):
        r = player.get_punching_rect()
        old_pos = self.rect.topleft
        if player.direction == Player.INDEX_DOWN:
            self.rect.top = r.bottom + BossEnemy.JUMP_DIST
        elif player.direction == Player.INDEX_UP:
            self.rect.bottom = r.top - BossEnemy.JUMP_DIST
        elif player.direction == Player.INDEX_RIGHT:
            self.rect.left = r.right + BossEnemy.JUMP_DIST
        elif player.direction == Player.INDEX_LEFT:
            self.rect.right = r.left - BossEnemy.JUMP_DIST
        self.checkCollisions(camera, avoid_stairs=True, direct=player.direction)
