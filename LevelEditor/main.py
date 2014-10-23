import pygame
from Globals import Globals
from LevelEditor import LevelEditor
import sys
import os

MIN_UPDATE_INTERVAL = .05

def create_map_file(file_path):
    if not os.path.isfile(file_path):
        print 'Creating empty map at "' + file_path + '"'
    handle = open(file_path, 'a')
    handle.close()

def initialize():
    if len(sys.argv) < 3:
        print "The level editor should be run as:"
        print "\t python main.py [definition file path] [map file path]"
        sys.exit(1)
    def_file = sys.argv[1]
    map_file = sys.argv[2]
    if not os.path.isfile(def_file):
        print '"' + def_file + '" is not a valid file path.'
        sys.exit(1200)
    create_map_file(map_file)
    pygame.init()
    pygame.display.set_caption('The Crazy Six - Level Editor')
    Globals.WIDTH = 1200
    Globals.HEIGHT = 800
    Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    Globals.STATE = LevelEditor(def_file, map_file)

def loop():
    time_elapsed = 0
    while Globals.RUNNING:
        last = pygame.time.get_ticks()
        Globals.STATE.render()
        pygame.display.flip()
        elapsed = (pygame.time.get_ticks() - last) / 1000.0
        time_elapsed += elapsed
        if time_elapsed >= MIN_UPDATE_INTERVAL:
            Globals.STATE.update(time_elapsed)
            time_elapsed -= MIN_UPDATE_INTERVAL

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Globals.RUNNING = False
            else:
                Globals.STATE.event(event)

def main():
    initialize()
    loop()

if __name__ == '__main__':
    main()
