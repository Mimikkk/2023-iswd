from random import choice

from .extended_player import ExtendedPlayer

class DanielosPlayer(ExtendedPlayer):
  def __init__(self, name: str):
    super().__init__(name)
    self.suspected = []
    self.declared = None
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
    if declared and declared not in self.pile: self.pile.append(declared)
    valid = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards

    if not valid: return "draw"
    if len(self.cards) == 1: return valid[0], valid[0]

    card = declaration = choice(valid)
    self.pile.append(card)
    return card, declaration

  def should_accuse(self, declared):
    if declared in self.suspected or declared in self.pile:
      self.declared = declared
      return True
    self.suspected.append(declared)
    return False
