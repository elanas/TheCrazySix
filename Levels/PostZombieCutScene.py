from Level import Level
from ZombieCutScene import ZombieCutScene
import pygame
from Globals import Globals


class PostZombieCutScene(Level):
    SUBTITLE_TEXT = 'You are disoriented'
    SUBTITLE_LOOPS = 5

    def __init__(self):
        super(PostZombieCutScene, self).__init__(
            ZombieCutScene.DEF_NAME,
            ZombieCutScene.MAP_NAME,
            should_fade_in=False
        )
        self.overlay_surf = pygame.Surface(
            Globals.SCREEN.get_rect().size).convert()
        self.overlay_surf.fill(ZombieCutScene.OVERLAY_COLOR_SUB)
        self.show_subtitle(PostZombieCutScene.SUBTITLE_TEXT,
                           PostZombieCutScene.SUBTITLE_LOOPS)
        # Globals.stop_cutscene_music()

    def event(self, event):
        if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
            key = event.key
            if key == pygame.K_LEFT:
                key = pygame.K_RIGHT
            elif key == pygame.K_RIGHT:
                key = pygame.K_LEFT
            elif key == pygame.K_UP:
                key = pygame.K_DOWN
            elif key == pygame.K_DOWN:
                key = pygame.K_UP

            if event.type == pygame.KEYDOWN:
                self.handle_keydown(key)
            else:
                self.handle_keyup(key)
        else:
            super(PostZombieCutScene, self).event(event)

    def render_overlay(self):
        Globals.SCREEN.blit(self.overlay_surf, (0, 0),
                            special_flags=pygame.BLEND_SUB)
