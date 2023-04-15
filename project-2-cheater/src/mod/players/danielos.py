from random import choice

from .extended_player import ExtendedPlayer

class DanielosPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def __init__(self, name: str):
    super().__init__(name)
    self.suspicious = set()

  def on_start(self):
    self.suspicious.update(self.cards)

  def on_take(self, taken):
    self.suspicious.update(taken)

  def declare(self, declared):
    valid_held_cards = declared and [card for card in self.cards if card[0] >= declared[0]] or self.cards

    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    return card, declaration

  def should_accuse(self, declared):
    if declared in self.suspicious: return True
    return False
