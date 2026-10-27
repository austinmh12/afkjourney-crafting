from typing import Iterator
import itertools
from homestead import *
from tqdm import tqdm

RECIPES = [
	# Recipe('Roasted Corn', 'Kitchen', 5, 2030, 5190, 8250, 14300),
	# Recipe('Cool Candied Skewer', 'Kitchen', 6, 5570, 12800, 20400, 30000),
	# Recipe('Healthy Candied Skewer', 'Kitchen', 6, 2400, 6560, 11200, 21600),
	# Recipe('Popcorn', 'Kitchen', 5, 2080, 5290, 8640, 15200),
	# Recipe('Earthy Flatbread', 'Kitchen', 6, 3950, 9630, 15100, 26500),
	Recipe('Copper Carver', 'Forge', 3, 6, 8),
	Recipe('Copper Mask', 'Forge', 4, 15, 30),
	Recipe('Fine Carver', 'Forge', 5, 32, 100),
	Recipe('Pick Hammer', 'Forge', 6, 1110, 4640, 20000, 91500),
	Recipe('Protective Pick Hammer', 'Forge', 6, 1650, 9894, 33666, 129234), # TODO: Artisan cards all need to do the pyroburst check for this recipe
	Recipe('Herb Tray', 'Forge', 7, 234, 11100, 30100, 97000),
	Recipe('Mithril Mortar', 'Forge', 5, 450, 6570, 16800, 37200),
	Recipe('Thermo Chest', 'Forge', 6, 1250, 4490, 24000, 51000),
	Recipe('Iron Mixing Dish', 'Forge', 7, 1490, 11800, 26700, 49000)
]

# TODO: Add modes for selecting highest minimum for highst chance at stars, etc.
def main():
	results: dict[Recipe, tuple[Deck, ScoreResults]] = dict()
	# Generate all lengths of decks since theres no need for duplicating that
	for recipe in RECIPES:
		decks = generate_decks(recipe.location, recipe.cards)
		deck_results: list[tuple[Deck, ScoreResults]] = []
		print(f'{recipe.name} has {len(decks)} unique decks')
		deck_sample_average = 0
		for deck in tqdm(decks, desc=recipe.name):
			smp = deck.sample()
			if smp < deck_sample_average:
				continue
			deck_sample_average = smp
			deck_results.append((deck, deck.score(recipe.name)))
		# Store the deck with the highest average
		results[recipe] = max(deck_results, key=lambda s: s[1].average)
	for recipe, (deck, result) in results.items():
		print(recipe.name)
		print(f'    Min: {result.minimum} {"*" * recipe.star(result.minimum.total)}')
		print(f'    Avg: {result.average} {"*" * recipe.star(result.average)}')
		print(f'    Max: {result.maximum} {"*" * recipe.star(result.maximum.total)}')
		print(f'    Cards for Average:')
		print(f'      {", ".join([str(c) for c in deck.cards])}')

# Hardcoded limits and levels for my current levels for now
KITCHEN_LIMITS = {
	HeatControl: 4,
	Cut: 4,
	Season: 1,
	SlowCook: 2,
	Ferment: 2,
	Bake: 1,
	ExactCook: 1,
}
KITCHEN_LEVELS = {
	HeatControl: 7,
	Cut: 8,
	Season: 1,
	SlowCook: 4,
	Ferment: 2,
	Bake: 2,
	ExactCook: 1,
}
FORGE_LIMITS = {
	Forge: 3,
	Charge: 2,
	Sharpening: 1,
	MultiForge: 2,
	HeatUp: 2,
	Reforge: 2,
	Soulbind: 2,
	ForgeExpert: 4,
	Pyroburst: 2,
	Ignite: 1,
}
FORGE_LEVELS = {
	Forge: 5,
	Charge: 3,
	Sharpening: 1,
	MultiForge: 1,
	HeatUp: 4,
	Reforge: 2,
	Soulbind: 1,
	ForgeExpert: 5,
	Pyroburst: 1,
	Ignite: 1,
}
ALCHEMY_LIMITS = {
	
}
ALCHEMY_LEVELS = {
	
}

def generate_decks(location: str, length: int) -> Iterator[Deck]:
	decks = []
	if location == 'Forge':
		LIMITS = FORGE_LIMITS
		LEVELS = FORGE_LEVELS
	elif location == 'Alchemy':
		LIMITS = ALCHEMY_LIMITS
		LEVELS = ALCHEMY_LEVELS
	else:
		LIMITS = KITCHEN_LIMITS
		LEVELS = KITCHEN_LEVELS
	# Hardcoded limits fr kitchen lvl 15
	allowed_cards = []
	for card, limit in LIMITS.items():
		allowed_cards.extend([card(LEVELS.get(card))] * limit)
	for combo in itertools.combinations(allowed_cards, length):
		# yield Deck(list(combo))
		decks.append(Deck(list(combo)))
	return decks

if __name__ == "__main__":
	main()