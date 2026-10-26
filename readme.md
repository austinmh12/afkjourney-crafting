# AFK Journey Homestead Crafting Calculator
This tool calculates the score for all combinations and permutations of each deck based on the recipe and the current facility level and card levels.

# WIP
This is currently a work in progress as it's not possible to view old levels of cards in the game and it's also very unoptimized. It's missing all of alchemy at the moment and at some point it will be a web page on github pages but tbd.

## TODO
- Common
  - [ ] Convert to flask app
  - [ ] Optimize deck calculations (Pick Hammer as 54264 unique 6 card decks, of which each has 720 permutations, that's 39,070,080 calculations just for that recipe...)
- Kitchen
  - [ ] Add remaining recipes
  - [ ] Implement any additional recipe powers
  - [ ] Implement Kitchen level selection
    - [ ] Find and implement kitchen level card limits
	- [ ] Find and implement kitchen level card level limits
- Forge
  - [ ] Add remaining recipes
  - [ ] Implement any additional recipe powers
  - [ ] Implement Forge level selection
    - [ ] Find and implement forge level card limits
	- [ ] Find and implement forge level card level limits
- Alchemy
  - [ ] Add all cards
  - [ ] Add all recipes
  - [ ] Implement all recipe powers
  - [ ] Implement alchemy level selection
    - [ ] Find and implement alchemy level card limits
	- [ ] Find and implement alchemy level card level limits