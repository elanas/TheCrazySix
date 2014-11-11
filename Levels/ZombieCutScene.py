import pygame
from Globals import Globals
from Level import Level
from CutSceneEnemy import CutSceneEnemy


class ZombieCutScene(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'cut_test.txt'
    NEGATIVE_MARGIN = 3
    # SUBTITLE_TEXT = 'Press enter to skip'

    def __init__(self):
        super(ZombieCutScene, self).__init__(
            ZombieCutScene.DEF_NAME, ZombieCutScene.MAP_NAME,
            has_timer=False)
        self.init_enemy()
        # self.show_subtitle(ZombieCutScene.SUBTITLE_TEXT)

    def init_enemy(self):
    	self.enemy = CutSceneEnemy(self.player.rect.centerx,
    							   self.player.rect.top +
    							   ZombieCutScene.NEGATIVE_MARGIN)
    	self.enemySprites.add(self.enemy)

    def update_enemy(self, time):
    	if self.enemy.rect.bottom < self.player.rect.top:
    		self.enemy.rect.bottom += time * ZombieCutScene.VELOCITY

    def event(self, event):
    	if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.handle_escape()

    def init_enemies(self):
    	pass

    def check_collisions(self):
    	pass