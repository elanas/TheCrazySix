from EventPair import EventPair
import pygame
import re


class SettingsManager(object):
    COMMENT_CHAR = '#'
    DEFAULT_PATH = 'settings.txt'
    LABEL_SEPARATOR = ':: '
    VOLUME_LABEL = 'volume'
    BRIGHTNESS_LABEL = 'brightness'
    MIN_BRIGHTNESS = 30
    MIN_VOLUME = 0
    MAX_BRIGHTNESS = 100
    MAX_VOLUME = 100
    DEFAULT_VOLUME = 100
    DEFAULT_BRIGHTNESS = 100
    VOLUME = None
    BRIGHTNESS = None
    LOADED = False
    EVENT_LABEL_POSTFIX = '_event'
    UP_LABEL = 'up' + EVENT_LABEL_POSTFIX
    DOWN_LABEL = 'down' + EVENT_LABEL_POSTFIX
    LEFT_LABEL = 'left' + EVENT_LABEL_POSTFIX
    RIGHT_LABEL = 'right' + EVENT_LABEL_POSTFIX
    ACTION_LABEL = 'action' + EVENT_LABEL_POSTFIX
    ESCAPE_LABEL = 'escape' + EVENT_LABEL_POSTFIX
    RETURN_LABEL = 'return' + EVENT_LABEL_POSTFIX
    BACKSPACE_LABEL = 'backspace' + EVENT_LABEL_POSTFIX
    EVENTS_UP = []
    EVENTS_DOWN = []
    EVENTS_LEFT = []
    EVENTS_RIGHT = []
    EVENTS_ACTION = []
    EVENTS_ESCAPE = []
    EVENTS_RETURN = []
    EVENTS_BACKSPACE = []
    DEFAULT_UP = [EventPair(type=pygame.KEYDOWN, value=pygame.K_UP)]
    DEFAULT_DOWN = [EventPair(type=pygame.KEYDOWN, value=pygame.K_DOWN)]
    DEFAULT_LEFT = [EventPair(type=pygame.KEYDOWN, value=pygame.K_LEFT)]
    DEFAULT_RIGHT = [EventPair(type=pygame.KEYDOWN, value=pygame.K_RIGHT)]
    DEFAULT_ACTION = [EventPair(type=pygame.KEYDOWN, value=pygame.K_SPACE)]
    DEFAULT_ESCAPE = [EventPair(type=pygame.KEYDOWN, value=pygame.K_ESCAPE)]
    DEFAULT_RETURN = [EventPair(type=pygame.KEYDOWN, value=pygame.K_RETURN)]
    DEFAULT_BACKSPACE = [EventPair(type=pygame.KEYDOWN, value=pygame.K_BACKSPACE)]

    @staticmethod
    def load(file_path=DEFAULT_PATH):
        SettingsManager.VOLUME = SettingsManager.DEFAULT_VOLUME
        SettingsManager.BRIGHTNESS = SettingsManager.DEFAULT_BRIGHTNESS
        SettingsManager.EVENTS_UP = SettingsManager.DEFAULT_UP
        SettingsManager.EVENTS_DOWN = SettingsManager.DEFAULT_DOWN
        SettingsManager.EVENTS_LEFT = SettingsManager.DEFAULT_LEFT
        SettingsManager.EVENTS_RIGHT = SettingsManager.DEFAULT_RIGHT
        SettingsManager.EVENTS_ACTION = SettingsManager.DEFAULT_ACTION
        SettingsManager.EVENTS_ESCAPE = SettingsManager.DEFAULT_ESCAPE
        SettingsManager.EVENTS_RETURN = SettingsManager.DEFAULT_RETURN
        SettingsManager.EVENTS_BACKSPACE = SettingsManager.DEFAULT_BACKSPACE
        try:
            with open(file_path, 'r') as file_handle:
                for line in [l.strip() for l in file_handle]:
                    if len(line) == 0 or \
                            line[0] == SettingsManager.COMMENT_CHAR:
                        continue
                    parts = line.split(SettingsManager.LABEL_SEPARATOR)
                    if len(parts) != 2:
                        raise Exception('The settings file is malformed.')
                    label, value = parts
                    if label.endswith(SettingsManager.EVENT_LABEL_POSTFIX):
                        # try:
                        value = SettingsManager.convert_events(value)
                        # except Exception as e:
                        #     # raise Exception('The settings file is malformed.')
                        #     raise e
                    SettingsManager.set_label_value(label, value)
        except IOError:
            pass
        SettingsManager.LOADED = True

    @staticmethod
    def convert_events(value):
        event_list = list()
        for event_dict in [a.strip() for a in value.split('}')]:
            if len(event_dict) == 0:
                continue
            event_dict = event_dict[1:]  # cut off '{'
            event_list.append(SettingsManager.convert_event(event_dict))
        return event_list

    @staticmethod
    def convert_event(event_dict):
        pair = EventPair()
        r = re.compile(r'(?:[^,(]|\([^)]*\))+')
        for keyvalue in [a.strip() for a in r.findall(event_dict)]:
            key, value = keyvalue.split(': ')
            key = key.replace("'", "")
            value = SettingsManager.convert_event_value(value)
            SettingsManager.add_event_attribute(pair, key, value)
        return pair

    @staticmethod
    def add_event_attribute(eventpair, key, value):
        if key == 'hat':
            eventpair.hat = value
        elif key == 'type':
            eventpair.type = value
        elif key == 'value':
            eventpair.value = value
        elif key == 'axis':
            eventpair.axis = value
        else:
            raise Exception('Attribute "' + key + '" is not recognized.')

    @staticmethod
    def convert_event_value(value):
        if value.startswith('('):
            value = value.replace('(', '').replace(')', '')
            values = tuple(int(v.strip()) for v in value.split(','))
            return values
        else:
            return int(value)

    @staticmethod
    def set_label_value(label, value):
        label = label.lower()
        if SettingsManager.BRIGHTNESS_LABEL == label:
            value = SettingsManager.to_int(label, value)
            if SettingsManager.MIN_BRIGHTNESS > value or \
                    value > SettingsManager.MAX_BRIGHTNESS:
                raise Exception(
                    'The brightness value must be in the range [30, 100]')
            SettingsManager.BRIGHTNESS = value
        elif SettingsManager.VOLUME_LABEL == label:
            value = SettingsManager.to_float(label, value)
            if SettingsManager.MIN_VOLUME > value or \
                    value > SettingsManager.MAX_VOLUME:
                raise Exception(
                    'The volume value must be in the range [0, 100]')
            SettingsManager.VOLUME = value
        elif SettingsManager.UP_LABEL == label:
            SettingsManager.EVENTS_UP = value
        elif SettingsManager.DOWN_LABEL == label:
            SettingsManager.EVENTS_DOWN = value
        elif SettingsManager.LEFT_LABEL == label:
            SettingsManager.EVENTS_LEFT = value
        elif SettingsManager.RIGHT_LABEL == label:
            SettingsManager.EVENTS_RIGHT = value
        elif SettingsManager.ACTION_LABEL == label:
            SettingsManager.EVENTS_ACTION = value
        elif SettingsManager.ESCAPE_LABEL == label:
            SettingsManager.EVENTS_ESCAPE = value
        elif SettingsManager.BACKSPACE_LABEL == label:
            SettingsManager.EVENTS_BACKSPACE = value
        elif SettingsManager.RETURN_LABEL == label:
            SettingsManager.EVENTS_RETURN = value
        else:
            raise Exception('The settings label "' + label + '" is invalid.')

    @staticmethod
    def to_int(label, str_val):
        try:
            return int(str_val)
        except ValueError:
            raise Exception('The value "' + str_val +
                            '" for the settings label "' + label +
                            '" is invalid')

    @staticmethod
    def to_float(label, str_val):
        try:
            return float(str_val)
        except ValueError:
            raise Exception('The value "' + str_val +
                            '" for the settings label "' + label +
                            '" is invalid')

    @staticmethod
    def set_brightness(value, file_path=DEFAULT_PATH):
        SettingsManager.BRIGHTNESS = value
        SettingsManager.save(file_path)

    @staticmethod
    def set_volume(value, file_path=DEFAULT_PATH):
        SettingsManager.VOLUME = value
        SettingsManager.save(file_path)

    @staticmethod
    def save(file_path=DEFAULT_PATH):
        try:
            with open(file_path, 'w') as file_handle:
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.BRIGHTNESS_LABEL,
                                             SettingsManager.BRIGHTNESS)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.VOLUME_LABEL,
                                             SettingsManager.VOLUME)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.UP_LABEL,
                                             SettingsManager.EVENTS_UP,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.DOWN_LABEL,
                                             SettingsManager.EVENTS_DOWN,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.LEFT_LABEL,
                                             SettingsManager.EVENTS_LEFT,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.RIGHT_LABEL,
                                             SettingsManager.EVENTS_RIGHT,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.ACTION_LABEL,
                                             SettingsManager.EVENTS_ACTION,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.ESCAPE_LABEL,
                                             SettingsManager.EVENTS_ESCAPE,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.RETURN_LABEL,
                                             SettingsManager.EVENTS_RETURN,
                                             is_event_list=True)
                SettingsManager.save_setting(file_handle,
                                             SettingsManager.BACKSPACE_LABEL,
                                             SettingsManager.EVENTS_BACKSPACE,
                                             is_event_list=True)
        except IOError as e:
            print 'An error occurred while saving the settings file:'
            print e

    @staticmethod
    def save_setting(file_handle, label, value, is_event_list=False):
        file_handle.write(label)
        file_handle.write(SettingsManager.LABEL_SEPARATOR)
        if not is_event_list:
            file_handle.write(str(value))
        else:
            str_rep = ""
            for pair in value:
                str_rep += str(pair.__dict__)
            file_handle.write(str_rep)
        file_handle.write('\n')
