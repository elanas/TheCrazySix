import pygame
from Level import Level
from TileSystem.TileType import TileType


class SyringeLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'dodge.txt'
    SUBTITLE_TEXT = 'Watch out for syringes'
    SUBTITLE_LOOPS = 3

    def __init__(self):
        super(SyringeLevel, self).__init__(
            SyringeLevel.DEF_NAME, SyringeLevel.MAP_NAME)
        self.show_subtitle(SyringeLevel.SUBTITLE_TEXT, SyringeLevel.SUBTITLE_LOOPS)

    def event(self, event):
        super(SyringeLevel, self).event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            radius = max(self.player.rect.size) * 2
            special_tiles = self.camera.get_special_tiles(
            self.player.rect.center, radius)
            self.check_lever_collision(special_tiles)

    def check_lever_collision(self, special_tiles):
        lever_rects = [pair.rect for pair in special_tiles
                        if TileType.LEVER_LEFT_ATTR in pair.tile.special_attr]
        temp_rect = self.player.rect.inflate(
            -Player.LEVER_OFFSET, -Player.LEVER_OFFSET)
        num_lever_left = len(temp_rect.collidelistall(lever_rects))
        if num_lever_left > 0:
            self.handle_lever_on()
    def handle_lever_on(self):
        for turret in self.turrets:
            turret.turn_off()