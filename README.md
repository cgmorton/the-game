
# The Game

A Python implementation of the card game [The Game](http://idwgames.com/games/the-game/).

The goal of the project was to try to design "players" that could be simulated for thousands of rounds to see if there was an optimum way to play.

I originally wanted to use Objected Oriented Programming, but that will take a bit more work.

## Players

Currently, only the following simple players have been implemented.

### Random

Randomly plays 2 cards on any pile

### Random Up/Down

First tries playing lowest cards on the up piles until they are full, then plays highest card on the down piles.
Only plays 2 cards on each turn.

### Minimum Difference

Play card with the smallest difference to the pile cards.
Only plays 2 cards on each turn.

### Minimum Difference mod 1

Play card with the smallest difference to one of the pile cards.
Play 10 cards when possible

## Todo

Implement a way for players to indicate which piles should not be played on.
Implement a player that will continue playing cards if the minimum difference is small enough.
Implement more advanced players!

## Required Modules

+ NumPy
+ Matplotlib (for viewing simulation results)
