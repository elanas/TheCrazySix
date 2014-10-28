import pygame
from Level import Level


class Level1(Level):
	DEF_NAME = 'map_def.txt'
	MAP_NAME = 'dodge.txt'

	def __init__(self):
		super(Level1, self).__init__(Level1.DEF_NAME, Level1.MAP_NAME)	