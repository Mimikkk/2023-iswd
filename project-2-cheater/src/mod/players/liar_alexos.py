from random import choice, random
from .extended_player import ExtendedPlayer


def increase_naive(card):
  # declare a card with value 1 higher
  incr_val = (1, 0) if card[0] < 14 else (0, 0)
  return card, tuple(map(sum, zip(card, incr_val)))

def increase_with_color(card, declarable, incr_val):
  higher_cards = [card for card in declarable if card[0] == card[0] + incr_val]

  if not higher_cards:
    return card, card
  else:
    return card, choice(higher_cards)

class LiarAlexosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def declare(self, declared):
    ## valid are cards that i can play from my hand truthfully
    valid = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards
    ## declarable are cards that are valid and also those that i can falsly declare
    ## but it does not take already played cards into account TODO
    declarable = declared and [card for card in self.cards if card[0] >= declared[0]] or self.Cards

    if not declarable: return "draw"

    card_min = min(self.cards, key=lambda x: x[0])
    card_min_valid, card_max_valid = min(valid, key=lambda x: x[0]), max(valid, key=lambda x: x[0])

    ### the incr_val could be dynamic based on the number of cards left in hand or in the pile
    return increase_with_color(card_min, declarable, incr_val=2)

    ### other option: play it safe in endgame, but this won't work well when
    ### we draw on not declarable instead on 'not valid' (maybe this can be patched somehow)
    # if len(self.cards) <= 3 or len(declarable) <= 12:
    #   return card_min_valid, card_min_valid
    # else:
    #   return increase_with_color(card_min, declarable, 2)


  def should_accuse(self, declared): return False
