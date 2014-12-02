

class SettingsManager(object):
    COMMENT_CHAR = '#'
    DEFAULT_PATH = 'settings.txt'
    LABEL_SEPARATOR = ': '
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

    @staticmethod
    def load(file_path=DEFAULT_PATH):
        SettingsManager.VOLUME = SettingsManager.DEFAULT_VOLUME
        SettingsManager.BRIGHTNESS = SettingsManager.DEFAULT_BRIGHTNESS
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
                    SettingsManager.set_label_value(label, value)
        except IOError:
            pass
        SettingsManager.LOADED = True

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
        except IOError as e:
            print 'An error occurred while saving the settings file:'
            print e

    @staticmethod
    def save_setting(file_handle, label, value):
        file_handle.write(label)
        file_handle.write(SettingsManager.LABEL_SEPARATOR)
        file_handle.write(str(value))
        file_handle.write('\n')
