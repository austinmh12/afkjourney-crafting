class Recipe:
	def __init__(self, name: str, location: str, cards: int, *stars: int):
		self.name = name
		self.location = location
		self.cards = cards
		self.stars = stars

	def star(self, value: int) -> int:
		# Check if value is less than 1 star
		if value < self.stars[0]:
			return 0
		# Check if value if more than max stars
		if value >= self.stars[-1]:
			return len(self.stars)
		# Else check for betweens
		for i, (st, ed) in enumerate(zip(self.stars[:-1], self.stars[1:]), start=1):
			if st <= value < ed:
				return i

	def __hash__(self) -> int:
		return hash(self.name)