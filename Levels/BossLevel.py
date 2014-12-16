import pygame
from Level import Level
from TileSystem.TileType import TileType
from Player import Player
from Globals import Globals


class BossLevel(Level):
    DEF_NAME = 'map_def.txt'
    MAP_NAME = 'boss.txt'
    SUBTITLE_TEXT = 'Find the antidote'
    SUBTITLE_LOOPS = 3
    VOICE_OVER = 'transition4.ogg'
    ROOM_VOICE_OVER = 'transition5.ogg'
    KILL_VOICE_OVER = 'transition6.ogg'
    MUSIC_PATH = 'syringe_level.ogg'
    NEW_END_ID = None

    def __init__(self, mid=0):
        BossLevel.NEW_END_ID = mid + 1
        super(BossLevel, self).__init__(
            BossLevel.DEF_NAME, 
            BossLevel.MAP_NAME,
            init_music_path=BossLevel.VOICE_OVER,
            music_path=BossLevel.MUSIC_PATH, mid=mid)
        self.show_subtitle(
            BossLevel.SUBTITLE_TEXT,
            BossLevel.SUBTITLE_LOOPS
        )
        self.room_sound_handle = self.loader.load_sound(
            BossLevel.ROOM_VOICE_OVER)
        self.kill_sound_handle = self.loader.load_sound(
            BossLevel.KILL_VOICE_OVER)
        self.first_special_door = True
        self.killed_all = False

    def handle_special_door(self):
        if self.first_special_door:
            self.first_special_door = False
            self.channel.set_endevent(BossLevel.NEW_END_ID)
            self.stop_music()
            self.switched_sound = False
            self.music_handle = self.room_sound_handle
            self.start_music()
            self.can_open_doors = False

    def update(self, time):
        super(BossLevel, self).update(time)
        if not self.killed_all and Globals.NUM_BOSSES == 0:
            self.killed_all = True
            self.handle_kill_all()

    def handle_kill_all(self):
        self.channel.set_endevent(BossLevel.NEW_END_ID)
        self.stop_music()
        self.switched_sound = False
        self.music_handle = self.kill_sound_handle
        self.start_music()
        self.can_open_doors = True

    def handle_antidote(self):
        pass
