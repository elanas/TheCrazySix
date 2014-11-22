import Level
import Globals
from HealthBar import HealthBar
import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import CustomLevelPicker


class CustomLevel(Level.Level):
    DEF_NAME = "map_def.txt"

    def __init__(self, map_path):
        super(CustomLevel, self).__init__(CustomLevel.DEF_NAME,
                                          map_path)
        Globals.Globals.HEALTH_BAR = HealthBar()

    def handle_escape(self):
        Globals.Globals.STATE = CustomLevelPicker.CustomLevelPicker()

    def handle_finish_fade_out(self):
        Globals.Globals.STATE = CustomLevelPicker.CustomLevelPicker()

    def handle_lose_game(self):
        Globals.Globals.STATE = CustomLevelPicker.CustomLevelPicker()
