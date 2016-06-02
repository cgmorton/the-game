import argparse
from collections import defaultdict
# import itertools
import logging
import math
# import os
import random

import matplotlib.pyplot as plt
import numpy as np

import players


class Deck():
    def __init__(self, min=2, max=99):
        self.deck = list(xrange(min, max + 1, 1))
        self.empty = False
        random.shuffle(self.deck)

    def __str__(self):
        return ' '.join(map(str, self.deck))

    def get_cards(self, n=1):
        for i in xrange(n):
            if self.deck:
                yield self.deck.pop()
            else:
                self.empty = True
                break


def main(n_players=3, hand_size=6):
    """"""
    logging.info('THE GAME')
    # At some point error checking to ensure n_players is 3 <= n <= 7

    # Initialize the piles
    logging.debug('\nInitializing Game')
    pile_dict = {
        'up_a': [1],
        'up_b': [1],
        'down_a': [100],
        'down_b': [100]
    }
    for pile, cards in pile_dict.items():
        logging.debug('  Pile {}: {}'.format(pile, cards))

    # Initialize the deck
    deck = Deck()
    logging.debug('  Deck: {} ({})\n'.format(deck, len(deck.deck)))

    # Initialize the player hands
    player_dict = defaultdict(list)
    for player in range(n_players):
        # Is there a better way to pop a slice/range from a list?
        player_dict[player] = list(deck.get_cards(hand_size))
        # Get cards one at a time
        # for card in range(hand_size):
        #     player_dict[player].append(deck.get_card())
        logging.debug('  Player {}: {}'.format(
            player + 1, player_dict[player]))
    logging.debug('\n  Deck: {} ({})'.format(deck, len(deck.deck)))

    # while not deck.empty:
    #     cards = list(deck.get_cards(7))
    #     print(cards)

    # Start play
    logging.debug('\nStarting Game')
    valid_move_flag = True
    turn = 0
    while valid_move_flag:
        logging.debug('\nTurn: {}'.format(turn + 1))

        # Loop through each player
        for player in range(n_players):
            logging.debug('Player: {}'.format(player + 1))

            # Skip player if hand is empty
            if len(player_dict[player]) == 0:
                continue

            for pile, cards in pile_dict.items():
                logging.debug('  Pile {}: {}'.format(
                    pile, ' '.join(map(str, cards))))

            # Play smartly
            valid_move_flag = players.min_diff_mod_player(
                player_dict[player], pile_dict,
                min_cards=2, max_cards=2, play_tens=True)

            # # Play the card with the minimum difference from either pile
            # valid_move_flag = players.min_diff_player(
            #     player_dict[player], pile_dict,
            #     min_cards=2, max_cards=2)

            # # Play cards randomly on up piles then on down piles
            # valid_move_flag = players.random_updown_player(
            #     player_dict[player], pile_dict,
            #     min_cards=2, max_cards=2)

            # # Play 2 cards randomly
            # valid_move_flag = players.random_player(
            #     player_dict[player], pile_dict,
            #     min_cards=2, max_cards=2)

            # Game is over if there are no valid moves to play
            if not valid_move_flag:
                break

            # Get new cards to replace used ones
            cards = list(deck.get_cards(
                hand_size - len(player_dict[player])))
            player_dict[player].extend(cards)
            logging.debug('  Get cards: {}'.format(cards))

            # At some point add logic to indicate not playing on a pile

        turn += 1

    logging.info('\nGame Over')

    # Print out the final game state
    # logging.debug('  Deck: {} ({})'.format(deck, len(deck.deck)))
    for pile, cards in pile_dict.items():
        logging.debug('  Pile {}: {}'.format(
            pile, ' '.join(map(str, cards))))
    # for player, cards in player_dict.items():
    #     logging.debug('  Hand {}: {}'.format(
    #         player, ' '.join(map(str, cards))))
    cards = len(deck.deck) + sum([len(c) for c in player_dict.values()])
    logging.info('{} unplayed cards\n'.format(cards))
    return cards


def arg_parse():
    """"""
    parser = argparse.ArgumentParser(
        description='The Game',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-mc', '--montecarlo', default=1, metavar='N', type=int,
        help='Play game N times')
    parser.add_argument(
        '-d', '--debug', default=logging.INFO, const=logging.DEBUG,
        help='Debug level logging', action="store_const", dest="loglevel")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = arg_parse()

    if args.montecarlo > 1:
        logging.basicConfig(level=logging.WARNING, format='%(message)s')
        counts = [main() for i in xrange(args.montecarlo)]
        logging.warning('Median: {}'.format(np.median(counts)))

        # plt.figure()
        fig, ax = plt.subplots(ncols=2, figsize=(8, 4))
        h_min = math.floor(min(counts)) - 0.5
        h_max = math.ceil(max(counts)) + 0.5
        n, bins, patches = ax[0].hist(
            counts, bins=h_max-h_min, range=(h_min, h_max),
            fc='g', alpha=0.75)
        ax[1] = plt.boxplot(counts, notch=True)
        # plt.plot(counts, '.')
        plt.show()
    else:
        logging.basicConfig(level=args.loglevel, format='%(message)s')
        main()
