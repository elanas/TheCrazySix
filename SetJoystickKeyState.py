from Globals import Globals
from GameState import GameState
from asset_loader import AssetLoader
from EventPair import EventPair
from SettingsManager import SettingsManager
from EventManager import EventManager
import pygame


class SetJoystickKeyState(GameState):
    ALLOWED_TYPES = set([pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION, pygame.JOYHATMOTION])
    TITLE_IMAGE_PATH = 'set_key.png'
    TITLE_MARGIN_TOP = 60

    def __init__(self, image_surf, list_index, return_state):
        self.list_index = list_index
        self.return_state = return_state
        self.image_surf = image_surf
        self.loader = AssetLoader('images')
        self.image_rect = self.image_surf.get_rect()
        self.image_rect.center = Globals.SCREEN.get_rect().center
        self.init_images()

    def init_images(self):
        self.background_img = self.loader.load_image('background.png')
        self.title_surf = self.loader.load_image_alpha(
            SetJoystickKeyState.TITLE_IMAGE_PATH)
        self.title_rect = self.title_surf.get_rect()
        self.title_rect.centerx = Globals.WIDTH / 2
        self.title_rect.top = SetJoystickKeyState.TITLE_MARGIN_TOP

    def render(self):
        Globals.SCREEN.blit(self.background_img, (0, 0))
        Globals.SCREEN.blit(self.title_surf, self.title_rect)
        Globals.SCREEN.blit(self.image_surf, self.image_rect)

    def handle_escape(self):
        Globals.STATE = self.return_state

    def set_event(self, event):
        pair = self.convert_event(event)
        SettingsManager.EVENTS_UP = [a for a in SettingsManager.EVENTS_UP if a != event]
        SettingsManager.EVENTS_DOWN = [a for a in SettingsManager.EVENTS_DOWN if a != event]
        SettingsManager.EVENTS_LEFT = [a for a in SettingsManager.EVENTS_LEFT if a != event]
        SettingsManager.EVENTS_RIGHT = [a for a in SettingsManager.EVENTS_RIGHT if a != event]
        SettingsManager.EVENTS_ATTACK = [a for a in SettingsManager.EVENTS_ATTACK if a != event]
        SettingsManager.EVENTS_ACTION = [a for a in SettingsManager.EVENTS_ACTION if a != event]
        SettingsManager.EVENTS_ESCAPE = [a for a in SettingsManager.EVENTS_ESCAPE if a != event]
        SettingsManager.EVENTS_RETURN = [a for a in SettingsManager.EVENTS_RETURN if a != event]
        SettingsManager.EVENTS_BACKSPACE = [a for a in SettingsManager.EVENTS_BACKSPACE if a != event]
        self.get_event_list().append(pair)
        SettingsManager.save()
        self.handle_escape()

    def get_event_list(self):
        from ControlSettings import ControlSettings
        if self.list_index == ControlSettings.INDEX_ESCAPE:
            return SettingsManager.EVENTS_ESCAPE
        elif self.list_index == ControlSettings.INDEX_ATTACK:
            return SettingsManager.EVENTS_ATTACK
        elif self.list_index == ControlSettings.INDEX_ACTION:
            return SettingsManager.EVENTS_ACTION
        elif self.list_index == ControlSettings.INDEX_RETURN:
            return SettingsManager.EVENTS_RETURN
        elif self.list_index == ControlSettings.INDEX_UP:
            return SettingsManager.EVENTS_UP
        elif self.list_index == ControlSettings.INDEX_DOWN:
            return SettingsManager.EVENTS_DOWN
        elif self.list_index == ControlSettings.INDEX_LEFT:
            return SettingsManager.EVENTS_LEFT
        elif self.list_index == ControlSettings.INDEX_RIGHT:
            return SettingsManager.EVENTS_RIGHT
        else:
            return list()

    def convert_event(self, event):
        pair = EventPair(type=event.type)
        if event.type == pygame.JOYBUTTONDOWN:
            pair.value = event.button
        elif event.type == pygame.JOYAXISMOTION:
            if event.value < 0:
                pair.value = -1
            elif event.value > 0:
                pair.value = 1
            else:
                pair.value = 0
            pair.axis = event.axis
        elif event.type == pygame.JOYHATMOTION:
            pair.hat = event.hat
            pair.value = event.value
        return pair

    def handle_raw_event(self, event):
        if event.type in SetJoystickKeyState.ALLOWED_TYPES and \
                EventManager.is_keydown(event):
            self.set_event(event)
