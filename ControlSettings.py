from GameState import GameState
from asset_loader import AssetLoader
from Globals import Globals
from os.path import join
from SetJoystickKeyState import SetJoystickKeyState
from SettingsManager import SettingsManager
import pygame


class SurfRectPair(object):

    def __init__(self, surf_arr=None, rect=None):
        self.surf_arr = surf_arr
        self.rect = rect


class ControlSettings(GameState):
    TITLE_IMAGE_PATH = 'control_settings.png'
    TITLE_MARGIN_TOP = 60
    TITLE_TEXT_MARGIN = 40
    TITLE_ARROW_MARGIN = 100
    SURF_INDEX_NORMAL = 0
    SURF_INDEX_HIT = 1
    SURF_INDEX_SELECTED = 2
    ARROW_PADDING = 10
    KEY_PADDING = 30
    RESET_MARGIN_BOTTOM = 20
    INDEX_UP = 0
    INDEX_DOWN = 2
    INDEX_LEFT = 1
    INDEX_RIGHT = 3
    INDEX_ATTACK = 4
    INDEX_ACTION = 5
    INDEX_ESCAPE = 6
    INDEX_RETURN = 7
    INDEX_RESET = 8
    NUM_OPTIONS = 9

    def __init__(self):
        self.loader = AssetLoader('images')
        self.control_loader = AssetLoader(join('images', 'controls'))
        self.background_img = self.loader.load_image('background.png')
        self.title_surf = self.loader.load_image_alpha(
            ControlSettings.TITLE_IMAGE_PATH)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = Globals.WIDTH / 2
        self.title_rect.top = ControlSettings.TITLE_MARGIN_TOP
        self.arrows_top = self.title_rect.bottom + \
            ControlSettings.TITLE_ARROW_MARGIN
        self.arrows_x_center = int(Globals.WIDTH / 4)
        self.text_top = self.title_rect.bottom + \
            ControlSettings.TITLE_TEXT_MARGIN
        self.surf_rect_pairs = [SurfRectPair()
                                for i in range(0, ControlSettings.NUM_OPTIONS)]
        self.surf_index = [ControlSettings.SURF_INDEX_NORMAL for i in range(
            0, ControlSettings.NUM_OPTIONS)]
        self.last_surf_index = [
            ControlSettings.SURF_INDEX_NORMAL for i in
            range(0, ControlSettings.NUM_OPTIONS)]
        self.ignore_index = [0 for i in range(0, ControlSettings.NUM_OPTIONS)]
        self.load_control_images()
        self.selection = 0
        self.set_selection(0)

    def set_selection(self, index):
        if self.selection != -1:
            if self.surf_index[self.selection] == \
                    ControlSettings.SURF_INDEX_HIT:
                self.last_surf_index[
                    self.selection] = ControlSettings.SURF_INDEX_NORMAL
            else:
                self.last_surf_index[
                    self.selection] = ControlSettings.SURF_INDEX_NORMAL
                self.surf_index[
                    self.selection] = ControlSettings.SURF_INDEX_NORMAL
        self.selection = index
        if self.surf_index[index] == ControlSettings.SURF_INDEX_HIT:
            self.last_surf_index[index] = ControlSettings.SURF_INDEX_SELECTED
        else:
            self.last_surf_index[index] = self.surf_index[index]
            self.surf_index[index] = ControlSettings.SURF_INDEX_SELECTED

    def change_selection(self, delta):
        index = self.selection + delta
        if index < 0 or index >= ControlSettings.NUM_OPTIONS:
            return
        self.set_selection(index)

    def select(self):
        if self.selection == -1:
            return
        if self.selection == ControlSettings.INDEX_RESET:
            SettingsManager.reset_controls()
            self.set_selection(0)
            return
        Globals.STATE = SetJoystickKeyState(
            self.surf_rect_pairs[self.selection].surf_arr[0],
            list_index=self.selection, return_state=self)

    def load_image_group(self, file_path):
        return self.control_loader.load_spritesheet_alpha(
            file_path, num_rows=3, num_cols=1)

    def set_surf_arr(self, index, file_path):
        self.surf_rect_pairs[index].surf_arr = self.load_image_group(file_path)
        self.surf_rect_pairs[index].rect = self.surf_rect_pairs[
            index].surf_arr[0].get_rect()

    def get_surf(self, index):
        return self.surf_rect_pairs[index].surf_arr[self.surf_index[index]]

    def get_rect(self, index):
        return self.surf_rect_pairs[index].rect

    def load_control_images(self):
        self.load_arrows()
        self.set_surf_arr(ControlSettings.INDEX_ATTACK, 'attack_key.png')
        self.set_surf_arr(ControlSettings.INDEX_ACTION, 'action_key.png')
        self.set_surf_arr(ControlSettings.INDEX_ESCAPE, 'escape_key.png')
        self.set_surf_arr(ControlSettings.INDEX_RETURN, 'return_key.png')
        self.set_surf_arr(ControlSettings.INDEX_RESET, 'reset_controls.png')

        centerx = int((3 * Globals.WIDTH) / 4)
        attack_key_rect = self.get_rect(ControlSettings.INDEX_ATTACK)
        attack_key_rect.centerx = centerx
        attack_key_rect.top = self.text_top

        action_key_rect = self.get_rect(ControlSettings.INDEX_ACTION)
        action_key_rect.centerx = centerx
        action_key_rect.top = attack_key_rect.bottom + \
            ControlSettings.KEY_PADDING

        escape_key_rect = self.get_rect(ControlSettings.INDEX_ESCAPE)
        escape_key_rect.centerx = centerx
        escape_key_rect.top = action_key_rect.bottom + \
            ControlSettings.KEY_PADDING    

        return_key_rect = self.get_rect(ControlSettings.INDEX_RETURN)
        return_key_rect.centerx = centerx
        return_key_rect.top = escape_key_rect.bottom + \
            ControlSettings.KEY_PADDING

        reset_rect = self.get_rect(ControlSettings.INDEX_RESET)
        reset_rect.centerx = int(Globals.WIDTH / 2)
        reset_rect.bottom = Globals.HEIGHT - \
            ControlSettings.RESET_MARGIN_BOTTOM

    def load_arrows(self):
        self.set_surf_arr(ControlSettings.INDEX_UP, 'arrow_up.png')
        self.set_surf_arr(ControlSettings.INDEX_DOWN, 'arrow_down.png')
        self.set_surf_arr(ControlSettings.INDEX_LEFT, 'arrow_left.png')
        self.set_surf_arr(ControlSettings.INDEX_RIGHT, 'arrow_right.png')

        arrow_up_rect = self.get_rect(ControlSettings.INDEX_UP)
        arrow_up_rect.centerx = self.arrows_x_center
        arrow_up_rect.top = self.arrows_top
        arrow_down_rect = self.get_rect(ControlSettings.INDEX_DOWN)
        arrow_down_rect.centerx = arrow_up_rect.centerx
        arrow_down_rect.top = arrow_up_rect.bottom + \
            ControlSettings.ARROW_PADDING
        arrow_left_rect = self.get_rect(ControlSettings.INDEX_LEFT)
        arrow_left_rect.top = arrow_down_rect.top
        arrow_left_rect.right = arrow_down_rect.left - \
            ControlSettings.ARROW_PADDING
        arrow_right_rect = self.get_rect(ControlSettings.INDEX_RIGHT)
        arrow_right_rect.top = arrow_down_rect.top
        arrow_right_rect.left = arrow_down_rect.right + \
            ControlSettings.ARROW_PADDING

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.title_surf, self.title_rect)
        for i, pair in enumerate(self.surf_rect_pairs):
            Globals.SCREEN.blit(pair.surf_arr[self.surf_index[i]], pair.rect)

    def handle_raw_event(self, event):
        if event.type == pygame.KEYDOWN:
            index = -1
            if event in SettingsManager.EVENTS_UP:
                index = ControlSettings.INDEX_UP
            elif event in SettingsManager.EVENTS_DOWN:
                index = ControlSettings.INDEX_DOWN
            elif event in SettingsManager.EVENTS_LEFT:
                index = ControlSettings.INDEX_LEFT
            elif event in SettingsManager.EVENTS_RIGHT:
                index = ControlSettings.INDEX_RIGHT
            elif event in SettingsManager.EVENTS_ESCAPE:
                index = ControlSettings.INDEX_ESCAPE
            elif event in SettingsManager.EVENTS_ACTION:
                index = ControlSettings.INDEX_ACTION
            elif event in SettingsManager.EVENTS_ATTACK:
                index = ControlSettings.INDEX_ATTACK
            elif event in SettingsManager.EVENTS_RETURN:
                index = ControlSettings.INDEX_RETURN
            if index != -1:
                self.ignore_index[index] = 2

    def quit(self):
        import SettingsState
        Globals.STATE = SettingsState.SettingsState()

    def check_hit(self, index, keydown=True):
        if not keydown:
            self.ignore_index[index] = 0
            if self.surf_index[index] != ControlSettings.SURF_INDEX_SELECTED:
                self.set_last_state(index)
            return False
        if self.ignore_index[index] > 0:
            self.ignore_index[index] -= 1
            if self.surf_index[index] != ControlSettings.SURF_INDEX_SELECTED:
                self.set_last_state(index)
            return False
        self.last_surf_index[index] = self.surf_index[index]
        self.surf_index[index] = ControlSettings.SURF_INDEX_HIT
        return True

    def set_last_state(self, index):
        if self.last_surf_index[index] == ControlSettings.SURF_INDEX_HIT:
            self.last_surf_index[index] = ControlSettings.SURF_INDEX_NORMAL
        self.surf_index[index] = self.last_surf_index[index]

    def handle_action_key(self, keydown=True):
        self.check_hit(ControlSettings.INDEX_ACTION, keydown)

    def handle_action_keyup(self):
        self.handle_action_key(False)

    def handle_attack(self, keydown=True):
        self.check_hit(ControlSettings.INDEX_ATTACK, keydown)

    def handle_attack_keyup(self):
        self.handle_attack(False)

    def handle_key_down(self, keydown):
        if keydown and self.ignore_index[ControlSettings.INDEX_DOWN] > 0:
            self.change_selection(1)
        self.check_hit(ControlSettings.INDEX_DOWN, keydown)

    def handle_key_up(self, keydown):
        if keydown and self.ignore_index[ControlSettings.INDEX_UP] > 0:
            self.change_selection(-1)
        self.check_hit(ControlSettings.INDEX_UP, keydown)

    def handle_key_left(self, keydown):
        if keydown and self.ignore_index[ControlSettings.INDEX_LEFT] > 0:
            self.change_selection(-1)
        self.check_hit(ControlSettings.INDEX_LEFT, keydown)

    def handle_key_right(self, keydown):
        if keydown and self.ignore_index[ControlSettings.INDEX_RIGHT] > 0:
            self.change_selection(1)
        self.check_hit(ControlSettings.INDEX_RIGHT, keydown)

    def handle_backspace(self):
        pass

    def handle_return(self, keydown=True):
        if keydown and self.ignore_index[ControlSettings.INDEX_RETURN] > 0:
            self.select()
            self.ignore_index[ControlSettings.INDEX_RETURN] = 0
        else:
            self.check_hit(ControlSettings.INDEX_RETURN, keydown)

    def handle_return_keyup(self):
        self.handle_return(False)

    def handle_escape(self, keydown=True):
        if self.ignore_index[ControlSettings.INDEX_ESCAPE] > 0:
            self.quit()
        self.check_hit(ControlSettings.INDEX_ESCAPE, keydown)

    def handle_escape_keyup(self):
        self.handle_escape(False)
