import pygame
import EventManager


class EventPair(object):

    def __init__(self, type=None, value=None, hat=-1, axis=-1):
        self.type = type
        self.value = value
        self.hat = hat
        self.axis = axis

    def match(self, event):
        if EventManager.EventManager.is_keyboard_event(self.type):
            if not EventManager.EventManager.is_keyboard_event(event.type):
                return False
            return self.value == event.key
        elif EventManager.EventManager.is_joystick_event(self.type):
            return self.match_joystick_event(event)
        return False

    def match_joystick_event(self, event):
        if not self.match_joystick_types(event):
            return False
        if self.type in EventManager.EventManager.JOYSTICK_BUTTON_EVENTS:
            
            return self.value == event.button
        elif self.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS:
            return self.hat == event.hat and EventManager.EventManager.hat_values_match(self.value, event.value)
        elif self.type in EventManager.EventManager.JOYSTICK_AXIS_EVENTS:
            return self.axis == event.axis and EventManager.EventManager.axis_values_match(self.value, event.value)
        else:
            # need to handle this
            return False

    def match_joystick_types(self, event):
        return \
            (self.type in EventManager.EventManager.JOYSTICK_BUTTON_EVENTS and event.type in EventManager.EventManager.JOYSTICK_BUTTON_EVENTS) or \
            (self.type in EventManager.EventManager.JOYSTICK_AXIS_EVENTS and event.type in EventManager.EventManager.JOYSTICK_AXIS_EVENTS) or \
            (self.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS and event.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS)

    def is_hat(self):
        return self.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS

    def __eq__(self, other):
        if type(other) is type(self):
            if EventManager.EventManager.is_keyboard_event(self.type) and EventManager.EventManager.is_keyboard_event(other.type):
                return self.value == other.value
            elif self.type in EventManager.EventManager.JOYSTICK_BUTTON_EVENTS and other.type in EventManager.EventManager.JOYSTICK_BUTTON_EVENTS:
                return self.value == other.value
            elif self.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS and other.type in EventManager.EventManager.JOYSTICK_HAT_EVENTS:
                return self.value == other.value
            elif self.type in EventManager.EventManager.JOYSTICK_AXIS_EVENTS and other.type in EventManager.EventManager.JOYSTICK_AXIS_EVENTS:
                return self.axis == other.axis and EventManager.EventManager.axis_values_match(self.value, other.value)
            # need to handle more things
            return False
        else:
            try:
                return self.match(other)
            except AttributeError:
                return False

    def __ne__(self, other):
        return not self.__eq__(other)
