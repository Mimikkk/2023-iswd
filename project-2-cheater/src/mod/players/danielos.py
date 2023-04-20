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

  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = set()
    self.pile = []

  def on_right_accusation(self, revealed, taken_count):
    self.on_draw()

  def on_wrong_accusation(self, revealed, taken_count):
    self.suspected.remove(revealed)
    self.on_draw()

  def on_caught(self, taken_count):
    self.on_draw()

  def on_honest(self, taken_count):
    self.on_draw()

  def on_opponent_draw(self):
    self.on_draw()

  def on_start(self):
    for card in self.cards: self.suspected.add(card)

  def on_take(self, taken):
    for card in taken: self.suspected.add(card)

  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]
    if not valid: return "draw"

    card = declaration = min(self.cards, key=self.by_rank)

    if declared:
      minimum = declared[0]
      if card[0] < minimum:
        declaration = (min(minimum + 1, 14), declaration[1])
        declaration = self.pick(declaration)
    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards

  def pick(self, declaration):
    for card in self.cards:
      if card[0] in (declaration[0], declaration[0] + 1): return card
    return declaration

  def present_state(self, declared):
    print(declared)
    print(sorted(self.cards))
    print(sorted(self.suspected))
    print(self.pile)
    print(self.state.pile)
    print(sorted(self.state.players[0].cards))
    print(sorted(self.state.players[1].cards))
    print()

  def on_draw(self):
    for _ in range(3):
      if self.pile and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)
