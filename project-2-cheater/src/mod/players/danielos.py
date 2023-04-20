from copy import copy
from random import choice, random, shuffle

import numpy as np

from .extended_player import ExtendedPlayer

Card = tuple[int, int]


def increase_by(card: Card, declarable: list[Card], value: int):
  if value == 0: return card, card

  declarable = [c for c in declarable if c[0] == card[0] + value]
  if not declarable: return increase_by(card, declarable, value - 1)
  return card, choice(declarable)


class DanielosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]
    declarable = [card for card in self.Cards if self.is_valid(card, declared)]
    if not valid: return "draw"

    card = declaration = min(self.cards, key=self.by_rank)

    if declared and not self.is_valid(card, declared):
      declaration = (min(declared[0] + 1, 14), declaration[1])
      declaration = self.pick(declaration)

    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards

  def pick(self, declaration):
    for card in self.cards:
      if card[0] in (declaration[0], declaration[0] + 1): return card
    return declaration
