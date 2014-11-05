from Level import Level
from SyringeLevel import SyringeLevel
from asset_loader import AssetLoader
from Globals import Globals
import Menu
import pygame


class IntroScreen(Level):
    LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"
    SOUND_NAME = "intro_sound.ogg"
    SUBTITLE_BACKGROUND = pygame.color.Color("black")
    SUBTITLE_PADDING = 5
    SUBTITLE_TEXT = "Climb the stairs to skip"
    SUBTITLE_COLOR = pygame.color.Color("white")
    SUBTITLE_FONT = pygame.font.Font(None, 32)
    SUBTITLE_MARGIN = 20

    def __init__(self):
        super(IntroScreen, self).__init__(IntroScreen.DEF_NAME,
                                          IntroScreen.MAP_NAME)
        self.audio = None
        if IntroScreen.LOADER is None:
            IntroScreen.LOADER = AssetLoader("images", "sounds")
        self.played_intro = False
        self.alpha_factor = 300
        self.start_music()
        self.init_subtitle()

    def init_subtitle(self):
        text_surf = IntroScreen.SUBTITLE_FONT.render(
            IntroScreen.SUBTITLE_TEXT, True, IntroScreen.SUBTITLE_COLOR)
        self.subtitle_rect = text_surf.get_rect()
        self.subtitle_rect.centerx = Globals.WIDTH / 2
        self.subtitle_rect.bottom = \
            Globals.HEIGHT - IntroScreen.SUBTITLE_MARGIN
        self.subtitle_rect.inflate_ip(
            IntroScreen.SUBTITLE_PADDING * 2,
            IntroScreen.SUBTITLE_PADDING * 2
        )
        self.subtitle_surf = pygame.Surface(self.subtitle_rect.size).convert()
        self.subtitle_surf.fill(IntroScreen.SUBTITLE_BACKGROUND)
        self.subtitle_surf.blit(text_surf, (
            IntroScreen.SUBTITLE_PADDING,
            IntroScreen.SUBTITLE_PADDING
        ))
        self.subtitle_surf.set_alpha(255)

    def render_pre_fade(self):
        if self.played_intro:
            Globals.SCREEN.blit(self.subtitle_surf, self.subtitle_rect)

    def update(self, time):
        super(IntroScreen, self).update(time)
        old_alpha = self.subtitle_surf.get_alpha()
        if old_alpha == 0 or old_alpha == 255:
            self.alpha_factor *= -1
        new_alpha = int(old_alpha + self.alpha_factor * time)
        if new_alpha < 0:
            new_alpha = 0
        elif new_alpha > 255:
            new_alpha = 255
        self.subtitle_surf.set_alpha(new_alpha)

    def handle_stairs(self):
        self.start_fade_out()
        self.stop_music()
        # Globals.STATE = SyringeLevel()

    def handle_finish_fade_out(self):
        Globals.STATE = SyringeLevel()

    def handle_escape(self):
        self.stop_music()
        Globals.STATE = Menu.Menu()

    def start_music(self):
        if not Globals.INTRO_SOUND_PLAYED:
            self.played_intro = True
            Globals.INTRO_SOUND_PLAYED = True
            self.audio = IntroScreen.LOADER.load_sound(IntroScreen.SOUND_NAME)
            self.audio.play()

    def stop_music(self):
        if self.audio is not None:
            self.audio.stop()
