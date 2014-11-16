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
    HIT_ALPHA = 70
    POST_HIT_ALPHA = 40
    OVERLAY_COLOR_SUB = (0, 70, 70)

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
       	self.overlay_sub = False

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
    	self.camera.viewpoint.x = self.old_viewpoint.x
    	self.camera.viewpoint.y = self.old_viewpoint.y
    	self.camera.move(x_delta, y_delta)
    	self.player.rect.x = self.old_player_rect.x + x_delta
    	self.player.rect.y = self.old_player_rect.y + y_delta
    	self.enemy.rect.x = self.old_enemy_rect.x + x_delta
    	self.enemy.rect.y = self.old_enemy_rect.y + y_delta

    def start_shaking(self):
    	self.shaking_time = 0
    	self.shaking = True
    	self.old_viewpoint = pygame.Rect.copy(self.camera.viewpoint)
    	self.old_player_rect = pygame.Rect.copy(self.player.rect)
    	self.old_enemy_rect = pygame.Rect.copy(self.enemy.rect)

    def stop_shaking(self):
    	self.shaking = False
    	self.camera.viewpoint.x = self.old_viewpoint.x
    	self.camera.viewpoint.y = self.old_viewpoint.y
    	self.camera.surface_ready = False
    	self.player.rect.x = self.old_player_rect.x
    	self.player.rect.y = self.old_player_rect.y
    	self.enemy.rect.x = self.old_enemy_rect.x
    	self.enemy.rect.y = self.old_enemy_rect.y

    def render_pre_fade(self):
    	super(ZombieCutScene, self).render_pre_fade()
    	if self.overlay_surf is not None:
    		Globals.SCREEN.blit(self.overlay_surf, (0, 0), special_flags=pygame.BLEND_SUB)
    	if self.showing_subtitle:
            Globals.SCREEN.blit(self.subtitle_surf, self.subtitle_rect)

    def event(self, event):
    	if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.handle_escape()
            elif event.key == pygame.K_RETURN:
            	self.handle_done()

    def init_enemies(self):
    	pass

    def check_collisions(self):
    	pass

    def handle_pause(self):
    	self.overlay_surf = pygame.Surface(Globals.SCREEN.get_rect().size).convert()
    	self.overlay_surf.fill(ZombieCutScene.OVERLAY_COLOR_SUB)
    	self.start_shaking()

    def handle_unpause(self):
    	self.stop_shaking()

    def handle_done(self):
    	self.handle_finish_fade_out()