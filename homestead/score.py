from random import random

from .stack import Stack

class Score:
	def __init__(self):
		self.left = 1
		self.right = 1
		self.stack = Stack() # For forging and alchemy
		self.redist: bool = False
		self.post_double: bool = False
		self._calculated: bool = False

	@property
	def total(self) -> int:
		# End of process actions need to be processed
		if not self._calculated:
			if self.post_double:
				self.double_random()
			if self.redist:
				self.redistribute()
			self._calculated = True
		return self.left * self.right

	def add_random(self, value: int):
		if random() <= .5:
			self.left += value
		else:
			self.right += value

	def add_highest(self, value: int):
		if self.left <= self.right:
			self.right += value
		else:
			self.left += value

	def add_lowest(self, value: int):
		if self.left <= self.right:
			self.left += value
		else:
			self.right += value

	def add_all(self, value: int):
		self.left += value
		self.right += value

	def double_random(self):
		if random() <= .5:
			self.left *= 2
		else:
			self.right *= 2

	def double_highest(self):
		if self.left <= self.right:
			self.right *= 2
		else:
			self.left *= 2

	def double_lowest(self):
		if self.left <= self.right:
			self.left *= 2
		else:
			self.right *= 2

	def redistribute(self):
		new_val = (self.right + self.left) // 2
		self.left = new_val
		self.right = new_val

	def __str__(self) -> str:
		return f'{self.left}x{self.right} ({self.total})'

	def __lt__(self, o: object) -> bool:
		return isinstance(o, Score) and self.total < o.total