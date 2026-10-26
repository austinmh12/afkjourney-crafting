from random import choice

from .stack import Stack

class Score:
	def __init__(self, has_middle: bool = False):
		self.left = 1
		self.middle = 1
		self.right = 1
		self.has_middle = has_middle
		self.stack = Stack() # For forging
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
		return self.left * self.middle * self.right

	def add_random(self, value: int):
		vals = ['l', 'r', 'm'] if self.has_middle else ['l', 'r']
		c = choice(vals)
		if c == 'l':
			self.left += value
		elif c == 'r':
			self.right += value
		else:
			self.middle += value

	def add_highest(self, value: int):
		vals = [('l', self.left), ('m', self.middle), ('r', self.right)]
		if not self.has_middle:
			vals.remove(('m', self.middle))
		highest = max(vals, key=lambda x: x[1])
		if highest[0] == 'l':
			self.left += value
		elif highest[0] == 'r':
			self.right += value
		else:
			self.middle += value

	def add_lowest(self, value: int):
		vals = [('l', self.left), ('m', self.middle), ('r', self.right)]
		if not self.has_middle:
			vals.remove(('m', self.middle))
		lowest = min(vals, key=lambda x: x[1])
		if lowest[0] == 'l':
			self.left += value
		elif lowest[0] == 'r':
			self.right += value
		else:
			self.middle += value

	def add_all(self, value: int):
		self.left += value
		self.right += value
		if self.has_middle:
			self.middle += value

	def double_random(self):
		vals = ['l', 'r', 'm'] if self.has_middle else ['l', 'r']
		c = choice(vals)
		if c == 'l':
			self.left *= 2
		elif c == 'r':
			self.right *= 2
		else:
			self.middle *= 2

	def double_highest(self):
		vals = [('l', self.left), ('m', self.middle), ('r', self.right)]
		if not self.has_middle:
			vals.remove(('m', self.middle))
		highest = max(vals, key=lambda x: x[1])
		if highest[0] == 'l':
			self.left *= 2
		elif highest[0] == 'r':
			self.right *= 2
		else:
			self.middle *= 2

	def double_lowest(self):
		vals = [('l', self.left), ('m', self.middle), ('r', self.right)]
		if not self.has_middle:
			vals.remove(('m', self.middle))
		lowest = min(vals, key=lambda x: x[1])
		if lowest[0] == 'l':
			self.left *= 2
		elif lowest[0] == 'r':
			self.right *= 2
		else:
			self.middle *= 2

	def redistribute(self):
		vals = [self.left, self.right]
		if self.has_middle:
			vals.append(self.middle)
		new_val = sum(vals) // len(vals)
		self.left = new_val
		self.right = new_val
		if self.has_middle:
			self.middle = new_val

	def __str__(self) -> str:
		if self.has_middle:
			return f'{self.left}x{self.middle}x{self.right} ({self.total})'
		return f'{self.left}x{self.right} ({self.total})'

	def __lt__(self, o: object) -> bool:
		return isinstance(o, Score) and self.total < o.total