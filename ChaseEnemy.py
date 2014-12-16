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
    COLLISION_OFFSET = -20
    MIN_DIRECTION_CHANGE_TIME = .5
    MIN_DISTANCE_CHECK = .4
    CHASE_VELOCITY = Player.MOVE_VELOCITY * 2 / 3
    KILL_BONUS = 10

    def __init__(self, camera, x=None, y=None,
                 min_dist_check=MIN_DISTANCE_CHECK,
                 chase_tile_radius=CHASE_TILE_RADIUS,
                 kill_bonus=KILL_BONUS):
        super(ChaseEnemy, self).__init__(
            camera=camera, x=x, y=y, kill_bonus=kill_bonus)
        self.tile_size = max(camera.tileEngine.get_tile_rect().size)
        self.chase_radius = self.tile_size * chase_tile_radius
        self.min_dist_check = min_dist_check
        self.time_since_dist_check = 0
        self.time_since_change = ChaseEnemy.MIN_DIRECTION_CHANGE_TIME
        self.last_dist_check = False
        self.last_d = self.direction

    def update(self, time, camera, player, act_normal=True):
        self.enemy_point = self.rect.center
        self.player_point = player.rect.center
        if not self.player_in_radius(time):
            if act_normal:
                self.velocity = Enemy.MOVE_VELOCITY
                super(ChaseEnemy, self).update(time, camera, player)
            return False
        else:
            self.velocity = ChaseEnemy.CHASE_VELOCITY
            self.update_chase(time, player)
            self.checkCollisions(camera, avoid_stairs=True, direct=self.last_d)
            self.last_d = self.direction
            super(ChaseEnemy, self).update(time, camera, player,
                                           change_direction=False)
            return True

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

    def player_in_radius(self, time):
        self.time_since_dist_check += time
        if self.last_dist_check or \
                self.time_since_dist_check >= self.min_dist_check:
            self.time_since_dist_check = 0
        else:
            return self.last_dist_check
        self.last_dist_check = ChaseEnemy.distance(
            self.enemy_point, self.player_point) <= self.chase_radius
        return self.last_dist_check

    @staticmethod
    def distance(p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    @staticmethod
    def angle_to(p0, p1):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        return math.atan2(dy, dx)
