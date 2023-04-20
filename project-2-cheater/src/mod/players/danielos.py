from copy import copy
from random import choice, random, shuffle

import numpy as np

from .extended_player import ExtendedPlayer

Card = tuple[int, int]


class DanielosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name):
    super().__init__(name)

  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]
    if len(self.cards) == 1 and len(valid) == 1: return valid[0], valid[0]
    if not valid: return "draw"

    card = declaration = min(self.cards, key=self.by_rank)

    if declared and not self.is_valid(card, declared):
      minimum = min(declared[0] + 1, 14)
      declaration = (minimum, card[1])

      viable = [card for card in self.cards if card[0] in (minimum, minimum + 1)]
      declaration = choice(viable or [declaration])

    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards
