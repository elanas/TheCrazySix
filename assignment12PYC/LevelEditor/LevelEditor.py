import pygame
# from GameState import GameState
from Globals import Globals
from TileEngine import TileEngine
from TileManager import TileManager
from TileType import TileType
from Camera import Camera
from DefinitionBrowser import DefinitionBrowser
from asset_loader import AssetLoader
from Action import Action
from os.path import join
import sys
import os
from GameState import GameState
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class LevelEditor(GameState):
    HIDDEN_ATTR = [TileType.LEVER_RIGHT_ATTR, TileType.TURRET_ATTR,
                   TileType.GREENBALL_ATTR]
    IN_GAME_HIDDEN_EXTRA = [TileType.STAIR_DOWN_ATTR, TileType.RESPAWN_ATTR]
    RIGHT_PADDING_FACTOR = 4
    PADDING = 20
    HIGHLIGHT_COLOR = (255, 0, 255)
    HIGHLIGHT_ALPHA = 100
    HIGHLIGHT_BORDER = pygame.color.Color("red")
    SELECTION_ALPHA = 255
    QUICK_TIMEOUT = 1
    MESSAGE_TIMEOUT = 2
    INFO_TIMEOUT = 6
    MESSAGE_PADDING = 10
    MESSAGE_FONT = pygame.font.Font(None, 30)
    DEFAULT_MESSAGE_COLOR = pygame.color.Color("white")
    ERROR_MESSAGE_COLOR = pygame.color.Color("red")
    MESSAGE_BACKGROUND = pygame.color.Color("black")
    TITLE_FONT = pygame.font.Font(None, 35)
    TITLE = "Tiles:"
    SECOND_TITLE = "Combos:"
    TITLE_COLOR = pygame.color.Color("white")
    COMBO_DEF_PATH = join('maps', 'combo_def.txt')
    # TURRET_RIGHT_COMBO = ''

    def __init__(self, definition_path, map_path, globals=Globals,
                 in_game=False):
        self.globals = globals
        self.actions = list()
        self.browser = None
        self.message_time = 0
        self.message_surf = None
        self.message_rect = None
        self.key_code = None
        self.mouse_down = False
        self.info_mode = False
        self.delete_mode = False
        self.in_game = in_game
        loader = AssetLoader(join("images", "tiles"))
        TileType.create_empty(loader)
        self.base_image = loader.load_image("transparent.png")
        self.base_rect = self.base_image.get_rect()
        self.definition_path = definition_path
        self.map_path = map_path
        self.tile_engine = TileEngine(self.definition_path, self.map_path)
        self.combo_tile_manager = TileManager(LevelEditor.COMBO_DEF_PATH, None)
        self.tile_rect = self.tile_engine.get_tile_rect()
        self.right_padding = self.tile_rect.width * \
            LevelEditor.RIGHT_PADDING_FACTOR
        self.shift_factor = self.tile_rect.width
        self.init_camera()
        self.init_highlight()
        self.init_title()
        self.init_browser()
        self.init_second_title()
        self.init_combo_browser()
        self.in_combo = False

    def init_title(self):
        self.title_surf = LevelEditor.TITLE_FONT.render(
            LevelEditor.TITLE, False, LevelEditor.TITLE_COLOR)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = self.camera_dest.right + \
            (self.globals.WIDTH - self.camera_dest.right) / 2
        self.title_rect.top = self.camera_dest.top

    def init_second_title(self):
        self.second_title_surf = LevelEditor.TITLE_FONT.render(
            LevelEditor.SECOND_TITLE, False, LevelEditor.TITLE_COLOR)
        self.second_title_rect = self.second_title_surf.get_rect()
        self.second_title_rect.centerx = self.camera_dest.right + \
            (self.globals.WIDTH - self.camera_dest.right) / 2
        self.second_title_rect.top = self.browser.container.bottom + 10

    def init_browser(self):
        width = (self.globals.WIDTH - self.camera_dest.right) - 20
        height = self.globals.HEIGHT - self.title_rect.height * 2 - (32 * 3)
        c = pygame.Rect(0, self.title_rect.bottom + 5, width, height)
        c.centerx = self.title_rect.centerx
        # if self.browser is not None:
        #     pygame.draw.rect(self.globals.SCREEN, (0, 0, 0), self.browser.container)
        hidden_attr = LevelEditor.HIDDEN_ATTR
        if self.in_game:
            hidden_attr.extend(LevelEditor.IN_GAME_HIDDEN_EXTRA)
        self.browser = DefinitionBrowser(self.tile_engine.tileManager,
                                         self.tile_engine.get_tile_rect(), c,
                                         hidden_attr)

    def init_combo_browser(self):
        width = self.browser.container.width
        height = self.globals.HEIGHT - self.second_title_rect.bottom - 10
        c = pygame.Rect(0, self.second_title_rect.bottom + 5, width, height)
        c.centerx = self.browser.container.centerx
        self.combo_browser = DefinitionBrowser(
            self.combo_tile_manager, self.tile_engine.get_tile_rect(),
            c)

    def init_camera(self):
        self.camera_dest = pygame.Rect(
            LevelEditor.PADDING, LevelEditor.PADDING, self.globals.WIDTH -
            self.right_padding - LevelEditor.PADDING, self.globals.HEIGHT -
            LevelEditor.PADDING)
        self.camera = Camera(self.tile_engine, self.camera_dest)
        extra_y = self.camera_dest.height % self.tile_rect.height
        extra_x = self.camera_dest.width % self.tile_rect.width
        if extra_y > 0:
            self.camera_dest.height -= extra_y
        if extra_x > 0:
            self.camera_dest.width -= extra_x
        self.camera_dest.centery = self.globals.HEIGHT / 2

    def init_highlight(self, source=None, alpha=HIGHLIGHT_ALPHA, border=False):
        self.highlight_surf = pygame.Surface(self.tile_rect.size).convert()
        if source is None:
            self.highlight_surf.fill(LevelEditor.HIGHLIGHT_COLOR)
            self.highlight_surf.set_alpha(alpha)
        else:
            self.highlight_surf.blit(source, (0, 0))
            self.highlight_surf.set_alpha(alpha)
        if border:
            pygame.draw.rect(self.highlight_surf,
                             LevelEditor.HIGHLIGHT_BORDER, self.tile_rect, 1)

    def render(self):
        self.globals.SCREEN.fill((0, 0, 0))
        self.camera.render(self.globals.SCREEN, False)
        self.handle_mouse()

        if self.message_surf is not None:
            self.globals.SCREEN.blit(self.message_surf, self.message_rect)

        self.globals.SCREEN.blit(self.title_surf, self.title_rect)
        self.browser.render(self.globals.SCREEN)
        self.globals.SCREEN.blit(
            self.second_title_surf, self.second_title_rect)
        self.combo_browser.render(self.globals.SCREEN)

    def update(self, time):
        if self.key_code is not None:
            if self.key_code == pygame.K_UP or self.key_code == pygame.K_w:
                self.camera.move(0, -self.shift_factor)
            elif self.key_code == pygame.K_DOWN or self.key_code == pygame.K_s:
                self.camera.move(0, self.shift_factor)
            elif self.key_code == pygame.K_LEFT or self.key_code == pygame.K_a:
                self.camera.move(-self.shift_factor, 0)
            elif self.key_code == pygame.K_RIGHT or \
                    self.key_code == pygame.K_d:
                self.camera.move(self.shift_factor, 0)
        if self.message_surf is not None:
            self.message_time -= time
            if self.message_time <= 0:
                self.message_surf = None
        if self.mouse_down:
            self.handle_mouse_click()

    def set_message(self, content, timeout=MESSAGE_TIMEOUT,
                    color=DEFAULT_MESSAGE_COLOR):
        temp_surf = LevelEditor.MESSAGE_FONT.render(content, True, color)
        self.message_rect = temp_surf.get_rect()
        self.message_rect.bottom = self.camera_dest.bottom
        self.message_rect.centerx = self.camera_dest.centerx
        self.message_rect.inflate_ip(LevelEditor.MESSAGE_PADDING * 2,
                                     LevelEditor.MESSAGE_PADDING * 2)
        self.message_surf = pygame.Surface(self.message_rect.size).convert()
        self.message_surf.fill(LevelEditor.MESSAGE_BACKGROUND)
        self.message_surf.blit(
            temp_surf, (LevelEditor.MESSAGE_PADDING,
                        LevelEditor.MESSAGE_PADDING))
        if self.message_rect.left < 0:
            self.message_rect.left = 0
        self.message_time = timeout

    def handle_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.camera_dest.collidepoint(pos):
            temp = (pos[0] - self.camera_dest.left, pos[1] -
                    self.camera_dest.top)
            rect = self.tile_rect.copy()
            x = pos[0] - temp[0] % self.tile_rect.width
            y = pos[1] - temp[1] % self.tile_rect.height
            rect.topleft = (x, y)
            self.globals.SCREEN.blit(self.highlight_surf, rect)

    def handle_mouse_click(self):
        coord = list(pygame.mouse.get_pos())
        if self.camera_dest.collidepoint(coord):
            coord[0] += self.camera.viewpoint.left - self.camera_dest.left
            coord[1] += self.camera.viewpoint.top - self.camera_dest.top
            col = int(coord[0] / self.tile_rect.width)
            row = int(coord[1] / self.tile_rect.height)
            if self.info_mode:
                self.show_tile_info(row, col)
            elif self.delete_mode:
                self.delete_tile(row, col)
            else:
                self.handle_tile_set(row, col)
        elif self.browser.container.collidepoint(coord):
            coord[0] -= self.browser.container.left
            coord[1] -= self.browser.container.top
            if self.info_mode:
                self.browser.handle_info_click(coord, self)
            else:
                self.handle_browser_click(coord)
        elif self.combo_browser.container.collidepoint(coord):
            coord[0] -= self.combo_browser.container.left
            coord[1] -= self.combo_browser.container.top
            if self.info_mode:
                self.combo_browser.handle_info_click(coord, self)
            else:
                self.handle_combo_browser_click(coord)

    def handle_tile_set(self, row, col):
        if not self.in_combo:
            self.handle_normal_tile_set(row, col)
        else:
            self.handle_combo_tile_set(row, col)

    def handle_normal_tile_set(self, row, col, tile=None):
        if tile is None:
            tile = self.browser.get_selected_tile()
        if tile is None:
            return row, col, False
        if self.tile_engine.is_coord_valid(row, col):
            if self.tile_engine.tileMap[row][col] is not tile:
                old_tile = self.tile_engine.tileMap[row][col]
                self.tile_engine.tileMap[row][col] = tile
                a = Action(type=Action.SET_TYPE, row=row, col=col,
                           old_tile=old_tile, new_tile=tile)
                self.actions.append(a)
                return row, col, True
            else:
                return row, col, False
        else:
            new_row, new_col = self.make_room(row, col)
            result = self.handle_normal_tile_set(new_row, new_col)
            return new_row, new_col, result

    def handle_combo_tile_set(self, row, col):
        tile = self.combo_browser.get_selected_tile()
        if tile is None:
            return
        if TileType.TURRET_COMBO in tile.special_attr:
            if TileType.TURRET_COMBO_RIGHT in tile.special_attr:
                prefix = 't_right_'
            elif TileType.TURRET_COMBO_LEFT in tile.special_attr:
                prefix = 't_left_'
            else:
                return
            self.handle_turret_combo(row, col, prefix)

    def handle_turret_combo(self, row, col, prefix):
        num_added = 0
        old_row = row
        old_col = col
        for i in range(0, 4):
            if not self.tile_engine.is_coord_valid(row, col):
                self.set_message('combo cannot be added off map',
                                 color=LevelEditor.ERROR_MESSAGE_COLOR)
                return
            if i == 1:
                col -= 1
                row += 1
            else:
                col += 1
        row = old_row
        col = old_col
        for i in range(0, 4):
            attr = prefix + str(i)
            tile = self.tile_engine.get_tile_from_attr(attr)
            row, col, result = self.handle_normal_tile_set(row, col, tile)
            if result:
                num_added += 1

            if i == 1:
                col -= 1
                row += 1
            else:
                col += 1
        if num_added > 0:
            a = Action(type=Action.COMBO_SET, num_sets=num_added)
            self.actions.append(a)
        self.set_message('combo added', timeout=LevelEditor.QUICK_TIMEOUT)

    def make_room(self, row, col):
        row_delta, col_delta = 0, 0
        tile_map = self.tile_engine.tileMap
        # add to front of map
        for i in range(row, 0):
            tile_map.insert(0, list())
            self.camera.viewpoint.y += self.tile_rect.height
            row_delta += 1
        # add to end of map
        for i in range(len(tile_map), row + 1):
            tile_map.append(list())
        new_row = 0
        if row > 0:
            new_row = row
        # add to beginning of ALL map rows
        if col < 0:
            for row_num in range(0, len(tile_map)):
                curr_row = tile_map[row_num]
                for j in range(0, -col):
                    curr_row.insert(0, None)
            for j in range(0, -col):
                self.camera.viewpoint.x += self.tile_rect.width
                col_delta += 1
        # add to end of map row
        for i in range(len(tile_map[new_row]), col + 1):
            tile_map[row].append(None)
        new_col = 0
        if col > 0:
            new_col = col
        self.offset_actions(row_delta, col_delta)
        return new_row, new_col

    def offset_actions(self, row_delta, col_delta):
        if row_delta == 0 and col_delta == 0:
            return
        for a in self.actions:
            a.row += row_delta
            a.col += col_delta

    def handle_browser_click(self, coord):
        self.browser.handle_mouse_click(coord)
        tile = self.browser.get_selected_tile()
        if tile is not None:
            self.combo_browser.clear_selection()
            self.in_combo = False
            if self.info_mode:
                self.toggle_info_mode()
            elif self.delete_mode:
                self.toggle_delete_mode()
            self.init_highlight(tile.image, alpha=LevelEditor.SELECTION_ALPHA,
                                border=True)

    def handle_combo_browser_click(self, coord):
        self.combo_browser.handle_mouse_click(coord)
        tile = self.combo_browser.get_selected_tile()
        if tile is not None:
            self.browser.clear_selection()
            self.in_combo = True
            if self.info_mode:
                self.toggle_info_mode()
            elif self.delete_mode:
                self.toggle_delete_mode()
            self.init_highlight(tile.image, alpha=LevelEditor.SELECTION_ALPHA,
                                border=True)

    def delete_tile(self, row, col):
        if self.tile_engine.is_coord_valid(row, col) and \
                self.tile_engine.tileMap[row][col] is not None:
            old_tile = self.tile_engine.tileMap[row][col]
            a = Action(type=Action.DELETE_TYPE, row=row, col=col,
                       old_tile=old_tile)
            self.actions.append(a)
            self.tile_engine.tileMap[row][col] = None

    def show_tile_info(self, row=-1, col=-1, tile=None):
        if self.tile_engine.is_coord_valid(row, col):
            tile = self.tile_engine.tileMap[row][col]
        if tile is None:
            self.set_message("empty tile", timeout=LevelEditor.QUICK_TIMEOUT)
        else:
            self.set_message(str(tile), LevelEditor.INFO_TIMEOUT)

    def set_default_cursor(self):
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    def toggle_info_mode(self, suppress=False):
        if suppress:
            self.info_mode = False
            return
        self.browser.clear_selection()
        self.init_highlight()
        self.toggle_delete_mode(True)
        self.info_mode = not self.info_mode
        if self.info_mode:
            self.set_message("begin info mode")
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.set_message("end info mode")
            self.set_default_cursor()

    def toggle_delete_mode(self, suppress=False):
        if suppress:
            self.delete_mode = False
            return
        self.browser.clear_selection()
        self.init_highlight()
        self.toggle_info_mode(True)
        self.delete_mode = not self.delete_mode
        if self.delete_mode:
            self.set_message("begin delete mode")
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            self.set_message("end delete mode")
            self.set_default_cursor()

    def handle_escape(self):
        if not self.in_game:
            self.revert_and_reload()
        else:
            import CustomLevelPicker
            self.globals.STATE = CustomLevelPicker.CustomLevelPicker()

    def handle_key_up(self, keydown):
        if keydown and self.key_code is None:
            self.key_code = pygame.K_UP
        elif not keydown and self.key_code == pygame.K_UP:
            self.key_code = None

    def handle_key_down(self, keydown):
        if keydown and self.key_code is None:
            self.key_code = pygame.K_DOWN
        elif not keydown and self.key_code == pygame.K_DOWN:
            self.key_code = None

    def handle_key_left(self, keydown):
        if keydown and self.key_code is None:
            self.key_code = pygame.K_LEFT
        elif not keydown and self.key_code == pygame.K_LEFT:
            self.key_code = None

    def handle_key_right(self, keydown):
        if keydown and self.key_code is None:
            self.key_code = pygame.K_RIGHT
        elif not keydown and self.key_code == pygame.K_RIGHT:
            self.key_code = None

    def handle_raw_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.toggle_info_mode()
            elif event.key == pygame.K_BACKSPACE:
                self.toggle_delete_mode()
            elif event.key == pygame.K_RETURN:
                self.handle_save()
            elif event.key == pygame.K_u:
                self.undo_action()
            elif event.key == pygame.K_MINUS:
                self.browser.scroll_down()
            elif event.key == pygame.K_EQUALS:
                self.browser.scroll_up()
            elif self.key_code is None:
                self.key_code = event.key
        elif event.type == pygame.KEYUP:
            if event.key == self.key_code:
                self.key_code = None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                old_mode = self.info_mode
                self.info_mode = True
                self.handle_mouse_click()
                self.info_mode = old_mode
            else:
                self.mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False

    def undo_action(self, supress_message=False):
        if len(self.actions) == 0:
            if not supress_message:
                self.set_message("there is nothing to undo",
                                 color=LevelEditor.ERROR_MESSAGE_COLOR)
            return
        action = self.actions.pop()
        if action.type == Action.DELETE_TYPE:
            self.tile_engine.tileMap[action.row][action.col] = action.old_tile
            if not supress_message:
                self.set_message("delete undone",
                                 timeout=LevelEditor.QUICK_TIMEOUT)
        elif action.type == Action.SET_TYPE:
            self.tile_engine.tileMap[action.row][action.col] = action.old_tile
            if not supress_message:
                self.set_message("tile set undone",
                                 timeout=LevelEditor.QUICK_TIMEOUT)
        elif action.type == Action.COMBO_SET:
            for i in range(0, action.num_sets):
                self.undo_action(supress_message=True)
            self.set_message("combo set undone",
                             timeout=LevelEditor.QUICK_TIMEOUT)
        else:
            self.set_message("Undo failed",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)

    def revert_and_reload(self):
        try:
            self.tile_engine = TileEngine(self.definition_path, self.map_path)
            self.camera.tileEngine = self.tile_engine
            self.init_browser()
            self.init_highlight()
            self.set_message("reverted all changes and reloaded tile engine")
        except Exception as e:
            self.set_message("failed to reload tile engine",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            print "Reload failed: ", e

    def handle_save(self):
        min_x = 0
        tile_map = self.tile_engine.tileMap
        if not self.validate_map():
            return
        min_x = min([self.get_x_start(row) for row in tile_map
                     if len(row) > 0])
        min_y = self.get_y_start()
        max_y = self.get_y_end()
        try:
            map_file = open(self.map_path, 'w')
            if min_y == max_y:
                return
            for row_num in range(min_y, max_y):
                row = tile_map[row_num]
                for col_num in range(min_x, self.get_length(row)):
                    col = row[col_num]
                    if col is None:
                        col = TileType.EMPTY_TILE
                    map_file.write(col.symbol)
                map_file.write('\n')
            self.set_message("saved successfully")
        except IOError as e:
            self.set_message("failed to save the map file",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            print "Failed to save the map file"
            print e
        finally:
            map_file.close()

    def get_x_start(self, row):
        x_start = 0
        for col in range(0, len(row)):
            if row[col] is not None:
                break
            x_start += 1
        return x_start

    def get_length(self, row):
        length = len(row)
        for col_num in range(len(row) - 1, -1, -1):
            if row[col_num] is not None:
                break
            length -= 1
        return length

    def get_y_start(self):
        y_start = 0
        for row in self.tile_engine.tileMap:
            found_tile = False
            for col in row:
                if col is not None:
                    found_tile = True
                    break
            if found_tile:
                break
            y_start += 1
        return y_start

    def get_y_end(self):
        y_end = len(self.tile_engine.tileMap)
        for row_num in range(len(self.tile_engine.tileMap) - 1, -1, -1):
            row = self.tile_engine.tileMap[row_num]
            found_tile = False
            for col in row:
                if col is not None:
                    found_tile = True
                    break
            if found_tile:
                break
            y_end -= 1
        return y_end

    def validate_map(self):
        tile_map = self.tile_engine.tileMap
        if len(tile_map) == 0:
            self.set_message("cannot save an empty map",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            return False
        num_player_spawn = 0
        num_stairs_up = 0
        for col in tile_map:
            for tile in col:
                if tile is None:
                    continue
                if TileType.START_ATTR in tile.special_attr:
                    num_player_spawn += 1
                if TileType.STAIR_UP_ATTR in tile.special_attr:
                    num_stairs_up += 1
        if num_player_spawn == 0:
            self.set_message("you must define a player spawn point",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            return False
        elif num_player_spawn > 1:
            self.set_message("you cannot define multiple player spawn points",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            return False
        if num_stairs_up == 0 and self.in_game:
            self.set_message("you must define at least on stair going \"up\"",
                             color=LevelEditor.ERROR_MESSAGE_COLOR)
            return False
        return True
