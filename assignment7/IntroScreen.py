from Level import Level
from TileTest import TileTest
from asset_loader import AssetLoader
from Globals import Globals
import Menu

class IntroScreen(Level):
    LOADER = None
    DEF_NAME = "map_def.txt"
    MAP_NAME = "intro_screen.txt"

    def __init__(self):
        super(IntroScreen, self).__init__(IntroScreen.DEF_NAME,
                                          IntroScreen.MAP_NAME)
        if IntroScreen.LOADER is None:
            IntroScreen.LOADER = AssetLoader("images", "sounds")
        self.start_music()

    def handle_stairs(self):
        self.stop_music()
        Globals.STATE = TileTest()

    def handle_escape(self):
        Globals.STATE = Menu.Menu()

    def start_music(self):
        # TODO - start music if needed
        # can load sound file with IntroScreen.LOADER.load_sound(...)
        pass

    def stop_music(self):
        # TODO
        pass