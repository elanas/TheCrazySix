from GameState import GameState
from Globals import Globals
from GameState import GameState
from TileSystem.TileEngine import TileEngine
from TileSystem.TileType import TileType
from TileSystem.Camera import Camera
from Player import Player
from Character import Character
from Enemy import Enemy
from ChaseEnemy import ChaseEnemy
from os.path import join
import pygame
from Turret import Turret
from HealthBar import HealthBar
from ScoreTimer import ScoreTimer
import Menu
import WinGame
import LoseGame
from HighscoreManager import HighscoreManager
from PauseScreen import PauseScreen
from HUDManager import HUDManager
from asset_loader import AssetLoader
from LightSource import LightSource


class Level(GameState):
    MAP_BASE = "maps"
    MAX_OFFSET_X = 150
    MAX_OFFSET_Y = 75
    FACTOR = 10
    ALPHA_FACTOR = 550
    MIN_ALPHA = 0
    MAX_ALPHA = 255
    SUBTITLE_BACKGROUND = pygame.color.Color("black")
    SUBTITLE_PADDING = 5
    SUBTITLE_COLOR = pygame.color.Color("white")
    SUBTITLE_FONT = pygame.font.Font(None, 32)
    SUBTITLE_MARGIN = 20
    POTION_CURED_SUBTITLE = 'You have been cured'
    POTION_CURED_SUBTITLE_LOOPS = 5
    ACTION_TILE_HINT = 'Press the action key to use'
    ACTION_TILE_LOOPS = 1
    LOCKED_TILE_HINT = 'This is locked'
    LOCKED_TILE_LOOPS = 1
    HEALTH_PICKUP = 5
    DAMAGE_TRAP = -1
    POTION_PICKUP_DISORIENTED = 5
    POTION_PICKUP = 10
    PUNCHING_INFLATE = .2
    MUSIC_END_ID = pygame.USEREVENT
    SOUND_FADE_TIME = 500

    def __init__(self, definition_path, map_path, music_path=None, music_loops=-1,
                 has_timer=True, should_fade_in=True):
        self.has_timer = has_timer
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
        self.lights = list()
        self.init_player()
        self.init_enemies()
        self.timer = None
        if Globals.HEALTH_BAR is None:
            Globals.HEALTH_BAR = HealthBar()
        if Globals.HUD_MANAGER is None:
            Globals.HUD_MANAGER = HUDManager() 
        self.black_surf = pygame.Surface(
            (Globals.WIDTH, Globals.HEIGHT)).convert()
        self.black_surf.fill((0, 0, 0))
        self.fade_in = False
        self.fade_out = False
        self.showing_subtitle = False
        self.alpha_factor = 300
        self.should_fade_in = should_fade_in
        self.pausing = False
        self.going_back = False
        self.score_counted = False
        self.respawn_coords = [-1, -1]
        self.timer = None
        self.find_respawn()
        self.loader = AssetLoader('images', 'sounds')
        self.channel = None
        self.music_loops = music_loops
        if music_path is not None:
            self.music_handle = self.loader.load_sound(music_path)
        else:
            self.music_handle = None

    def start_music(self):
        if self.channel or self.music_handle is None:
            return
        self.channel = self.music_handle.play(
            loops=self.music_loops, fade_ms=Level.SOUND_FADE_TIME)
        self.channel.set_endevent(Level.MUSIC_END_ID)

    def pause_music(self):
        if self.channel:
            self.channel.pause()

    def resume_music(self):
        if self.channel:
            self.channel.unpause()

    def stop_music(self):
        if self.channel:
            self.channel.fadeout(Level.SOUND_FADE_TIME)
            self.channel = None

    def find_respawn(self):
        tile_map = self.tile_engine.tileMap
        for row_num in range(0, len(tile_map)):
            for col_num in range(0, len(tile_map[row_num])):
                if tile_map[row_num][col_num] is None:
                    continue
                if TileType.RESPAWN_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    if self.has_respawn_coords():
                        raise Exception(
                            "There can only be one respawn point in the map"
                        )
                    self.respawn_coords[0] = row_num
                    self.respawn_coords[1] = col_num
        if self.has_respawn_coords():
            tile_map[self.respawn_coords[0]][self.respawn_coords[1]] = \
                self.tile_engine.get_tile_from_attr(TileType.BASE_ATTR)

    def has_respawn_coords(self):
        return self.respawn_coords[0] != -1 and self.respawn_coords[1] != -1

    def got_current_state(self):
        diff = self.camera.initView()
        # print diff
        self.shift_non_player_objects(diff[0], diff[1])
        self.player.rect.center = Globals.SCREEN.get_rect().center
        if self.should_fade_in:
            self.start_fade_in()
        if self.has_timer and self.timer is None:
            self.timer = ScoreTimer()
        elif self.timer is not None:
            self.timer.unpause()
        Globals.stop_menu_sound()
        self.start_music()

    def got_state_back(self):
        if self.has_respawn_coords():
            diff = self.camera.set_viewpoint_with_coords(
                self.respawn_coords[0], self.respawn_coords[1])
            center = Globals.SCREEN.get_rect().center
            self.player.stop_and_set_direction(Character.INDEX_DOWN)
            self.player.rect.left = center[0] - 16
            self.player.rect.top = center[1]
            self.shift_non_player_objects(diff[0], diff[1])
            self.start_fade_in()
            self.start_music()
        else:
            raise Exception(
                "A respawn point must be defined to return to the level")

    def shift_non_player_objects(self, x_delta, y_delta):
        for enemy in self.enemySprites:
                enemy.rect.centerx += x_delta
                enemy.rect.centery += y_delta
        for turret in self.turrets:
            turret.move(x_delta, y_delta)

    def handle_stair_up(self):
        if not self.score_counted:
            self.score_counted = True
            Globals.PLAYER_SCORE += Globals.HEALTH_BAR.health
            if self.has_timer:
                time = self.timer.total_time / 1000
                diff = max(300 - time, 0)
                Globals.PLAYER_SCORE += diff
        self.going_back = False
        self.pausing = False
        self.start_fade_out()

    def handle_stair_down(self):
        self.going_back = True
        self.start_fade_out()

    def handle_enemy_collision(self):
        pass

    def handle_special_collision(self, pair):
        self.replace_special_tile(pair)
        if TileType.TRAP_ATTR in pair.tile.special_attr:
            Globals.HEALTH_BAR.changeHealth(Level.DAMAGE_TRAP)
            self.player.show_damage()
        elif TileType.HEALTH_ATTR in pair.tile.special_attr:
            Globals.HEALTH_BAR.changeHealth(Level.HEALTH_PICKUP)
        elif TileType.KEY_ATTR in pair.tile.special_attr:
            Globals.HUD_MANAGER.add_key()
        elif TileType.POTION_ATTR in pair.tile.special_attr:
            if Globals.DISORIENTED:
                Globals.DISORIENTED = False
                self.show_subtitle(Level.POTION_CURED_SUBTITLE,
                                   Level.POTION_CURED_SUBTITLE_LOOPS)
                self.player.stop_and_set_direction(self.player.direction)
                Globals.HEALTH_BAR.changeHealth(Level.POTION_PICKUP_DISORIENTED)
            else:
                Globals.HEALTH_BAR.changeHealth(Level.POTION_PICKUP)

    def handle_finish_fade_out(self):
        self.stop_music()
        if not Globals.goto_next_level():
            self.handle_last_level()

    def handle_last_level(self):
        manager = HighscoreManager()
        manager.add(Globals.PLAYER_NAME, Globals.PLAYER_SCORE)
        Globals.STATE = WinGame.WinGame()  # for now

    def handle_finish_fade_in(self):
        if self.timer is not None:
            self.timer.unpause()

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
            self.camera.set_dirty()

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
                    self.camera.set_dirty()
                elif TileType.CHASE_SPAWN_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_enemy(row_num, col_num, chase_enemy=True)
                    tile_map[row_num][col_num] = base_tile
                    self.camera.set_dirty()
                elif TileType.TURRET_LEFT in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_turret(row_num, col_num, True)
                elif TileType.TURRET_RIGHT in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_turret(row_num, col_num, False)
                elif TileType.LIGHT_REPLACE_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_light(row_num, col_num)
                    tile_map[row_num][col_num] = base_tile
                    self.camera.set_dirty()
                elif TileType.LIGHT_ATTR in \
                        tile_map[row_num][col_num].special_attr:
                    self.add_light(row_num, col_num)

    def add_light(self, row_num, col_num):
        y = self.tile_rect.height * (row_num - 1) - self.camera.viewpoint.top
        x = self.tile_rect.width * (col_num - 1) - self.camera.viewpoint.left
        self.lights.append(LightSource(x, y, self.tile_rect.width))

    def add_enemy(self, row_num, col_num, chase_enemy=False):
        y = self.tile_rect.height * row_num - self.camera.viewpoint.top
        x = self.tile_rect.width * col_num - self.camera.viewpoint.left
        if not chase_enemy:
            enemy = Enemy(Globals.WIDTH, Globals.HEIGHT, x=x, y=y)
        else:
            enemy = ChaseEnemy(camera=self.camera, x=x, y=y)
        self.enemySprites.add(enemy)


    def add_turret(self, row_num, col_num, left):
        row_num += 1
        if not left:
            col_num += 1
        y = self.tile_rect.height * row_num - self.camera.viewpoint.top
        x = self.tile_rect.width * col_num - self.camera.viewpoint.left
        self.turrets.append(Turret(x, y, left))

    def check_collisions(self):
        radius = max(self.player.rect.size) * 2
        self.check_turret_collisions()
        self.check_punching_collisions()
        self.enemySprites = pygame.sprite.Group([e for e in self.enemySprites if e.is_alive])
        self.check_enemy_collisions()
        special_tiles = self.camera.get_special_tiles(
            self.player.rect.center, radius)
        self.check_stair_collisions(special_tiles)
        self.check_special_collisions(special_tiles)
        self.check_action_hints()

    def check_action_hints(self):
        if self.showing_subtitle:
            return
        temp_rect = self.player.rect.inflate(
            Player.ACTION_OFFSET, Player.ACTION_OFFSET)
        radius = max(temp_rect.size) * 2
        special_tiles = self.camera.get_special_tiles(
            self.player.rect.center, radius)
        action_tiles = [pair for pair in special_tiles if
                        TileType.ACTION_ATTR in pair.tile.special_attr and
                        temp_rect.colliderect(pair.rect)]
        locked_tiles = [pair for pair in action_tiles if
                        TileType.LOCKED_ATTR in pair.tile.special_attr]
        if not Globals.HUD_MANAGER.has_key() and len(locked_tiles) > 0:
            self.show_subtitle(Level.LOCKED_TILE_HINT, Level.LOCKED_TILE_LOOPS)
        elif len(action_tiles) > 0:
            self.show_subtitle(Level.ACTION_TILE_HINT, Level.ACTION_TILE_LOOPS)

    def check_special_collisions(self, special_tiles):
        for pair in special_tiles:
            if self.player.rect.colliderect(pair.rect):
                self.handle_special_collision(pair)

    def check_stair_collisions(self, special_tiles):
        stair_up_rects = [pair.rect for pair in special_tiles
                          if TileType.STAIR_UP_ATTR in pair.tile.special_attr]
        temp_rect = self.player.rect.inflate(
            -Player.STAIR_OFFSET, -Player.STAIR_OFFSET)
        num_up_stairs = len(temp_rect.collidelistall(stair_up_rects))
        if num_up_stairs > 0:
            self.handle_stair_up()
        stair_down_rects = [pair.rect for pair in special_tiles if 
                            TileType.STAIR_DOWN_ATTR in pair.tile.special_attr]
        num_down_stairs = len(temp_rect.collidelistall(stair_down_rects))
        if num_down_stairs > 0:
            self.handle_stair_down()

    def check_enemy_collisions(self):
        enemy_rects = [enemy.rect.inflate(-20, -20) for enemy in self.enemySprites]
        player_rect = self.player.rect.copy()            
        if self.player.punching:
            # player_rect.inflate_ip(
            #     -player_rect.width * Level.PUNCHING_INFLATE,
            #     -player_rect.height * Level.PUNCHING_INFLATE)
            pass
        collided_indices = player_rect.collidelistall(enemy_rects)
        if len(collided_indices) > 0:
            self.handle_health_change(Enemy.HEALTH_EFFECT)

    def check_punching_collisions(self):
        if not self.player.punching:
            return
        punching_rect = self.player.get_punching_rect()
        for enemy in self.enemySprites:
            if punching_rect.colliderect(enemy.rect):
                enemy.handle_hit()

    def check_turret_collisions(self):
        for turret in self.turrets:
            for syringe in turret.syringeSprites:
                if self.player.rect.colliderect(syringe):
                    self.handle_health_change(syringe.health_effect)
                    syringe.kill()

    def handle_health_change(self, health_effect):
        Globals.HEALTH_BAR.changeHealth(health_effect)
        if health_effect < 0:
            self.player.show_damage()

    def render(self):
        self.render_pre_fade()
        if self.fade_out or self.fade_in:
            Globals.SCREEN.blit(self.black_surf, (0, 0))
        self.render_post_fade()
        # r = self.player.get_punching_rect()
        # if r is not None:
        #     Globals.SCREEN.fill((255, 255, 255), r)

    def render_pre_fade(self):
        self.camera.render(Globals.SCREEN)
        self.render_lights()
        self.enemySprites.draw(Globals.SCREEN)
        for turret in self.turrets:
            turret.render(Globals.SCREEN)
        self.playerSprites.draw(Globals.SCREEN)
        self.render_overlay()
        if self.has_timer and not self.score_counted:
            self.timer.render(Globals.SCREEN)
        if self.showing_subtitle:
            Globals.SCREEN.blit(self.subtitle_surf, self.subtitle_rect)

    def render_lights(self):
        for light in self.lights:
            light.render(Globals.SCREEN)

    def render_overlay(self):
        if Globals.DISORIENTED:
            Globals.SCREEN.blit(Globals.get_disoriented_surf(), (0, 0),
                special_flags=pygame.BLEND_SUB)

    def render_post_fade(self):
        Globals.HEALTH_BAR.render(Globals.SCREEN)
        Globals.HUD_MANAGER.render(Globals.SCREEN)

    def update(self, time):
        if Globals.HEALTH_BAR.is_dead():
            self.handle_lose_game()
        if self.fade_out or self.fade_in:
            self.update_alpha(time)
            return
        Globals.HEALTH_BAR.update(time)
        self.player.update(time, self.camera)
        self.enemySprites.update(time, self.camera, self.player)
        for turret in self.turrets:
            turret.update(time, self.camera)
        self.check_camera_position()
        self.check_collisions()
        self.update_subtitle(time)

    def handle_lose_game(self):
        Globals.STATE = LoseGame.LoseGame()

    def update_subtitle(self, time):
        if not self.showing_subtitle:
            return
        old_alpha = self.subtitle_surf.get_alpha()
        if old_alpha == 0 or old_alpha == 255:
            self.alpha_factor *= -1
            if self.subtitle_loops != -1:
                self.subtitle_loops -= 1
                if self.subtitle_loops == 0:
                    self.stop_subtitle()
        new_alpha = int(old_alpha + self.alpha_factor * time)
        if new_alpha < 0:
            new_alpha = 0
        elif new_alpha > 255:
            new_alpha = 255
        self.subtitle_surf.set_alpha(new_alpha)

    def update_alpha(self, time):
        if self.fade_out:
            old_alpha = self.black_surf.get_alpha()
            new_alpha = int(old_alpha + time * Level.ALPHA_FACTOR)
            if new_alpha >= Level.MAX_ALPHA:
                if self.pausing:
                    self.handle_pause()
                elif self.going_back:
                    self.handle_go_back()
                else:
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

    def handle_action_key(self):
        temp_rect = self.player.rect.inflate(
            Player.ACTION_OFFSET, Player.ACTION_OFFSET)
        radius = max(temp_rect.size) * 2
        pairs = self.camera.get_special_tiles(
            self.player.rect.center, radius)
        special_tiles = [pair for pair in pairs if
                         temp_rect.colliderect(pair.rect)]
        self.handle_sliding_doors(special_tiles)
        self.handle_action_switch(special_tiles)

    def handle_sliding_doors(self, special_tiles):
        base = self.camera.tileEngine.get_tile_from_attr(
            TileType.BASE_ATTR)
        for pair in special_tiles:
            if TileType.SLIDING_DOOR_ATTR in pair.tile.special_attr:
                row, col = self.camera.tileEngine.get_tile_pos(
                    pair.coords[0],
                    pair.coords[1]
                )
                doors = self.get_sliding_doors(row, col)
                for pos in doors:
                    row, col = pos
                    self.camera.tileEngine.tileMap[row][col] = base
                self.camera.set_dirty()

    def get_sliding_doors(self, row, col):
        init_num_keys = Globals.HUD_MANAGER.num_keys
        coords = list()
        if TileType.LOCKED_ATTR in \
                self.camera.tileEngine.tileMap[row][col].special_attr:
            if not Globals.HUD_MANAGER.has_key():
                return list()
            else:
                init_num_keys = -1
                Globals.HUD_MANAGER.use_key()
        coords.append([row, col])
        result = self.get_doors_delta(row, col, init_num_keys, row_delta=-1)
        if result == -1:
            return list()
        coords.extend(result)
        result = self.get_doors_delta(row, col, init_num_keys, row_delta=1)
        if result == -1:
            return list()
        coords.extend(result)
        result = self.get_doors_delta(row, col, init_num_keys, col_delta=-1)
        if result == -1:
            return list()
        coords.extend(result)
        result = self.get_doors_delta(row, col, init_num_keys, col_delta=1)
        if result == -1:
            return list()
        coords.extend(result)
        return coords

    def get_doors_delta(self, row, col, init_num_keys, row_delta=0, col_delta=0):
        coords = list()
        tile_map = self.camera.tileEngine.tileMap
        row += row_delta
        col += col_delta
        while self.camera.tileEngine.is_coord_valid(row, col) and \
                TileType.SLIDING_DOOR_ATTR in tile_map[row][col].special_attr:
            if TileType.LOCKED_ATTR in tile_map[row][col].special_attr:
                if not Globals.HUD_MANAGER.has_key():
                    return -1
                elif Globals.HUD_MANAGER.num_keys >= init_num_keys:
                    Globals.HUD_MANAGER.use_key()
            coords.append([row, col])
            row += row_delta
            col += col_delta
        return coords

    def handle_action_switch(self, special_tiles):
        for pair in special_tiles:
            if TileType.LEVER_LEFT_ATTR in pair.tile.special_attr:
                row, col = self.camera.tileEngine.get_tile_pos(pair.coords[0],
                                                               pair.coords[1])
                lever_right = self.camera.tileEngine.get_tile_from_attr(
                    TileType.LEVER_RIGHT_ATTR)
                self.camera.tileEngine.tileMap[row][col] = lever_right
                self.camera.set_dirty()
                self.handle_lever_on()
            elif TileType.LEVER_RIGHT_ATTR in pair.tile.special_attr:
                row, col = self.camera.tileEngine.get_tile_pos(pair.coords[0],
                                                               pair.coords[1])
                lever_left = self.camera.tileEngine.get_tile_from_attr(
                    TileType.LEVER_LEFT_ATTR)
                self.camera.tileEngine.tileMap[row][col] = lever_left
                self.camera.set_dirty()
                self.handle_lever_off()

    def handle_lever_on(self):
        for turret in self.turrets:
            turret.turn_off()

    def handle_lever_off(self):
        for turret in self.turrets:
            turret.turn_on()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key if not Globals.DISORIENTED else \
                self.invert_key(event.key)
            self.handle_keydown(key)
        elif event.type == pygame.KEYUP:
            key = event.key if not Globals.DISORIENTED else \
                self.invert_key(event.key)
            self.handle_keyup(key)

    def handle_key_down(self, keydown):
        key = pygame.K_DOWN if not Globals.DISORIENTED else pygame.K_UP
        if keydown:
            self.handle_keydown(key)
        else:
            self.handle_keyup(key)

    def handle_key_up(self, keydown):
        key = pygame.K_UP if not Globals.DISORIENTED else pygame.K_DOWN
        if keydown:
            self.handle_keydown(key)
        else:
            self.handle_keyup(key)

    def handle_key_left(self, keydown):
        key = pygame.K_LEFT if not Globals.DISORIENTED else pygame.K_RIGHT
        if keydown:
            self.handle_keydown(key)
        else:
            self.handle_keyup(key)

    def handle_key_right(self, keydown):
        key = pygame.K_RIGHT if not Globals.DISORIENTED else pygame.K_LEFT
        if keydown:
            self.handle_keydown(key)
        else:
            self.handle_keyup(key)

    def handle_attack(self):
        self.player.handle_attack()

    def handle_raw_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_1:
                self.handle_stair_up()
            elif key == pygame.K_2:
                delta = 100 - Globals.HEALTH_BAR.health
                Globals.HEALTH_BAR.changeHealth(delta)
            elif key == pygame.K_3:
                Globals.HUD_MANAGER.add_key()

    def handle_keydown(self, key):
        self.keyCode = key
        for p in self.playerSprites:
            p.keyPressed(key)

    def handle_go_back(self):
        if Globals.goto_previous_level():
            self.timer.pause()
            self.player.stop_and_set_direction(Character.INDEX_UP)
            self.camera.initView()

    def start_pause_fade(self):
        if self.pausing:
            return
        self.pausing = True
        if self.has_timer:
            self.timer.pause()
        self.start_fade_out()

    def handle_pause(self):
        self.pausing = False
        if self.has_timer:
            self.timer.pause()
        self.pause_music()
        self.goto_pause()

    def goto_pause(self):
        Globals.STATE = PauseScreen(self)

    def handle_unpause(self):
        self.resume_music()
        if self.has_timer:
            self.timer.unpause()

    def handle_escape(self):
        # self.handle_pause()
        self.start_pause_fade()

    def handle_keyup(self, key):
        if key == self.keyCode:
            self.keyCode = None
            for p in self.playerSprites:
                p.keyReleased(key)

    def check_camera_position(self):
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
            for light in self.lights:
                light.move(-diff, 0)
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
            for light in self.lights:
                light.move(0, -diff)

    def init_subtitle(self, text):
        text_surf = Level.SUBTITLE_FONT.render(
            text, True, Level.SUBTITLE_COLOR)
        self.subtitle_rect = text_surf.get_rect()
        self.subtitle_rect.centerx = Globals.WIDTH / 2
        self.subtitle_rect.bottom = \
            Globals.HEIGHT - Level.SUBTITLE_MARGIN
        self.subtitle_rect.inflate_ip(
            Level.SUBTITLE_PADDING * 2,
            Level.SUBTITLE_PADDING * 2
        )
        self.subtitle_surf = pygame.Surface(self.subtitle_rect.size).convert()
        self.subtitle_surf.fill(Level.SUBTITLE_BACKGROUND)
        self.subtitle_surf.blit(text_surf, (
            Level.SUBTITLE_PADDING,
            Level.SUBTITLE_PADDING
        ))
        self.subtitle_surf.set_alpha(255)

    def show_subtitle(self, text, loops=-1):
        self.subtitle_loops = loops
        if self.subtitle_loops != -1:
            self.subtitle_loops *= 2
        self.init_subtitle(text)
        self.showing_subtitle = True

    def stop_subtitle(self):
        self.showing_subtitle = False
