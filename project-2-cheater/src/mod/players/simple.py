from numpy.random import choice
from .player import Player

class SimplePlayer(Player):
  def putCard(self, declared_card):
    should_draw = len(self.cards) == 1 and declared_card is not None and self.cards[0][0] < declared_card[0]
    if should_draw: return "draw"

    declaration = card = min(self.cards, key=lambda x: x[0])
    if declared_card is not None:
      value = declared_card[0]
      if card[0] < value: declaration = (min(value + 1, 14), declaration[1])

    return card, declaration

  def checkCard(self, opponent_declaration):
    if opponent_declaration in self.cards: return True
    return choice([True, False], p=[0.3, 0.7])
