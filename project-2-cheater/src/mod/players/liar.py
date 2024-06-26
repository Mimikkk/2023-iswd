from random import choice, random
from .extended_player import ExtendedPlayer

class LiarPlayer(ExtendedPlayer):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def declare(self, declared):
    valid = [card for card in self.cards if not declared or card[0] >= declared[0]]
    declarable = [card for card in self.Cards if not declared or card[0] >= declared[0]]

    if not valid: return "draw"

    if declarable and random() < 0.25:
      card = choice(valid)
      declaration = choice(declarable)
      return card, declaration

    card = declaration = choice(valid)
    return card, declaration

  def should_accuse(self, declared): return False
