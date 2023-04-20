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

def play_valid_as_declarable(valid, declarable):

  declarable.sort(key=lambda x: x[0])
  valid.sort(key=lambda x: x[0])

  card = valid[0]
  if valid[0][0] < declarable[0][0]:
    return card, declarable[0]
  else:
    return card, card

class LiarAlexosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = []
    self.pile = []

  def on_right_accusation(self, revealed, taken_count):
    if revealed in self.suspected:
      self.suspected.remove(revealed)
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_wrong_accusation(self, revealed, taken_count):
    self.suspected.remove(revealed)

  def on_caught(self, taken_count: int):
    for _ in range(taken_count):
      if len(self.pile) > 0: self.pile.pop()

  def on_honest(self, taken_count: int):
    for _ in range(taken_count):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)

  def on_start(self):
    self.suspected.extend(self.cards)

  def on_take(self, taken):
    self.suspected.extend(taken)

  def declare(self, declared):
    # valid = those i can place without lying
    valid = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards
    declarable = declared and [card for card in self.Cards if card[0] >= declared[0]] or self.Cards
    valid = list(valid) if type(valid) != list else valid
    declarable = list(declarable) if type(declarable) != list else declarable

    if not valid: return "draw"

    card_min_valid, card_max_valid = min(valid, key=lambda x: x[0]), max(valid, key=lambda x: x[0])

    ### the incr_val could be dynamic based on the number of cards left in hand or in the pile
    # return increase_with_color(card_min, declarable_not_in_pile, incr_val=2)
    # return card_min_valid, card_min_valid

    ### other option: play it safe in endgame, but this won't work well when
    ### we draw on not declarable instead on 'not valid' (maybe this can be patched somehow)
    if len(self.cards) <= 3:
      return card_max_valid, card_max_valid
    else:
      return increase_with_color(card_min_valid, declarable, 2)
      # return play_valid_as_declarable(valid, declarable)
  def should_accuse(self, declared):
    if declared in self.cards:
      return True
