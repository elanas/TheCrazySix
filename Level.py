from GameState import GameState
from Globals import Globals
from GameState import GameState
from TileEngine import TileEngine
from TileType import TileType
from Camera import Camera
from Player import Player
from Enemy import Enemy
from os.path import join
import pygame
from Turret import Turret
from HealthBar import HealthBar


class Level(GameState):
    MAP_BASE = "maps"
    MAX_OFFSET_X = 150
    MAX_OFFSET_Y = 75
    FACTOR = 10

    def __init__(self, definition_path, map_path):
        self.keyCode = None
        self.definition_path = definition_path
        self.map_path = map_path
        self.tile_engine = TileEngine(
            join(Level.MAP_BASE, definition_path),
            join(Level.MAP_BASE, map_path)
        )
        self.camera = Camera(self.tile_engine, pygame.Rect(
            0, 0, Globals.WIDTH, Globals.HEIGHT))
        self.tile_rect = self.tile_engine.get_tile_rect()
        self.enemySprites = pygame.sprite.Group()
        self.playerSprites = pygame.sprite.Group()
        self.turrets = list()
        self.init_player()
        self.init_enemies()
        if Globals.HEALTH_BAR is None:
            Globals.HEALTH_BAR = HealthBar()

    def handle_stairs(self):
        pass

    def handle_escape(self):
        pass

    def handle_enemy_collision(self):
        pass

    def handle_special_collision(self, pair):
        self.replace_special_tile(pair)

    def replace_special_tile(self, pair):
        if pair.tile.is_replaceable:
            row, col = self.camera.tileEngine.get_tile_pos(pair.coords[0],
                                                           pair.coords[1])
            base = self.camera.tileEngine.get_tile_from_attr(
                pair.tile.replace_attr)
            if base is None:
                base = self.camera.tileEngine.get_tile_from_attr(
                    TileType.BASE_ATTR)
            self.camera.tileEngine.tileMap[row][col] = base

    def init_player(self):
        self.player = Player(
            Globals.WIDTH, Globals.HEIGHT,
            Globals.WIDTH / 2, Globals.HEIGHT / 2
        )
        self.playerSprites.add(self.player)

    def init_enemies(self):
        tile_map = self.tile_engine.tileMap
        base_tile = self.tile_engine.get_tile_from_attr(TileType.BASE_ATTR)
        for row_num in range(0, len(tile_map)):
            for col_num in range(0, len(tile_map[row_num])):
                if tile_map[row_num][col_num] is None:
                    continue
                if TileType.SPAWN_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_enemy(row_num, col_num)
                    tile_map[row_num][col_num] = base_tile
                elif TileType.TURRET_LEFT in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_turret(row_num, col_num, True)
                elif TileType.TURRET_RIGHT in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_turret(row_num, col_num, False)

    def add_enemy(self, row_num, col_num):
        y = self.tile_rect.height * row_num - self.camera.viewpoint.top
        x = self.tile_rect.width * col_num - self.camera.viewpoint.left
        self.enemySprites.add(Enemy(Globals.WIDTH, Globals.HEIGHT, x=x, y=y))

    def add_turret(self, row_num, col_num, left):
        row_num += 1
        if not left:
            col_num += 1
        y = self.tile_rect.height * row_num - self.camera.viewpoint.top
        x = self.tile_rect.width * col_num - self.camera.viewpoint.left
        self.turrets.append(Turret(x, y, left))

    def check_collisions(self):
        # radius = max(self.player.rect.size) * 1.5
        # center = self.player.rect.center
        for turret in self.turrets:
            for syringe in turret.syringeSprites:
                if self.player.rect.colliderect(syringe):
                    Globals.HEALTH_BAR.changeHealth(syringe.health_effect)
                    Globals.HEALTH_BAR.printHealth()
                    syringe.kill()

    def render(self):
        self.camera.render(Globals.SCREEN)
        self.enemySprites.draw(Globals.SCREEN)
        for turret in self.turrets:
            turret.render(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)
        Globals.HEALTH_BAR.render(Globals.SCREEN)


    def update(self, time):
        Globals.HEALTH_BAR.update(time)
        self.player.update(time, self.camera, self.enemySprites, self)
        self.enemySprites.update(time, self.camera)
        for turret in self.turrets:
            turret.update(time, self.camera)
        self.checkCameraPosition()
        self.check_collisions()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reload_level()
            elif event.key == pygame.K_ESCAPE:
                self.handle_escape()
            else:
                self.keyCode = event.key
                for p in self.playerSprites:
                    p.keyPressed(event.key)
        elif event.type == pygame.KEYUP and event.key == self.keyCode:
            self.keyCode = None
            for p in self.playerSprites:
                p.keyReleased(event.key)

    def checkCameraPosition(self):
        dist_x = self.camera.container.centerx - self.player.rect.centerx
        dist_y = self.camera.container.centery - self.player.rect.centery
        if abs(dist_x) > Level.MAX_OFFSET_X:
            diff = abs(dist_x) - Level.MAX_OFFSET_X
            # player is to the right of center
            if dist_x < 0:
                pass
            # player is to the left of center
            else:
                diff *= -1
            self.camera.move(diff, 0)
            self.player.rect.centerx -= diff
            for enemy in self.enemySprites:
                enemy.rect.centerx -= diff
            for turret in self.turrets:
                turret.move(-diff, 0)
        if abs(dist_y) > Level.MAX_OFFSET_Y:
            diff = abs(dist_y) - Level.MAX_OFFSET_Y
            # player is below center
            if dist_y < 0:
                pass
            # player is above center
            else:
                diff *= -1
            self.camera.move(0, diff)
            self.player.rect.centery -= diff
            for enemy in self.enemySprites:
                enemy.rect.centery -= diff
            for turret in self.turrets:
                turret.move(0, -diff)

    def reload_level(self):
        try:
            new_state = Level(self.definition_path, self.map_path)
            Globals.STATE = new_state
            print "Reloaded level"
        except Exception as e:
            print "Reload failed: ", e
