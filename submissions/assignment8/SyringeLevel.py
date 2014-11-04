import pygame
from Level import Level
from TileTest import TileTest
from Globals import Globals
import Menu


class SyringeLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'dodge.txt'

    def __init__(self):
        super(SyringeLevel, self).__init__(
            SyringeLevel.DEF_NAME, SyringeLevel.MAP_NAME)

    def handle_stairs(self):
        Globals.STATE = TileTest()

    def handle_escape(self):
        Globals.STATE = Menu.Menu()
