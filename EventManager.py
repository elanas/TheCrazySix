import pygame
from Globals import Globals


class EventManager(object):
    JOYSTICK_EVENTS = set([
        pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION,
        pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN
    ])
    JOYSTICK_BUTTON_EVENTS = set([pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN])
    JOYSTICK_AXIS_EVENTS = set([pygame.JOYAXISMOTION])
    KEYBOARD_EVENTS = set([pygame.KEYUP, pygame.KEYDOWN])

    def __init__(self):
        self.joysticks = list()
        self.init_joysticks()

    def init_joysticks(self):
        pygame.init()
        num_joysticks = pygame.joystick.get_count()
        for i in range(0, num_joysticks):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    @staticmethod
    def is_joystick_event(event_type):
        return event_type in EventManager.JOYSTICK_EVENTS

    @staticmethod
    def is_keyboard_event(event_type):
        return event_type in EventManager.KEYBOARD_EVENTS

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._send_quit()
            elif event in Globals.EVENTS_RETURN:
                self._send_return(event)
            elif event in Globals.EVENTS_ESCAPE:
                self._send_escape(event)
            elif event in Globals.EVENTS_ACTION:
                self._send_action_key(event)
            elif self.handle_joystick_event(event):
                pass
            elif self.handle_keyboard_event(event):
                pass
            self._send_raw(event)

    def handle_joystick_event(self, event):
        if not EventManager.is_joystick_event(event.type):
            return False
        if event.type in EventManager.JOYSTICK_BUTTON_EVENTS:
            self.handle_joystick_button(event)
        return True

    def handle_joystick_button(self, event):
        keydown = event.type == pygame.JOYBUTTONDOWN
        self.handle_simple_event(event, keydown)

    def handle_keyboard_event(self, event):
        if not EventManager.is_keyboard_event(event.type):
            return False
        keydown = event.type == pygame.KEYDOWN
        self.handle_simple_event(event, keydown)
        return True

    def handle_simple_event(self, event, keydown):
        if event in Globals.EVENTS_UP:
            self._send_key_up(keydown)
        elif event in Globals.EVENTS_DOWN:
            self._send_key_down(keydown)
        elif event in Globals.EVENTS_LEFT:
            self._send_key_left(keydown)
        elif event in Globals.EVENTS_RIGHT:
            self._send_key_right(keydown)
        elif event in Globals.EVENTS_BACKSPACE:
            self._send_backspace(keydown)

    def _send_raw(self, event):
        Globals.STATE.handle_raw_event(event)

    def _send_key_down(self, keydown):
        Globals.STATE.handle_key_down(keydown=keydown)

    def _send_key_up(self, keydown):
        Globals.STATE.handle_key_up(keydown=keydown)

    def _send_key_left(self, keydown):
        Globals.STATE.handle_key_left(keydown=keydown)

    def _send_key_right(self, keydown):
        Globals.STATE.handle_key_right(keydown=keydown)

    def _send_backspace(self, keydown):
        Globals.STATE.handle_backspace(keydown=keydown)

    def _send_return(self, event):
        if self.is_keydown(event):
            Globals.STATE.handle_return()

    def _send_action_key(self, event):
        if self.is_keydown(event):
            Globals.STATE.handle_action_key()

    def _send_escape(self, event):
        if self.is_keydown(event):
            Globals.STATE.handle_escape()

    def _send_quit(self):
        Globals.STATE.handle_quit()

    def is_keydown(self, event):
        return event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN
