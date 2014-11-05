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
import Menu
import WinGame


class Level(GameState):
    MAP_BASE = "maps"
    MAX_OFFSET_X = 150
    MAX_OFFSET_Y = 75
    FACTOR = 10
    ALPHA_FACTOR = 550
    MIN_ALPHA = 0
    MAX_ALPHA = 255

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
        self.black_surf = pygame.Surface(
            (Globals.WIDTH, Globals.HEIGHT)).convert()
        self.black_surf.fill((0, 0, 0))
        self.fade_in = False
        self.fade_out = False

    def got_current_state(self):
        self.start_fade_in()

    def handle_stairs(self):
        self.start_fade_out()
        pass

    def handle_escape(self):
        Globals.STATE = Menu.Menu()

    def handle_enemy_collision(self):
        pass

    def handle_special_collision(self, pair):
        self.replace_special_tile(pair)

    def handle_finish_fade_out(self):
        if not Globals.goto_next_level():
            self.handle_last_level()

    def handle_last_level(self):
        Globals.STATE = WinGame.WinGame()  # for now

    def handle_finish_fade_in(self):
        pass

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
                    syringe.kill()

    def render(self):
        self.render_pre_fade()
        if self.fade_out or self.fade_in:
            Globals.SCREEN.blit(self.black_surf, (0, 0))
        self.render_post_fade()

    def render_pre_fade(self):
        self.camera.render(Globals.SCREEN)
        self.enemySprites.draw(Globals.SCREEN)
        for turret in self.turrets:
            turret.render(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)

    def render_post_fade(self):
        Globals.HEALTH_BAR.render(Globals.SCREEN)

    def update(self, time):
        if self.fade_out or self.fade_in:
            self.update_alpha(time)
            return
        Globals.HEALTH_BAR.update(time)
        self.player.update(time, self.camera, self.enemySprites, self)
        self.enemySprites.update(time, self.camera)
        for turret in self.turrets:
            turret.update(time, self.camera)
        self.checkCameraPosition()
        self.check_collisions()

    def update_alpha(self, time):
        if self.fade_out:
            old_alpha = self.black_surf.get_alpha()
            new_alpha = int(old_alpha + time * Level.ALPHA_FACTOR)
            if new_alpha >= Level.MAX_ALPHA:
                self.handle_finish_fade_out()
                self.fade_out = False
            self.black_surf.set_alpha(new_alpha)
        elif self.fade_in:
            old_alpha = self.black_surf.get_alpha()
            new_alpha = int(old_alpha - time * Level.ALPHA_FACTOR)
            if new_alpha <= Level.MIN_ALPHA:
                self.handle_finish_fade_in()
                self.fade_in = False
            self.black_surf.set_alpha(new_alpha)
    
    def start_fade_out(self):
        self.black_surf.set_alpha(Level.MIN_ALPHA)
        self.fade_out = True

    def start_fade_in(self):
        self.black_surf.set_alpha(Level.MAX_ALPHA)
        self.fade_in = True

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
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
