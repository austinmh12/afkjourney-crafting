from random import randint, random as rand

from .score import Score

# Core class for cards, implements the properties and dunders
# and has a placeholder for the score function
class Card:
	def __init__(
		self,
		name: str,
		level: int
	):
		self._name = name
		self._level = level
		# For forging cards
		self.artisan: bool = False
		self.boosts_artisan: bool = False

	@property
	def name(self) -> str:
		return self._name

	@property
	def level(self) -> int:
		return self._level

	def score(self, score: Score, recipe: str, prev_cards: list[Card]) -> int:
		# Takes the current mutable score and adds the current card's value to it
		# taking into account the recipe powers and previous cards
		pass

	def __str__(self) -> str:
		return f'{self.name} (lvl {self.level})'

	def __eq__(self, o: object) -> bool:
		# Cards are the same if their subclass is the same
		# since they can't be different levels in the same deck
		return isinstance(o, self.__class__)

#################
# Kitchen Cards #
#################
class Cut(Card):
	def __init__(self, level: int):
		super().__init__('Cut', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		# Determine random ranges based on level
		values = {
			1: (1, 1),
			2: (2, 2),
			3: (3, 3),
			4: (4, 8),
			5: (8, 12),
			6: (10, 15),
			7: (1, 1), # TODO
			8: (13, 18),
			9: (13, 18),
		}
		low, high = values.get(self.level, (0, 0))
		# Salted Raisin power cut always yields max points
		val = high if recipe == 'Salted Raisin' else randint(low, high)
		# Roasted Corn power cut always affects lowest color
		score.add_lowest(val) if recipe == 'Roasted Corn' else score.add_random(val)
		for prev in reversed(prev_cards):
			if prev.name != 'Cut':
				break
			val = high if recipe == 'Salted Raisin' else randint(low, high)
			score.add_lowest(val) if recipe == 'Roasted Corn' else score.add_random(val)
			# At lvl 9+ cut triggers twice per previous card in cut streak
			if self.level >= 9:
				val = high if recipe == 'Salted Raisin' else randint(low, high)
				score.add_lowest(val) if recipe == 'Roasted Corn' else score.add_random(val)

class HeatControl(Card):
	def __init__(self, level: int):
		super().__init__('Heat Control', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		limit = 7 # Limit of how many times it's allowed to retrigger
		# Determine base value
		# TODO: Levels 1-6, 9+
		values = {
			1: 3,
			2: 4,
			3: 6,
			4: 8,
			5: 10,
			6: 12,
			7: 15,
			8: 18,
		}
		val = values.get(self.level, 0)
		score.add_random(val)
		# Slow cook triggers when heat control triggers or retriggers at lvls 4 and below
		# at lvl 5+ slow cook triggers when heat control flips
		slow_cook_triggers = 0
		slow_cook_level = 0
		if len([p for p in prev_cards if p.name == 'Slow Cook']):
			slow_cook_triggers += 1 # For the flip
			slow_cook_level = [p for p in prev_cards if p.name == 'Slow Cook'][0].level
		# Ferment causes heat control to trigger at least 2 extra times
		ferment_triggers = len([p for p in prev_cards if isinstance(p, Ferment)])
		ferment_level = [p for p in prev_cards if isinstance(p, Ferment)][0].level if ferment_triggers else 0
		for _ in range(ferment_triggers * ferment_level):
			score.add_random(val)
			# Only triggers slow cook on flip at lvl 5+
			if slow_cook_level < 5:
				slow_cook_triggers += 1
			# limit -= 1 #? Not sure if this counts
		while rand() >= 0.5 and limit > 0: # Heat control has a 50% chance to continually retrigger
			score.add_random(val)
			# Only triggers slow cook on flip at lvl 5+
			if slow_cook_level < 5:
				slow_cook_triggers += 1
			limit -= 1
		for sc in [p for p in prev_cards if p.name == 'Slow Cook']:
			for _ in range(slow_cook_triggers):
				sc.score(score, '', []) # Recipe and prev cards don't affect slow cook (yet)
		

class Season(Card):
	def __init__(self, level: int):
		super().__init__('Season', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		score.double_random()

class SlowCook(Card):
	def __init__(self, level: int):
		super().__init__('Slow Cook', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		values = {
			1: 4,
			2: 2,
			3: 4,
			4: 5,
			5: 6,
		}
		val = values.get(self.level, 0)
		# At level 2+ value affects all colors
		if self.level >= 2:
			score.add_all(val)
		else:
			score.add_random(val)

class Ferment(Card):
	def __init__(self, level: int):
		super().__init__('Ferment', level)
	
	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		# Ferment doesn't score at all
		pass

class Bake(Card):
	def __init__(self, level: int):
		super().__init__('Bake', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		# Max level is 2
		score.add_random(5) if self.level == 1 else score.add_random(10)
		# Forces point redistribution at the end
		score.redist = True

class ExactCook(Card):
	def __init__(self, level: int):
		super().__init__('Exact Cook', level)

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		# prev_cards is special here as it's all the cards
		values = {
			1: 3,
			2: 2,
			1: 1,
		}
		needed = values.get(self.level, 3)
		prev = None
		in_a_row = 0
		# If the needed amount of cards appeared in a row, double at the end
		for card in prev_cards:
			if card != prev:
				in_a_row = 0
			else:
				in_a_row += 1
				if in_a_row >= needed:
					score.post_double = True
					break
			prev = card

###############
# Forge Cards #
###############
class Forge(Card):
	def __init__(self, level: int):
		super().__init__('Forge', level)
		self.artisan = True

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		values = {
			1:1,
			2:2,
			3:3,
			4:5,
			5:10,
			6:15,
		}
		val = values.get(self.level, 0)
		# Apply stack bonuses
		# Heat Up
		val += score.stack.heat_up_bonus
		# Charge
		if score.stack.charge_charges:
			score.add_all(val)
			score.stack.charge_charges -= 1
		else:
			score.add_random(val)
		# Multi-forge
		while score.stack.multi_forge_amt > 0:
			if score.stack.charge_charges:
				score.add_all(val)
				score.stack.charge_charges -= 1
			else:
				score.add_random(val)
			score.stack.multi_forge_amt -= 1

class Charge(Card):
	def __init__(self, level: int):
		super().__init__('Charge', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		values = {
			1: 0,
			2: 0,
			3: 0,
			4: 5,
		}
		charges = {
			1: 1,
			2: 3,
			3: 99, # Every deck is less than 10 cards, so 99 represents inf
			4: 99,
		}
		# At lvl 4+ this gives points
		val = values.get(self.level, 0)
		score.add_random(val)
		# Set the stack charge amount
		charge = charges.get(self.level, 0)
		score.stack.charge_charges = charge

class Sharpening(Card):
	def __init__(self, level: int):
		super().__init__('Sharpening', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		values = {
			1: 10,
			2: 12,
		}
		val = values.get(self.level, 0)
		# prev_cards is special here as it receives all future cards
		# Add val for each unseen card in the cycle
		for _ in prev_cards:
			score.add_random(val)

class MultiForge(Card):
	def __init__(self, level: int):
		super().__init__('Multi-Forge', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		charges = {
			1: 2,
			2: 3,
		}
		# Set the multi forge charges 
		# this stacks, tested with copper carver, 2 multi forge and a forge, got 41x11 which is 5 total triggers
		score.stack.multi_forge_amt += charges.get(self.level, 0)

class HeatUp(Card):
	def __init__(self, level: int):
		super().__init__('Heat Up', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		val = {
			1: 3,
			2: 6,
			3: 10,
			4: 12,
			5: 14,
		}.get(self.level, 0)
		# Set the stack bonus
		#? I believe this is always permanent
		score.stack.heat_up_bonus = val

class Reforge(Card):
	def __init__(self, level: int):
		super().__init__('Reforge', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		val = {
			1: 5,
			2: 10,
			3: 15
		}.get(self.level, 0)
		score.add_all(val)

class Soulbind(Card):
	def __init__(self, level: int):
		super().__init__('Soulbind', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		val = {
			1: 0,
			2: 5,
		}.get(self.level, 0)
		score.add_random(val)
		# Soulbind retriggers enhancing cards
		for card in prev_cards:
			if isinstance(card, (Charge, HeatUp, MultiForge)):
				card.score(score, recipe, prev_cards)

class ForgeExpert(Card):
	def __init__(self, level: int):
		super().__init__('Forge Expert', level)
		self.artisan = True

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		val = {
			1: 3,
			2: 4,
			3: 4,
			4: 5,
			5: 5,
			6: 10,
		}.get(self.level, 0)
		bonus = {
			1: 3,
			2: 3,
			3: 4,
			4: 5,
			5: 5,
			6: 5,
		}.get(self.level, 0)
		# Apply stack bonuses
		# Heat up
		val += score.stack.heat_up_bonus
		# Score once then multi forge
		# Charge
		if score.stack.charge_charges:
			score.add_all(val + (bonus * score.stack.forge_expert_mult))
			score.stack.charge_charges -= 1
		else:
			score.add_random(val + (bonus * score.stack.forge_expert_mult))
		score.stack.forge_expert_mult += 1
		# Multi-forge is additional after the main reveal
		while score.stack.multi_forge_amt > 0:
			if score.stack.charge_charges:
				score.add_all(val + (bonus * score.stack.forge_expert_mult))
				score.stack.charge_charges -= 1
			else:
				score.add_random(val + (bonus * score.stack.forge_expert_mult))
			score.stack.multi_forge_amt -= 1
			score.stack.forge_expert_mult += 1

class Pyroburst(Card):
	def __init__(self, level: int):
		super().__init__('Pyroburst', level)
		self.artisan = True

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		val = {
			1: 12,
			2: 18,
		}.get(self.level, 0)
		# Apply bonuses
		double_trigger = 0 # If this hits 2, this card triggers 2 additional times
		# Heat up
		val += score.stack.heat_up_bonus
		double_trigger += 1 if score.stack.heat_up_bonus else 0
		# Charge
		if score.stack.charge_charges:
			double_trigger += 1
			score.add_all(val)
			score.stack.charge_charges -= 1
		else:
			score.add_random(val)
		# Multi-forge
		double_trigger += 1 if score.stack.multi_forge_amt else 0
		while score.stack.multi_forge_amt > 0:
			if score.stack.charge_charges:
				score.add_all(val)
				score.stack.charge_charges -= 1
			else:
				score.add_random(val)
			score.stack.multi_forge_amt -= 1
		if double_trigger >= 2:
			for _ in range(2):
				if score.stack.charge_charges:
					score.add_all(val)
					score.stack.charge_charges -= 1
				else:
					score.add_random(val)

class Ignite(Card):
	def __init__(self, level: int):
		super().__init__('Ignite', level)
		self.artisan = False

	def score(self, score: Score, recipe: str, prev_cards: list[Card]):
		score.double_random()

#################
# Alchemy Cards #
#################