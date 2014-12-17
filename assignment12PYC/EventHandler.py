from Globals import Globals


class EventHandler(object):

    def handle_raw_event(self, event):
        pass

    def handle_attack(self):
        pass

    def handle_attack_keyup(self):
        pass

    def handle_action_key(self):
        pass

    def handle_action_keyup(self):
        pass

    def handle_key_down(self, keydown=True):
        pass

    def handle_key_up(self, keydown=True):
        pass

    def handle_key_left(self, keydown=True):
        pass

    def handle_key_right(self, keydown=True):
        pass

    def handle_backspace(self):
        pass

    def handle_backspace_keyup(self):
        pass

    def handle_return(self):
        pass

    def handle_return_keyup(self):
        pass

    def handle_escape(self):
        pass

    def handle_escape_keyup(self):
        pass

    def handle_quit(self):
        Globals.RUNNING = False
