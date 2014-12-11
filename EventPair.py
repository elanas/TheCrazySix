import pygame
from EventManager import EventManager


class EventPair(object):

	def __init__(self, type, id, keydown=True):
		self.type = type
		self.id = id

	def match(self, event):
		if EventManager.is_keyboard_event(self.type):
			if not EventManager.is_keyboard_event(event.type):
				return False
			return self.id == event.key
		elif EventManager.is_joystick_event(self.type):
				return self.match_joystick_event(event)
		return False

	def match_joystick_event(self, event):
		if self.type in EventManager.JOYSTICK_BUTTON_EVENTS:
			return self.id == event.button
		else:
			# need to handle this
			return False

	def __eq__(self, other):
		if type(other) is type(self):
			if EventManager.is_keyboard_event(self.type) and EventManager.is_keyboard_event(other.type):
				return self.id == other.id
			elif self.type in EventManager.JOYSTICK_BUTTON_EVENTS and other.type in EventManager.JOYSTICK_BUTTON_EVENTS:
				return self.id == other.id
			# need to handle more things
			return False
		else:
			try:
				return self.match(other)
			except AttributeError:
				return False

	def __ne__(self, other):
		return not self.__eq__(other)
