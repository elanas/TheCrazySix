import os
import pygame
import math
from Enemy import Enemy
from Character import Character
from asset_loader import AssetLoader
from Globals import Globals
from Player import Player


class ChaseEnemy(Enemy):
    CHASE_TILE_RADIUS = 8
    CHASE_RADIUS = None
    COLLISION_OFFSET = -10
    MIN_DIRECTION_CHANGE_TIME = .5
    CHASE_VELOCITY = Player.MOVE_VELOCITY * 2 / 3

    def __init__(self, camera, x=None, y=None):
        super(ChaseEnemy, self).__init__(camera=camera, x=x, y=y)
        self.tile_size = max(camera.tileEngine.get_tile_rect().size)
        if ChaseEnemy.CHASE_RADIUS is None:
            ChaseEnemy.CHASE_RADIUS = \
                self.tile_size * ChaseEnemy.CHASE_TILE_RADIUS
        self.time_since_change = ChaseEnemy.MIN_DIRECTION_CHANGE_TIME

    def update(self, time, camera, player):
        self.enemy_point = self.rect.center
        self.player_point = player.rect.center
        if not self.player_in_radius(player):
            self.velocity = Enemy.MOVE_VELOCITY
            super(ChaseEnemy, self).update(time, camera, player)
        else:
            self.velocity = ChaseEnemy.CHASE_VELOCITY
            self.checkCollisions(camera)
            self.update_chase(time, player)
            super(ChaseEnemy, self).update(time, camera, player,
                change_direction=False)

    def update_chase(self, time, player):
        temp_rect = self.rect.inflate(
            ChaseEnemy.COLLISION_OFFSET, ChaseEnemy.COLLISION_OFFSET)
        if temp_rect.colliderect(player.rect):
            self.moving = False
            return
        self.time_since_change += time
        if self.time_since_change >= ChaseEnemy.MIN_DIRECTION_CHANGE_TIME:
            self.time_since_change = 0
        else:
            return
        self.moving = True
        angle = ChaseEnemy.angle_to(self.enemy_point, self.player_point)
        dist = ChaseEnemy.distance(self.enemy_point, self.player_point)
        x_diff = dist * math.cos(angle)
        y_diff = dist * math.sin(angle)
        if math.fabs(x_diff) > math.fabs(y_diff):
            new_direct = Enemy.INDEX_LEFT if x_diff < 0 else Enemy.INDEX_RIGHT
        else:
            new_direct = Enemy.INDEX_UP if y_diff < 0 else Enemy.INDEX_DOWN
        self.setDirection(new_direct)

    def player_in_radius(self, player):
        return ChaseEnemy.distance(self.enemy_point, self.player_point) <= \
            ChaseEnemy.CHASE_RADIUS

    @staticmethod
    def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    @staticmethod
    def angle_to(p0, p1):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        return math.atan2(dy, dx) 