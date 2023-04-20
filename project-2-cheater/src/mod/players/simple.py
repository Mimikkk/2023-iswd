from numpy.random import choice
from .extended_player import ExtendedPlayer


class SimplePlayer(ExtendedPlayer):
  def declare(self, declared):
    should_draw = len(self.cards) == 1 and not self.is_valid(self.cards[0], declared)
    if should_draw: return "draw"

    declaration = card = min(self.cards, key=lambda x: x[0])
    if declared:
      value = declared[0]
      if card[0] < value: declaration = (min(value + 1, 14), declaration[1])

    return card, declaration

  def should_accuse(self, declared):
    if declared in self.cards: return True
    return choice([True, False], p=[0.3, 0.7])
