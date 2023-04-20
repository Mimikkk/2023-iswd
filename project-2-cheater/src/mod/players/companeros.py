from random import choice

from .player import Player

Card = tuple[int, int]


class CompanerosPlayer(Player):
  Cards = tuple(
    (rank, color)
    for rank in range(9, 15)
    for color in range(4)
  )

  def declare(self, declared):
    valid = [card for card in self.cards if self.is_valid(card, declared)]

    if len(self.cards) == 1 and len(valid) == 1: return valid[0], valid[0]
    if not valid: return "draw"

    card = declaration = min(self.cards, key=self.by_rank)

    if declared and not self.is_valid(card, declared):
      minimum = min(declared[0] + 1, 14)

      viable = [card for card in self.cards if card[0] in range(minimum, minimum + 3)]
      declaration = choice(viable or valid)

    return card, declaration

  def should_accuse(self, declared):
    return declared in self.cards

  def __init__(self, name: str):
    super().__init__(name)

  def putCard(self, declared_card):
    return self.declare(declared_card)

  def checkCard(self, opponent_declaration):
    return self.should_accuse(opponent_declaration)

  def is_valid(self, first: Card, other: Card | None):
    return not other or first[0] >= other[0]

  def by_rank(self, card: Card):
    return card[0]

  def by_color(self, card: Card):
    return card[1]
