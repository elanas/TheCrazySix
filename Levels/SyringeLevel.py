import pygame
from Level import Level
from TileSystem.TileType import TileType
from Player import Player


class SyringeLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'dodge.txt'
    SUBTITLE_TEXT = 'Watch out for syringes'
    SUBTITLE_LOOPS = 3

    def __init__(self):
        super(SyringeLevel, self).__init__(
            SyringeLevel.DEF_NAME, SyringeLevel.MAP_NAME)
        self.show_subtitle(SyringeLevel.SUBTITLE_TEXT, SyringeLevel.SUBTITLE_LOOPS)

    def handle_lever_on(self):
        for turret in self.turrets:
            turret.turn_off()

    def handle_lever_off(self):
        for turret in self.turrets:
            turret.turn_on()