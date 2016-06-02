import itertools
import logging
import random


def random_player(hand, pile_dict, min_cards=2, max_cards=6):
    """Randomly play a card on a pile

    Args:
        hand (list):
        pile_dict (dict):
        min_cards (int):
        max_cards (int):

    Return
        boolean: return True if there is a valid move
    """
    logging.debug('  Hand: {}'.format(' '.join(map(str, hand))))

    # The player hand is already random, so only shuffle the pile keys
    piles = sorted(pile_dict.keys(), key=lambda *args: random.random())
    # piles = sorted(pile_dict.keys(), key=os.urandom)

    # Iterate through all possible pairs of cards and piles
    cards_played = []
    for card, pile in itertools.product(hand, piles):
        if card in cards_played:
            # Skip card if it was already played
            continue
        elif (('up' in pile and card > pile_dict[pile][-1]) or
              ('down' in pile and card < pile_dict[pile][-1])):
            logging.debug('  Play: {} {}'.format(card, pile))
            pile_dict[pile].append(card)
            hand.remove(card)
            cards_played.append(card)

            # Player can't play more than the max number of cards
            if len(cards_played) >= max_cards:
                break
        else:
            continue

    # Game is over if the player can't play the minimum number of cards
    if len(cards_played) < min_cards:
        return False
    else:
        return True


def random_updown_player(hand, pile_dict, min_cards=2, max_cards=6):
    """First try playing sorted hand on the up piles,
        then play reverse sorted hand on the down piles

    Args:
        hand (list):
        pile_dict (dict):
        min_cards (int):
        max_cards (int):

    Return
        boolean: return True if there is a valid move
    """
    cards_played = []
    logging.debug('  Hand: {}'.format(' '.join(map(str, hand))))

    up_piles = sorted(
        [k for k in pile_dict.keys() if 'up' in k],
        key=lambda *args: random.random())
    down_piles = sorted(
        [k for k in pile_dict.keys() if 'down' in k],
        key=lambda *args: random.random())

    # Try playing sorted hand on the up piles
    sorted_hand = sorted(hand[:])
    logging.debug('  Hand: {}'.format(' '.join(map(str, sorted_hand))))
    for card, pile in itertools.product(sorted_hand, up_piles):
        if len(cards_played) >= max_cards:
            break
        elif card in cards_played:
            # Skip card if it was already played
            continue
        elif card > pile_dict[pile][-1]:
            logging.debug('  Play: {} {}'.format(card, pile))
            pile_dict[pile].append(card)
            hand.remove(card)
            cards_played.append(card)

    # Then try playing reverse sorted hand on the down piles
    sorted_hand = sorted(hand[:], reverse=True)
    logging.debug('  Hand: {}'.format(' '.join(map(str, sorted_hand))))
    for card, pile in itertools.product(hand, down_piles):
        # Player can't play more than the max number of cards
        if len(cards_played) >= max_cards:
            break
        elif card in cards_played:
            # Skip card if it was already played
            continue
        elif card < pile_dict[pile][-1]:
            logging.debug('  Play: {} {}'.format(card, pile))
            pile_dict[pile].append(card)
            hand.remove(card)
            cards_played.append(card)

    # Game is over if the player can't play the minimum number of cards
    if len(cards_played) < min_cards:
        return False
    else:
        return True


def min_diff_player(hand, pile_dict, min_cards=2, max_cards=6):
    """Play cards closest to the pile cards

    Args:
        hand (list):
        pile_dict (dict):
        min_cards (int):
        max_cards (int):

    Return
        boolean: return True if there is a valid move
    """
    cards_played = []
    logging.debug('  Hand: {}'.format(' '.join(map(str, hand))))

    while len(cards_played) < max_cards:
        play_list = []
        # Compute difference between piles and cards in hand
        # Put diff as first value in nested list to sort on
        for p_name, p_cards in pile_dict.items():
            if 'up' in p_name:
                diff = [
                    [h_card - p_cards[-1], p_name, h_card]
                    for h_card in hand if h_card > p_cards[-1]]
            elif 'down' in p_name:
                diff = [
                    [p_cards[-1] - h_card, p_name, h_card]
                    for h_card in hand if h_card < p_cards[-1]]
            play_list.extend(diff)

        # Place the card with the lowest difference on a pile
        if play_list:
            diff, pile, card = sorted(play_list)[0]
            logging.debug('  Play: {} {}'.format(card, pile))
            pile_dict[pile].append(card)
            hand.remove(card)
            cards_played.append(card)
        else:
            break

    # Game is over if the player can't play the minimum number of cards
    if len(cards_played) < min_cards:
        return False
    else:
        return True


def min_diff_mod_player(hand, pile_dict, min_cards=2, max_cards=6,
                        play_tens=True):
    """Play cards closest to the pile cards

    Args:
        hand (list):
        pile_dict (dict):
        min_cards (int):
        max_cards (int):
        play_tens (bool): Play -10s when possible

    Return
        boolean: return True if there is a valid move
    """
    cards_played = []
    logging.debug('  Hand: {}'.format(' '.join(map(str, hand))))

    # while len(cards_played) < max_cards:
    while len(cards_played) < max_cards:
        play_list = []
        # Compute difference between piles and cards in hand
        # Put diff as first value in nested list to sort on
        for p_name, p_cards in pile_dict.items():
            if 'up' in p_name:
                diff = [
                    [h_card - p_cards[-1], p_name, h_card]
                    for h_card in hand
                    if h_card > p_cards[-1] or ((p_cards[-1] - h_card) == 10)]
            elif 'down' in p_name:
                diff = [
                    [p_cards[-1] - h_card, p_name, h_card]
                    for h_card in hand
                    if h_card < p_cards[-1] or ((p_cards[-1] - h_card) == 10)]
            play_list.extend(diff)

        # Place the card with the lowest difference on a pile
        if play_list:
            tens_list = [plays for plays in play_list if plays[0] == -10]
            if play_tens and tens_list:
                diff, pile, card = tens_list[0]
                logging.info('  Ten: {} {}'.format(card, pile))
            else:
                diff, pile, card = sorted(play_list)[0]
                logging.debug('  Play: {} {}'.format(card, pile))
            pile_dict[pile].append(card)
            hand.remove(card)
            cards_played.append(card)
        else:
            break

    # Game is over if the player can't play the minimum number of cards
    if len(cards_played) < min_cards:
        return False
    else:
        return True
