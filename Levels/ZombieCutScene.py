import pygame
from Globals import Globals
from Level import Level
from CutSceneEnemy import CutSceneEnemy
import random


class ZombieCutScene(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'cut_test.txt'
    NEGATIVE_MARGIN = 8
    SHAKE_AMOUNT = 5
    SHAKE_WAIT = .05
    INITIAL_SUBTITLE = 'Press enter to skip'
    INITIAL_TIMES = 3

    def __init__(self):
        super(ZombieCutScene, self).__init__(
            ZombieCutScene.DEF_NAME, ZombieCutScene.MAP_NAME,
            has_timer=False)
        self.init_enemy()
        self.overlay_surf = None
        self.shaking = False
        self.shaking_time = 0
        self.show_subtitle(ZombieCutScene.INITIAL_SUBTITLE,
        				   ZombieCutScene.INITIAL_TIMES)

    def init_enemy(self):
    	self.enemy = CutSceneEnemy(self.player.rect.centerx,
    							   self.player.rect.top +
    							   ZombieCutScene.NEGATIVE_MARGIN,
    							   self)
    	self.enemySprites.add(self.enemy)

    def update(self, time):
    	super(ZombieCutScene, self).update(time)
    	if self.shaking:
    		self.shaking_time += time
    		if self.shaking_time >= ZombieCutScene.SHAKE_WAIT:
    			self.shaking_time = 0
    			self.move_camera()

    def move_camera(self):
    	# if self.old_viewpoint:
	    # 	x_delta = self.old_viewpoint.x - self.camera.viewpoint.x
	    # 	y_delta = self.old_viewpoint.y - self.camera.viewpoint.y
	    # 	self.camera.move(x_delta, y_delta)
    	x_delta = random.randint(-ZombieCutScene.SHAKE_AMOUNT,
    							 ZombieCutScene.SHAKE_AMOUNT)
    	y_delta = random.randint(-ZombieCutScene.SHAKE_AMOUNT,
    							 ZombieCutScene.SHAKE_AMOUNT)
    	self.camera.move(x_delta, y_delta)
    	self.player.rect.left -= x_delta
    	self.player.rect.top -= y_delta
    	self.enemy.rect.left -= x_delta
    	self.enemy.rect.top -= y_delta

    def start_shaking(self):
    	self.shaking_time = 0
    	self.shaking = True
    	self.old_viewpoint = self.camera.viewpoint

    def stop_shaking(self):
    	self.shaking = False
    	x_delta = self.old_viewpoint.x - self.camera.viewpoint.x
    	y_delta = self.old_viewpoint.y - self.camera.viewpoint.y
    	self.camera.move(x_delta, y_delta)
    	self.player.rect.left -= x_delta
    	self.player.rect.top -= y_delta
    	self.enemy.rect.left -= x_delta
    	self.enemy.rect.top -= y_delta

    def render_pre_fade(self):
    	super(ZombieCutScene, self).render_pre_fade()
    	if self.overlay_surf is not None:
    		Globals.SCREEN.blit(self.overlay_surf, (0, 0))
    	if self.showing_subtitle:
            Globals.SCREEN.blit(self.subtitle_surf, self.subtitle_rect)

    def event(self, event):
    	if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.handle_escape()

    def init_enemies(self):
    	pass

    def check_collisions(self):
    	pass

    def handle_pause(self):
    	self.overlay_surf = pygame.Surface(Globals.SCREEN.get_rect().size)
    	self.overlay_surf.fill(pygame.color.Color('red'))
    	self.overlay_surf.set_alpha(70)
    	self.start_shaking()

    def handle_unpause(self):
    	self.overlay_surf = None
    	self.stop_shaking()
