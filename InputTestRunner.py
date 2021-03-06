from EventManager import EventManager
from GameState import GameState
from Globals import Globals
from SettingsManager import SettingsManager
import sys
import pygame


class TestInput(GameState):

    def handle_raw_event(self, event):
        result = '\t' + pygame.event.event_name(event.type)
        if EventManager.is_keyboard_event(event.type):
            result += '\t' + pygame.key.name(event.key)
        elif event.type in EventManager.JOYSTICK_BUTTON_EVENTS:
            result += '\t' + str(event.button)
        elif event.type in EventManager.JOYSTICK_AXIS_EVENTS:
            result += '\tjoy: ' + \
                str(event.joy) + '\taxis: ' + str(event.axis) + \
                '\tvalue: ' + '%.3f' % (event.value)
        elif event.type in EventManager.JOYSTICK_HAT_EVENTS:
            result += '\tjoy: ' + \
                str(event.joy) + '\that: ' + str(event.hat) + \
                '\tvalue: ' + str(event.value)
        elif EventManager.is_joystick_event(event.type):
            result = '\t' + str(event)
        else:
            return
        print result

    def handle_attack(self):
        print 'ATTACK'

    def handle_attack_keyup(self):
        print 'ATTACK RELEASE'

    def handle_action_key(self):
        print 'ACTION'

    def handle_action_keyup(self):
        print 'ACTION RELEASE'

    def handle_key_down(self, keydown=True):
        print 'DOWN', keydown

    def handle_key_up(self, keydown=True):
        print 'UP', keydown

    def handle_key_left(self, keydown=True):
        print 'LEFT', keydown

    def handle_key_right(self, keydown=True):
        print 'RIGHT', keydown

    def handle_backspace(self):
        print 'BACKSPACE'

    def handle_backspace_keyup(self):
        print 'BACKSPACE RELEASE'

    def handle_return(self):
        print 'RETURN'

    def handle_return_keyup(self):
        print 'RETURN RELEASE'

    def handle_escape(self):
        print 'ESCAPE'

    def handle_escape_keyup(self):
        print 'ESCAPE RELEASE'

    def render(self):
        Globals.SCREEN.fill((0, 0, 0))


if __name__ == '__main__':
    SettingsManager.load()
    Globals.EVENT_MANAGER = EventManager()
    Globals.STATE = TestInput()
    pygame.init()
    Globals.WIDTH = 150
    Globals.HEIGHT = 150
    Globals.SCREEN = pygame.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    while Globals.RUNNING:
        Globals.STATE.render()
        pygame.display.flip()
        Globals.EVENT_MANAGER.check_events()
