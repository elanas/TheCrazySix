import Level
import Globals
from HealthBar import HealthBar
import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import CustomLevelPicker
from PauseScreen import PauseScreen


class CustomLevel(Level.Level):
    DEF_NAME = "map_def.txt"
    MUSIC_PATH = 'syringe_level.ogg'

    def __init__(self, map_path):
        super(CustomLevel, self).__init__(CustomLevel.DEF_NAME,
                                          map_path,
                                          music_path=CustomLevel.MUSIC_PATH)
        Globals.Globals.HEALTH_BAR = HealthBar()

    def goto_pause(self):
        self.pause_music()
        escape_state = CustomLevelPicker.CustomLevelPicker()
        Globals.Globals.STATE = PauseScreen(self, escape_state)

    def handle_finish_fade_out(self):
        self.stop_music()
        Globals.Globals.STATE = CustomLevelPicker.CustomLevelPicker()

    def handle_lose_game(self):
        self.stop_music()
        Globals.Globals.STATE = CustomLevelPicker.CustomLevelPicker()
