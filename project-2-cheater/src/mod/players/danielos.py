from random import choice

from .extended_player import ExtendedPlayer

Card = tuple[int, int]
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

  def on_take(self, taken: list[Card]):
    self.suspicious.update(taken)

  def on_opponent_draw(self): ...
  def on_wrong_accusation(self, revealed: Card, taken_count: int): ...
  def on_right_accusation(self, revealed: Card, taken_count: int): ...
  def on_caught(self, taken_count: int): ...
  def on_honest(self, taken_count: int): ...

  def declare(self, declared: Card | None):
    valid_held_cards = declared and [card for card in self.cards if card[0] > declared[0]] or self.cards

    if not valid_held_cards: return "draw"

    card = declaration = choice(valid_held_cards)
    return card, declaration

  def should_accuse(self, declared: Card):
    if declared in self.suspicious: return True
    return False
