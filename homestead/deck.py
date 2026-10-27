import itertools
from random import sample

from .score import Score
from .card import *

class ScoreResults:
	def __init__(self):
		self.scores: list[Score] = list()

	@property
	def minimum(self) -> Score:
		return min(self.scores, default=0)

	@property
	def maximum(self) -> Score:
		return max(self.scores, default=0)

	@property
	def average(self) -> int:
		if self.scores:
			return sum(s.total for s in self.scores) // len(self.scores)
		return 0

class Deck:
	def __init__(self, cards: list[Card]):
		self.cards = cards

	def sample(self, recipe: str, samples: int = 15) -> int:
		# Score X random permutations for their average score
		results = ScoreResults()
		perms = [list(x) for x in itertools.permutations(self.cards)]
		deck_samples = sample(perms, samples)
		for deck_sample in deck_samples:
			score = Score()
			for i, card in enumerate(deck_sample):
				prev_cards = deck_sample[:i]
				card.score(score, recipe, prev_cards)
			results.scores.append(score)
		return results.average

	def score(self, recipe: str) -> ScoreResults:
		# Calculates the minimum, maximum, and average score for each permutation
		# of the deck.
		results = ScoreResults()

		# All permutations of this deck
		perms = (list(x) for x in itertools.permutations(self.cards))
		# print(f'Permutations of deck: {len(perms)}')

		for deck_perm in perms:
			order = deck_perm[:] # Original order, needed for Exact Cook
			score = Score()
			for i, card in enumerate(order):
				prev_cards = deck_perm[:i]
				if isinstance(card, ExactCook):
					prev_cards = order[:]
				elif isinstance(card, Sharpening):
					prev_cards = order[i:]
					prev_cards.pop(0) # Current card doesn't count
				card.score(score, recipe, prev_cards)
			results.scores.append(score)
		return results

	def __hash__(self) -> int:
		return hash(''.join([str(c) for c in sorted(self.cards)]))