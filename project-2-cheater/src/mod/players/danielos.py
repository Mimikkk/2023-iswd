from random import choice

from .extended_player import ExtendedPlayer


class DanielosPlayer(ExtendedPlayer):
  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = []
    self.declared = None
    self.pile = []

  def on_right_accusation(self, revealed, taken_count):
    if revealed in self.suspected: self.suspected.remove(revealed)
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
    self.suspected.extend(self.cards)

  def on_take(self, taken):
    self.suspected.extend(taken)

  def declare(self, declared):
    if declared and declared not in self.pile:
      self.pile.append(declared)
      self.suspected.append(declared)
    valid = [card for card in self.cards if self.is_valid(card, declared)]

    if len(self.cards) == 1 and len(valid) == 1: return valid[0], valid[0]
    if not valid: return "draw"

    card = declaration = choice(valid)
    self.pile.append(card)
    return card, declaration

  def should_accuse(self, declared):
    if declared:
      self.pile.append(declared)
    if declared not in self.pile:
      self.suspected.append(declared)

    return declared in self.suspected

  def on_draw(self):
    for _ in range(3):
      if len(self.pile) > 0 and (card := self.pile.pop()) in self.suspected: self.suspected.remove(card)
