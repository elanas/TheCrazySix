import pygame
from Globals import Globals


DIRECTIONAL_STATUS = [False for i in range(0, 4)]
STATUS_UP = 0
STATUS_DOWN = 1
STATUS_RIGHT = 2
STATUS_LEFT = 3


class EventManager(object):
    FLOAT_ERROR = .001
    HAT_BASE = (0, 0)
    JOYSTICK_EVENTS = set([
        pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION,
        pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN
    ])
    JOYSTICK_BUTTON_EVENTS = set([pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN])
    JOYSTICK_AXIS_EVENTS = set([pygame.JOYAXISMOTION])
    JOYSTICK_HAT_EVENTS = set([pygame.JOYHATMOTION])
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
            elif event in Globals.EVENTS_BACKSPACE:
                self._send_backspace(event)
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
        elif event.type in EventManager.JOYSTICK_HAT_EVENTS or event.type in EventManager.JOYSTICK_AXIS_EVENTS:
            self.handle_joystick_other(event)
        return True

    def handle_joystick_button(self, event):
        keydown = event.type == pygame.JOYBUTTONDOWN
        self.handle_directional_event(event, keydown)

    def handle_joystick_other(self, event):
        directional = self.handle_directional_event(event, True)
        if directional != -1 or self.should_keyup_directionals(event):
            self._send_keyup_directionals(ignore_id=directional)

    def handle_keyboard_event(self, event):
        if not EventManager.is_keyboard_event(event.type):
            return False
        keydown = event.type == pygame.KEYDOWN
        self.handle_directional_event(event, keydown)
        return True

    def handle_directional_event(self, event, keydown):
        if event in Globals.EVENTS_UP:
            self._send_key_up(keydown)
            return STATUS_UP
        elif event in Globals.EVENTS_DOWN:
            self._send_key_down(keydown)
            return STATUS_DOWN
        elif event in Globals.EVENTS_LEFT:
            self._send_key_left(keydown)
            return STATUS_LEFT
        elif event in Globals.EVENTS_RIGHT:
            self._send_key_right(keydown)
            return STATUS_RIGHT
        else:
            return -1

    def should_keyup_directionals(self, event):
        if event.type in EventManager.JOYSTICK_HAT_EVENTS:
            return self.should_keyup_directionals_hat(event)
        elif event.type in EventManager.JOYSTICK_AXIS_EVENTS:
            return self.should_keyup_directionals_axis(event)
        return False

    def should_keyup_directionals_hat(self, event):
        if EventManager.hat_event_in(event, Globals.EVENTS_UP) and DIRECTIONAL_STATUS[STATUS_UP]:
            return True
        elif EventManager.hat_event_in(event, Globals.EVENTS_DOWN) and DIRECTIONAL_STATUS[STATUS_DOWN]:
            return True
        elif EventManager.hat_event_in(event, Globals.EVENTS_RIGHT) and DIRECTIONAL_STATUS[STATUS_RIGHT]:
            return True
        elif EventManager.hat_event_in(event, Globals.EVENTS_LEFT) and DIRECTIONAL_STATUS[STATUS_LEFT]:
            return True
        return False

    def should_keyup_directionals_axis(self, event):
        if EventManager.axis_event_in(event, Globals.EVENTS_UP) and DIRECTIONAL_STATUS[STATUS_UP]:
            return True
        elif EventManager.axis_event_in(event, Globals.EVENTS_DOWN) and DIRECTIONAL_STATUS[STATUS_DOWN]:
            return True
        elif EventManager.axis_event_in(event, Globals.EVENTS_RIGHT) and DIRECTIONAL_STATUS[STATUS_RIGHT]:
            return True
        elif EventManager.axis_event_in(event, Globals.EVENTS_LEFT) and DIRECTIONAL_STATUS[STATUS_LEFT]:
            return True
        return False

    @staticmethod
    def hat_event_in(event, event_list, match_base=True):
        for e in event_list:
            if e.type in EventManager.JOYSTICK_HAT_EVENTS and EventManager.hat_values_match(event.value, e.value, match_base=match_base):
                return True
        return False

    @staticmethod
    def axis_event_in(event, event_list, match_base=True):
        for e in event_list:
            if e.type in EventManager.JOYSTICK_AXIS_EVENTS and EventManager.axis_values_match(event.value, e.value, match_base=match_base):
                return True
        return False

    @staticmethod
    def hat_values_match(value0, value1, match_base=False):
        if match_base and (value0 == EventManager.HAT_BASE or value1 == EventManager.HAT_BASE):
            return True
        return value0 == value1

    @staticmethod
    def axis_values_match(value0, value1, match_base=False):
        near0 = EventManager.nearly_zero(value0)
        near1 = EventManager.nearly_zero(value1)
        if match_base and (near0 or near1):
            return True
        if not near0 and not near1:
            return (value0 < 0 and value1 < 0) or (value0 > 0 and value1 > 0)
        else:
            return near0 and near1

    @staticmethod
    def nearly_zero(value):
        return EventManager.nearly_equal(value, 0)

    @staticmethod
    def nearly_equal(value0, value1):
        return abs(value0 - value1) < EventManager.FLOAT_ERROR

    @staticmethod
    def hat_used_directional():
        return \
            EventManager.count_hat_pairs(Globals.EVENTS_UP) > 0 or \
            EventManager.count_hat_pairs(Globals.EVENTS_DOWN) > 0 or \
            EventManager.count_hat_pairs(Globals.EVENTS_LEFT) > 0 or \
            EventManager.count_hat_pairs(Globals.EVENTS_RIGHT) > 0

    @staticmethod
    def count_hat_pairs(pair_list):
        return len([pair for pair in pair_list if pair.is_hat()])

    def _send_raw(self, event):
        Globals.STATE.handle_raw_event(event)

    def _send_keyup_directionals(self, ignore_id=-1):
        if ignore_id != STATUS_DOWN:
            self._send_key_down(False)
        if ignore_id != STATUS_UP:
            self._send_key_up(False)
        if ignore_id != STATUS_LEFT:
            self._send_key_left(False)
        if ignore_id != STATUS_RIGHT:
            self._send_key_right(False)

    def _send_key_down(self, keydown):
        DIRECTIONAL_STATUS[STATUS_DOWN] = keydown
        Globals.STATE.handle_key_down(keydown=keydown)

    def _send_key_up(self, keydown):
        DIRECTIONAL_STATUS[STATUS_UP] = keydown
        Globals.STATE.handle_key_up(keydown=keydown)

    def _send_key_left(self, keydown):
        DIRECTIONAL_STATUS[STATUS_LEFT] = keydown
        Globals.STATE.handle_key_left(keydown=keydown)

    def _send_key_right(self, keydown):
        DIRECTIONAL_STATUS[STATUS_RIGHT] = keydown
        Globals.STATE.handle_key_right(keydown=keydown)

    def _send_backspace(self, event):
        if self.is_keydown(event):
            Globals.STATE.handle_backspace()

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
        return event.type == pygame.KEYDOWN or \
            event.type == pygame.JOYBUTTONDOWN or \
            event.type in EventManager.JOYSTICK_HAT_EVENTS and not event.value == EventManager.HAT_BASE
